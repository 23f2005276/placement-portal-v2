from flask_restful import Resource, reqparse
from sqlalchemy import func
from ppa.routes.check_rbac import check_jwt_and_role
from ppa.extensions import db
from flask_jwt_extended import jwt_required
from ppa.models import Students, Company, PlacementDrives, PPAUsers, IndustryTypes, UserStatus


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
        all_users = db.session.scalars(
            db.select(PPAUsers).where(
                db.or_(
                    PPAUsers.role == "company_hr",
                    PPAUsers.role == "student"
                )
            )
        ).all()

        all_users_dict = [
            {
                "id": getattr(user, "id"),
                "full_name": getattr(user, "full_name"),
                "email": getattr(user, "email"),
                "role": getattr(user, "role"),
            }
            for user in all_users
        ]

        return {
            "message": "Fetched all Users successfully!",
            "users": all_users_dict,
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
        stmt = (
            db.select(Company, PPAUsers, IndustryTypes)
            .join(PPAUsers, Company.company_hr_id == PPAUsers.id)
            .join(IndustryTypes, Company.company_industry_id == IndustryTypes.id)
            .where(Company.status == UserStatus.PENDING_ROLE)
        )
        results = db.session.execute(stmt).all()

        pending_companies_list = []
        for company, hr, industry in results:
            pending_companies_list.append({
                "company_name": getattr(company, "company_name"),
                "company_hr_name": getattr(hr, "full_name"),
                "company_hr_email": getattr(hr, "email"),
                "company_website": getattr(company, "company_website"),
                "company_industry": getattr(industry, "industry_name"),
                "company_description": getattr(company, "company_description"),
            })

        return {
            "message": "Fetched pending company approvals successfully",
            "pending_companies": pending_companies_list,
        }, 200