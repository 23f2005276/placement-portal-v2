from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from ppa.extensions import db
from ppa.models import Students, Company

class IdentityResource(Resource):
    @jwt_required()
    def get(self):
        jwt = get_jwt()
        role = str(jwt.get("role"))
        user_id = jwt.get("sub")

        if role != "admin":
            if role == "student":
                student = db.session.scalar(db.select(Students).where(Students.id == int(user_id)))
                if student and student.status in ["pending", "blacklisted"]:
                    return {"message": student.status}, 403
            elif role == "company_hr":
                company = db.session.scalar(db.select(Company).where(Company.company_hr_id == int(user_id)))
                if company and company.status in ["pending", "blacklisted"]:
                    return {"message": company.status}, 403

        return {
            "message": "User Identified successfully",
            "role": role,
            "user_id": str(user_id)
        }, 200