from flask_restful import Resource, reqparse
from sqlalchemy import func
from ppa.routes.check_rbac import check_jwt_and_role
from ppa.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from ppa.models import Students, Company, PlacementDrives, PPAUsers, IndustryTypes, Branches
from flask import request


class TestResource(Resource):
    @check_jwt_and_role("admin")
    @jwt_required()
    def get(self):
        return {"message": "api is up and running"}, 200


class TotalEntitiesResource(Resource):
    @check_jwt_and_role("admin")
    def get(self):
        students_count = db.session.scalar(
            db.select(func.count()).select_from(Students)
        )
        companies_count = db.session.scalar(
            db.select(func.count()).select_from(Company)
        )
        placement_drives_count = db.session.scalar(
            db.select(func.count()).select_from(PlacementDrives)
        )

        return {
            "message": "Fetched Total Entities Successfully",
            "total": {
                "students": students_count,
                "companies": companies_count,
                "placements": placement_drives_count,
            },
        }, 200


class AllUsersResource(Resource):
    @check_jwt_and_role("admin")
    def get(self):
        student_stmt = (
            db.select(PPAUsers, Students)
            .join(Students, PPAUsers.id == Students.id)
            .where(PPAUsers.role == "student")
        )
        student_results = db.session.execute(student_stmt).all()

        company_hr_stmt = (
            db.select(PPAUsers, Company)
            .join(Company, PPAUsers.id == Company.company_hr_id)
            .where(PPAUsers.role == "company_hr")
        )
        company_hr_results = db.session.execute(company_hr_stmt).all()

        users_list = []
        for user, student in student_results:
            users_list.append({
                "id": getattr(user, "id"),
                "full_name": getattr(user, "full_name"),
                "email": getattr(user, "email"),
                "role": "student",
                "status": getattr(student, "status")
            })

        for user, company in company_hr_results:
            users_list.append({
                "id": getattr(user, "id"),
                "full_name": getattr(user, "full_name"),
                "email": getattr(user, "email"),
                "role": "company_hr",
                "status": getattr(company, "status")
            })

        return {
            "message": "Fetched all Users successfully!",
            "users": users_list,
        }, 200


class UpdateUserStatusResource(Resource):
    @check_jwt_and_role("admin")
    def patch(self):
        parser = reqparse.RequestParser()

        parser.add_argument("email", type=str, required=True, help="email is required to change the status of the user", location="json")
        parser.add_argument("action", type=str, required=True, help="action is required to change the status of the user", location="json") # action is either "approve" or "blacklist"

        req_fields = parser.parse_args()

        existing_user = db.session.scalar(db.select(PPAUsers).where(PPAUsers.email == req_fields.get("email")))

        if not existing_user or getattr(existing_user, "role") == "admin":
            return {
                "message": "Email not found on the server"
            }, 404

        if req_fields.get("action") not in ["approve", "blacklist"]:
            return {
                "message": "Invalid action performed on the status of the user"
            }, 400

        if getattr(existing_user, "role") == "company_hr":
            company_obj = db.session.scalar(db.select(Company).where(Company.company_hr_id == getattr(existing_user, "id")))

            if req_fields.get("action") == "approve":
                company_obj.status = "approved"
            
            if req_fields.get("action") == "blacklist":
                company_obj.status = "blacklisted"

            db.session.commit()

            return {
                "message": "updated the status of the user"
            }, 200
        
        if getattr(existing_user, "role") == "student":
            student_obj = db.session.scalar(db.select(Students).where(Students.id == getattr(existing_user, "id")))

            if req_fields.get("action") == "approve":
                student_obj.status = "approved"
            
            if req_fields.get("action") == "blacklist":
                student_obj.status = "blacklisted"

            db.session.commit()

            return {
                "message": "updated the status of the user"
            }, 200
        
class ApprovalResource(Resource):
    @check_jwt_and_role("admin")
    def get(self):
        company_stmt = (
            db.select(Company, PPAUsers, IndustryTypes)
            .join(PPAUsers, Company.company_hr_id == PPAUsers.id)
            .join(IndustryTypes, Company.company_industry_id == IndustryTypes.id)
            .where(Company.status == "pending")
        )
        company_results = db.session.execute(company_stmt).all()

        pending_companies_list = []
        for company, hr, industry in company_results:
            pending_companies_list.append({
                "id": getattr(company, "id"),
                "company_name": getattr(company, "company_name"),
                "company_hr_name": getattr(hr, "full_name"),
                "company_hr_email": getattr(hr, "email"),
                "company_website": getattr(company, "company_website"),
                "company_industry": getattr(industry, "industry_name"),
                "company_description": getattr(company, "company_description"),
            })

        drive_stmt = (
            db.select(PlacementDrives, Company)
            .join(Company, PlacementDrives.company_id == Company.id)
            .where(PlacementDrives.status == "pending")
        )
        drive_results = db.session.execute(drive_stmt).all()

        pending_drives_list = []
        for drive, company in drive_results:
            pending_drives_list.append({
                "id": getattr(drive, "id"),
                "company_name": getattr(company, "company_name"),
                "job_title": getattr(drive, "job_title"),
                "job_description": getattr(drive, "job_description"),
                "min_cgpa": float(getattr(drive, "min_cgpa")) if getattr(drive, "min_cgpa") is not None else None,
                "eligible_year": getattr(drive, "eligible_year"),
                "location": getattr(drive, "location"),
                "salary_package": getattr(drive, "salary_package"),
                "application_deadline": getattr(drive, "application_deadline").isoformat() if getattr(drive, "application_deadline") else None,
            })

        return {
            "message": "Fetched pending company and placement drive approvals successfully",
            "pending_companies": pending_companies_list,
            "pending_drives": pending_drives_list,
        }, 200

    @check_jwt_and_role("admin")
    def patch(self):
        data = request.get_json()
        if not data:
            return {"message": "Request body must be JSON"}, 400

        entity_type = data.get("type")
        entity_id = data.get("id")
        action = data.get("action", "approve")

        if not entity_type or not entity_id:
            return {"message": "type and id are required fields"}, 400

        if entity_type == "company":
            if action != "approve":
                return {"message": "Invalid action for company approvals. Only 'approve' is allowed."}, 400

            company = db.session.scalar(db.select(Company).where(Company.id == entity_id))
            if not company:
                return {"message": "Company not found"}, 404
            if company.status != "pending":
                return {"message": "Company status is not pending"}, 400
            company.status = "approved"
            db.session.commit()

        elif entity_type == "drive":
            if action not in ["approve", "reject"]:
                return {"message": "Invalid action for placement drive approvals. Must be 'approve' or 'reject'."}, 400

            drive = db.session.scalar(db.select(PlacementDrives).where(PlacementDrives.id == entity_id))
            if not drive:
                return {"message": "Placement drive not found"}, 404
            if drive.status != "pending":
                return {"message": "Placement drive status is not pending"}, 400

            if action == "approve":
                drive.status = "approved"
            else:
                drive.status = "rejected"
            db.session.commit()

        else:
            return {"message": "Invalid type. Must be either company or drive"}, 400

        company_stmt = (
            db.select(Company, PPAUsers, IndustryTypes)
            .join(PPAUsers, Company.company_hr_id == PPAUsers.id)
            .join(IndustryTypes, Company.company_industry_id == IndustryTypes.id)
            .where(Company.status == "pending")
        )
        company_results = db.session.execute(company_stmt).all()

        pending_companies_list = []
        for company, hr, industry in company_results:
            pending_companies_list.append({
                "id": getattr(company, "id"),
                "company_name": getattr(company, "company_name"),
                "company_hr_name": getattr(hr, "full_name"),
                "company_hr_email": getattr(hr, "email"),
                "company_website": getattr(company, "company_website"),
                "company_industry": getattr(industry, "industry_name"),
                "company_description": getattr(company, "company_description"),
            })

        drive_stmt = (
            db.select(PlacementDrives, Company)
            .join(Company, PlacementDrives.company_id == Company.id)
            .where(PlacementDrives.status == "pending")
        )
        drive_results = db.session.execute(drive_stmt).all()

        pending_drives_list = []
        for drive, company in drive_results:
            pending_drives_list.append({
                "id": getattr(drive, "id"),
                "company_name": getattr(company, "company_name"),
                "job_title": getattr(drive, "job_title"),
                "job_description": getattr(drive, "job_description"),
                "min_cgpa": float(getattr(drive, "min_cgpa")) if getattr(drive, "min_cgpa") is not None else None,
                "eligible_year": getattr(drive, "eligible_year"),
                "location": getattr(drive, "location"),
                "salary_package": getattr(drive, "salary_package"),
                "application_deadline": getattr(drive, "application_deadline").isoformat() if getattr(drive, "application_deadline") else None,
            })

        return {
            "message": "Status updated successfully",
            "pending_companies": pending_companies_list,
            "pending_drives": pending_drives_list
        }, 200


class AdminInfoResource(Resource):
    @check_jwt_and_role("admin")
    def get(self):
        admin_id = get_jwt_identity()
        admin = db.session.scalar(db.select(PPAUsers).where(PPAUsers.id == int(admin_id)))
        if not admin:
            return {"message": "Admin user not found"}, 404
        return {
            "full_name": getattr(admin, "full_name"),
            "email": getattr(admin, "email")
        }, 200

    @check_jwt_and_role("admin")
    def patch(self):
        data = request.get_json()
        if not data:
            return {"message": "Request body must be JSON"}, 400

        full_name = data.get("full_name")
        if not full_name:
            return {"message": "full_name is required"}, 400

        admin_id = get_jwt_identity()
        admin = db.session.scalar(db.select(PPAUsers).where(PPAUsers.id == int(admin_id)))
        if not admin:
            return {"message": "Admin user not found"}, 404

        admin.full_name = full_name
        db.session.commit()

        return {
            "message": "Admin full name updated successfully",
            "full_name": getattr(admin, "full_name")
        }, 200


class UserInfoResource(Resource):
    @check_jwt_and_role("admin")
    def get(self):
        user_id = request.args.get("id")
        if not user_id:
            return {"message": "User ID is required"}, 400

        user = db.session.scalar(db.select(PPAUsers).where(PPAUsers.id == int(user_id)))
        if not user:
            return {"message": "User not found"}, 404

        if user.role == "student":
            student_stmt = (
                db.select(Students, Branches)
                .join(Branches, Students.branch_id == Branches.id)
                .where(Students.id == user.id)
            )
            res = db.session.execute(student_stmt).first()
            if not res:
                return {"message": "Student details not found"}, 404
            student, branch = res
            return {
                "role": "student",
                "full_name": getattr(user, "full_name"),
                "email": getattr(user, "email"),
                "student_roll_no": getattr(student, "student_roll_no"),
                "branch": getattr(branch, "branch_name"),
                "year_of_study": getattr(student, "year_of_study"),
                "current_cgpa": float(getattr(student, "current_cgpa")) if getattr(student, "current_cgpa") is not None else None
            }, 200

        elif user.role == "company_hr":
            company_stmt = (
                db.select(Company, IndustryTypes)
                .join(IndustryTypes, Company.company_industry_id == IndustryTypes.id)
                .where(Company.company_hr_id == user.id)
            )
            res = db.session.execute(company_stmt).first()
            if not res:
                return {"message": "Company details not found"}, 404
            company, industry = res
            return {
                "role": "company_hr",
                "company_name": getattr(company, "company_name"),
                "company_hr_name": getattr(user, "full_name"),
                "company_hr_email": getattr(user, "email"),
                "company_website": getattr(company, "company_website"),
                "company_industry": getattr(industry, "industry_name"),
                "company_description": getattr(company, "company_description")
            }, 200

        else:
            return {"message": "Invalid user role"}, 400

class AdminPlacementDrivesResource(Resource):
    @check_jwt_and_role("admin")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("drive_id", type=int, required=False, location="args")
        args = parser.parse_args()

        from ppa.models import EligibleBranches, Branches

        drive_id = args.get("drive_id")
        if drive_id:
            drive_stmt = (
                db.select(PlacementDrives, Company)
                .join(Company, PlacementDrives.company_id == Company.id)
                .where(PlacementDrives.id == drive_id)
            )
            res = db.session.execute(drive_stmt).first()
            if not res:
                return {"message": "Placement drive not found"}, 404
            drive, company = res

            branches_stmt = (
                db.select(Branches)
                .join(EligibleBranches, Branches.id == EligibleBranches.branch_id)
                .where(EligibleBranches.placement_drive_id == drive_id)
            )
            branches = db.session.scalars(branches_stmt).all()
            branch_names = [getattr(b, "branch_name") for b in branches]

            return {
                "id": getattr(drive, "id"),
                "company_name": getattr(company, "company_name"),
                "job_title": getattr(drive, "job_title"),
                "job_description": getattr(drive, "job_description"),
                "salary_package": getattr(drive, "salary_package"),
                "location": getattr(drive, "location"),
                "application_deadline": getattr(drive, "application_deadline").isoformat(),
                "status": getattr(drive, "status"),
                "min_cgpa": float(getattr(drive, "min_cgpa")),
                "eligible_year": getattr(drive, "eligible_year"),
                "eligible_branches": branch_names
            }, 200

        drives_stmt = (
            db.select(PlacementDrives, Company)
            .join(Company, PlacementDrives.company_id == Company.id)
        )
        res = db.session.execute(drives_stmt).all()

        drives_list = []
        for drive, company in res:
            branches_stmt = (
                db.select(Branches)
                .join(EligibleBranches, Branches.id == EligibleBranches.branch_id)
                .where(EligibleBranches.placement_drive_id == getattr(drive, "id"))
            )
            branches = db.session.scalars(branches_stmt).all()
            branch_names = [getattr(b, "branch_name") for b in branches]

            branches_text = ", ".join(branch_names)
            eligibility_text = f"{branches_text} > {getattr(drive, 'min_cgpa')} CGPA, Yr {getattr(drive, 'eligible_year')}"

            drives_list.append({
                "id": getattr(drive, "id"),
                "company_name": getattr(company, "company_name"),
                "job_title": getattr(drive, "job_title"),
                "salary_package": getattr(drive, "salary_package"),
                "location": getattr(drive, "location"),
                "application_deadline": getattr(drive, "application_deadline").isoformat(),
                "status": getattr(drive, "status"),
                "min_cgpa": float(getattr(drive, "min_cgpa")),
                "eligible_year": getattr(drive, "eligible_year"),
                "eligible_branches": branch_names,
                "eligibility_text": eligibility_text
            })

        return drives_list, 200

    @check_jwt_and_role("admin")
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("drive_id", type=int, required=True, location="json")
        parser.add_argument("action", type=str, required=True, location="json")
        args = parser.parse_args()

        drive = db.session.scalar(db.select(PlacementDrives).where(PlacementDrives.id == args.get("drive_id")))
        if not drive:
            return {"message": "Placement drive not found"}, 404

        if getattr(drive, "status") != "pending":
            return {"message": "Only pending drives can be approved or rejected"}, 400

        action = args.get("action")
        if action == "approve":
            drive.status = "approved"
        elif action == "reject":
            drive.status = "rejected"
        else:
            return {"message": "Invalid action"}, 400

        db.session.commit()
        return {"message": f"Placement drive has been successfully {drive.status}"}, 200

class AdminPlacementReportsResource(Resource):
    @check_jwt_and_role("admin")
    def get(self):
        from ppa.models import StudentPlacementStatus, StudentPlacementState, StudentApplications, StudentApplicationStatus
        
        total_students = db.session.scalar(db.select(func.count(Students.id)))
        placed_students = db.session.scalar(
            db.select(func.count(StudentPlacementStatus.student_id))
            .where(StudentPlacementStatus.placement_status == StudentPlacementState.PLACED_STATUS)
        ) or 0

        overall_placement_rate = 0.0
        if total_students and total_students > 0:
            overall_placement_rate = round((placed_students / total_students) * 100, 1)

        selected_apps_stmt = (
            db.select(StudentApplications, PlacementDrives)
            .join(PlacementDrives, StudentApplications.placement_id == PlacementDrives.id)
            .where(StudentApplications.status == StudentApplicationStatus.SELECTED_STATUS)
        )
        selected_res = db.session.execute(selected_apps_stmt).all()

        packages = [float(getattr(drive, "salary_package")) for _, drive in selected_res]
        avg_package = round(sum(packages) / len(packages), 1) if packages else 0.0
        highest_package = max(packages) if packages else 0.0

        company_stats = {}
        for app, drive in selected_res:
            company_id = getattr(drive, "company_id")
            if company_id not in company_stats:
                comp = db.session.scalar(db.select(Company).where(Company.id == company_id))
                sector = "N/A"
                if comp:
                    from ppa.models import IndustryTypes
                    ind = db.session.scalar(db.select(IndustryTypes).where(IndustryTypes.id == getattr(comp, "company_industry_id")))
                    if ind:
                        sector = getattr(ind, "industry_name")
                company_stats[company_id] = {
                    "company_name": getattr(comp, "company_name") if comp else "Unknown",
                    "sector": sector,
                    "students_hired": 0,
                    "packages_sum": 0.0
                }
            company_stats[company_id]["students_hired"] += 1
            company_stats[company_id]["packages_sum"] += float(getattr(drive, "salary_package"))

        top_companies = []
        for cid, info in company_stats.items():
            avg_pkg = round(info["packages_sum"] / info["students_hired"], 1) if info["students_hired"] > 0 else 0.0
            top_companies.append({
                "company_name": info["company_name"],
                "sector": info["sector"],
                "students_hired": info["students_hired"],
                "avg_package": avg_pkg
            })

        top_companies.sort(key=lambda x: x["students_hired"], reverse=True)

        return {
            "total_students_placed": placed_students,
            "overall_placement_rate": overall_placement_rate,
            "average_package": avg_package,
            "highest_package": highest_package,
            "top_companies": top_companies
        }, 200