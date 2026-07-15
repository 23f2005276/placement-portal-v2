from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def check_jwt_and_role(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            jwt = get_jwt()

            role_claims = str(jwt.get("role"))
            user_id = jwt.get("sub")

            if role_claims != "admin":
                from flask import request
                req_user_id = None
                if request.method == "GET":
                    if request.args and "user_id" in request.args:
                        req_user_id = request.args.get("user_id")
                elif request.method in ["POST", "PATCH", "PUT"]:
                    if request.is_json:
                        data = request.get_json(silent=True)
                        if data and "user_id" in data:
                            req_user_id = data.get("user_id")

                if req_user_id is not None:
                    if str(req_user_id) != str(user_id):
                        return {"message": "You're not allowed to access that resource"}, 403

                from ppa.extensions import db
                from ppa.models import Students, Company

                if role_claims == "student":
                    student = db.session.scalar(db.select(Students).where(Students.id == int(user_id)))
                    if student and student.status in ["pending", "blacklisted"]:
                        return {"message": student.status}, 403
                elif role_claims == "company_hr":
                    company = db.session.scalar(db.select(Company).where(Company.company_hr_id == int(user_id)))
                    if company and company.status in ["pending", "blacklisted"]:
                        return {"message": company.status}, 403

            if role_claims in roles or role_claims == "admin":
                return fn(*args, **kwargs)

            return {
                "message": "You're not allowed to access that resource"
            }, 403
        return wrapper
    return decorator          