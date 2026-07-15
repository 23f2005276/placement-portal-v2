from flask_restful import Resource, reqparse
from ppa.routes.check_rbac import check_jwt_and_role
from ppa.extensions import db, bcrypt_instance
from ppa.models import Company, PPAUsers, IndustryTypes, PlacementDrives, EligibleBranches, Branches, Students, Skills, StudentSkills

class ProfileResource(Resource):
    @check_jwt_and_role("company_hr")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True, location="args")
        args = parser.parse_args()

        stmt = (
            db.select(Company, PPAUsers, IndustryTypes)
            .join(PPAUsers, Company.company_hr_id == PPAUsers.id)
            .join(IndustryTypes, Company.company_industry_id == IndustryTypes.id)
            .where(PPAUsers.id == args.get("user_id"))
        )
        result = db.session.execute(stmt).first()
        if not result:
            return {"message": "Profile details not found"}, 404

        company, hr, industry = result
        return {
            "hr_name": getattr(hr, "full_name"),
            "hr_email": getattr(hr, "email"),
            "company_name": getattr(company, "company_name"),
            "company_website": getattr(company, "company_website"),
            "company_description": getattr(company, "company_description"),
            "company_industry": getattr(industry, "industry_name"),
            "status": getattr(company, "status")
        }, 200

    @check_jwt_and_role("company_hr")
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True, location="json")
        parser.add_argument("hr_name", type=str, required=True, location="json")
        parser.add_argument("hr_email", type=str, required=True, location="json")
        parser.add_argument("hr_password", type=str, required=False, location="json")
        args = parser.parse_args()

        hr = db.session.scalar(db.select(PPAUsers).where(PPAUsers.id == args.get("user_id")))
        if not hr:
            return {"message": "HR user not found"}, 404

        hr.full_name = args.get("hr_name")
        hr.email = args.get("hr_email")

        if args.get("hr_password") and args.get("hr_password").strip():
            hr.password_hash = bcrypt_instance.generate_password_hash(args.get("hr_password")).decode("utf-8")

        db.session.commit()
        return {"message": "Profile updated successfully"}, 200

class CreatePlacementDriveResource(Resource):
    @check_jwt_and_role("company_hr")
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True, location="json")
        parser.add_argument("job_title", type=str, required=True, location="json")
        parser.add_argument("job_description", type=str, required=True, location="json")
        parser.add_argument("min_cgpa", type=float, required=True, location="json")
        parser.add_argument("eligible_year", type=int, required=True, location="json")
        parser.add_argument("location", type=str, required=True, location="json")
        parser.add_argument("salary_package", type=int, required=True, location="json")
        parser.add_argument("application_deadline", type=str, required=True, location="json")
        parser.add_argument("eligible_branches", type=list, required=True, location="json")
        args = parser.parse_args()

        company = db.session.scalar(db.select(Company).where(Company.company_hr_id == args.get("user_id")))
        if not company:
            return {"message": "Company not found for this HR"}, 404

        from datetime import datetime
        try:
            deadline_dt = datetime.strptime(args.get("application_deadline"), "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return {"message": "Invalid date format for application_deadline"}, 400

        drive = PlacementDrives(
            company_id=getattr(company, "id"),
            job_title=args.get("job_title"),
            job_description=args.get("job_description"),
            min_cgpa=args.get("min_cgpa"),
            eligible_year=args.get("eligible_year"),
            location=args.get("location"),
            salary_package=args.get("salary_package"),
            application_deadline=deadline_dt
        )
        db.session.add(drive)
        db.session.flush()

        for branch_name in args.get("eligible_branches"):
            branch = db.session.scalar(db.select(Branches).where(Branches.branch_name == branch_name))
            if branch:
                eligible_branch = EligibleBranches(
                    placement_drive_id=getattr(drive, "id"),
                    branch_id=getattr(branch, "id")
                )
                db.session.add(eligible_branch)

        db.session.commit()
        return {"message": "Placement drive created successfully"}, 201

class ActivePlacementDrivesResource(Resource):
    @check_jwt_and_role("company_hr")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True, location="args")
        args = parser.parse_args()

        company = db.session.scalar(db.select(Company).where(Company.company_hr_id == args.get("user_id")))
        if not company:
            return {"message": "Company not found"}, 404

        drives = db.session.scalars(
            db.select(PlacementDrives)
            .where(PlacementDrives.company_id == getattr(company, "id"))
            .where(PlacementDrives.status == "approved")
        ).all()

        result = []
        for drive in drives:
            result.append({
                "id": getattr(drive, "id"),
                "company_name": getattr(company, "company_name"),
                "job_title": getattr(drive, "job_title"),
                "applicants_count": len(getattr(drive, "students_applied"))
            })

        return result, 200

class DriveApplicationsResource(Resource):
    @check_jwt_and_role("company_hr")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True, location="args")
        parser.add_argument("drive_id", type=int, required=True, location="args")
        args = parser.parse_args()

        company = db.session.scalar(db.select(Company).where(Company.company_hr_id == args.get("user_id")))
        if not company:
            return {"message": "Company not found"}, 404

        drive = db.session.scalar(db.select(PlacementDrives).where(PlacementDrives.id == args.get("drive_id")))
        if not drive:
            return {"message": "Placement drive not found"}, 404

        if getattr(drive, "company_id") != getattr(company, "id"):
            return {"message": "Unauthorized access to this placement drive"}, 403

        if getattr(drive, "status") not in ["approved", "closed"]:
            return {"message": "Access denied: Cannot view applications of a pending or rejected placement drive"}, 403

        from ppa.models import StudentApplications, Students, PPAUsers, Branches
        stmt = (
            db.select(StudentApplications, Students, PPAUsers, Branches)
            .join(Students, StudentApplications.student_id == Students.id)
            .join(PPAUsers, Students.id == PPAUsers.id)
            .join(Branches, Students.branch_id == Branches.id)
            .where(StudentApplications.placement_id == getattr(drive, "id"))
        )
        apps = db.session.execute(stmt).all()

        applications_list = []
        for app, student, user, branch in apps:
            applications_list.append({
                "id": getattr(app, "id"),
                "student_id": getattr(student, "id"),
                "student_name": getattr(user, "full_name"),
                "roll_no": getattr(student, "student_roll_no"),
                "branch_name": getattr(branch, "branch_name"),
                "cgpa": float(getattr(student, "current_cgpa")) if getattr(student, "current_cgpa") is not None else None,
                "status": getattr(app, "status")
            })

        return {
            "job_title": getattr(drive, "job_title"),
            "applications": applications_list
        }, 200

    @check_jwt_and_role("company_hr")
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True, location="json")
        parser.add_argument("application_id", type=int, required=True, location="json")
        parser.add_argument("status", type=str, required=True, location="json")
        args = parser.parse_args()

        company = db.session.scalar(db.select(Company).where(Company.company_hr_id == args.get("user_id")))
        if not company:
            return {"message": "Company not found"}, 404

        from ppa.models import StudentApplications
        app = db.session.scalar(db.select(StudentApplications).where(StudentApplications.id == args.get("application_id")))
        if not app:
            return {"message": "Application not found"}, 404

        drive = db.session.scalar(db.select(PlacementDrives).where(PlacementDrives.id == getattr(app, "placement_id")))
        if getattr(drive, "company_id") != getattr(company, "id"):
            return {"message": "Unauthorized access"}, 403

        app.status = args.get("status")
        if args.get("status") == "selected":
            from ppa.models import StudentPlacementStatus, StudentPlacementState
            status_row = db.session.scalar(db.select(StudentPlacementStatus).where(StudentPlacementStatus.student_id == getattr(app, "student_id")))
            if not status_row:
                status_row = StudentPlacementStatus(student_id=getattr(app, "student_id"), placement_status=StudentPlacementState.PLACED_STATUS)
                db.session.add(status_row)
            else:
                status_row.placement_status = StudentPlacementState.PLACED_STATUS
        db.session.commit()
        return {"message": "Application status updated successfully"}, 200

class CompanyStudentInfoResource(Resource):
    @check_jwt_and_role("company_hr")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True, location="args")
        parser.add_argument("student_id", type=int, required=True, location="args")
        args = parser.parse_args()

        student_stmt = (
            db.select(Students, PPAUsers, Branches)
            .join(PPAUsers, Students.id == PPAUsers.id)
            .join(Branches, Students.branch_id == Branches.id)
            .where(Students.id == args.get("student_id"))
        )
        res = db.session.execute(student_stmt).first()
        if not res:
            return {"message": "Student details not found"}, 404
        student, user, branch = res

        skills_stmt = (
            db.select(Skills)
            .join(StudentSkills, Skills.id == StudentSkills.skill_id)
            .where(StudentSkills.student_id == getattr(student, "id"))
        )
        skills_res = db.session.scalars(skills_stmt).all()
        skills_list = [getattr(s, "skill_name") for s in skills_res]

        return {
            "role": "student",
            "full_name": getattr(user, "full_name"),
            "email": getattr(user, "email"),
            "student_roll_no": getattr(student, "student_roll_no"),
            "branch": getattr(branch, "branch_name"),
            "year_of_study": getattr(student, "year_of_study"),
            "current_cgpa": float(getattr(student, "current_cgpa")) if getattr(student, "current_cgpa") is not None else None,
            "skills": skills_list
        }, 200

class CompanyPlacementDrivesResource(Resource):
    @check_jwt_and_role("company_hr")
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True, location="json")
        args = parser.parse_args()

        company = db.session.scalar(db.select(Company).where(Company.company_hr_id == args.get("user_id")))
        if not company:
            return {"message": "Company not found"}, 404

        drives = db.session.scalars(
            db.select(PlacementDrives)
            .where(PlacementDrives.company_id == getattr(company, "id"))
        ).all()

        result = []
        for drive in drives:
            result.append({
                "id": getattr(drive, "id"),
                "job_title": getattr(drive, "job_title"),
                "status": getattr(drive, "status"),
                "applicants_count": len(getattr(drive, "students_applied"))
            })

        return result, 200

    @check_jwt_and_role("company_hr")
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True, location="json")
        parser.add_argument("drive_id", type=int, required=True, location="json")
        parser.add_argument("status", type=str, required=True, location="json")
        args = parser.parse_args()

        company = db.session.scalar(db.select(Company).where(Company.company_hr_id == args.get("user_id")))
        if not company:
            return {"message": "Company not found"}, 404

        drive = db.session.scalar(db.select(PlacementDrives).where(PlacementDrives.id == args.get("drive_id")))
        if not drive:
            return {"message": "Placement drive not found"}, 404

        if getattr(drive, "company_id") != getattr(company, "id"):
            return {"message": "Unauthorized access to this placement drive"}, 403

        if getattr(drive, "status") != "approved":
            return {"message": "Only approved placement drives can be closed"}, 400

        drive.status = args.get("status")
        db.session.commit()
        return {"message": "Placement drive updated successfully"}, 200

    @check_jwt_and_role("company_hr")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True, location="args")
        parser.add_argument("drive_id", type=int, required=True, location="args")
        args = parser.parse_args()

        company = db.session.scalar(db.select(Company).where(Company.company_hr_id == args.get("user_id")))
        if not company:
            return {"message": "Company not found"}, 404

        drive = db.session.scalar(db.select(PlacementDrives).where(PlacementDrives.id == args.get("drive_id")))
        if not drive:
            return {"message": "Placement drive not found"}, 404

        if getattr(drive, "company_id") != getattr(company, "id"):
            return {"message": "Unauthorized access to this placement drive"}, 403

        from ppa.models import Branches, EligibleBranches
        branches_stmt = (
            db.select(Branches)
            .join(EligibleBranches, Branches.id == EligibleBranches.branch_id)
            .where(EligibleBranches.placement_drive_id == args.get("drive_id"))
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
            "min_cgpa": float(getattr(drive, "min_cgpa")),
            "eligible_year": getattr(drive, "eligible_year"),
            "eligible_branches": branch_names
        }, 200
