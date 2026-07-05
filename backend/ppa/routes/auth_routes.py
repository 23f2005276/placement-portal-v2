import time
from datetime import timedelta
from ppa.extensions import db, bcrypt_instance
from ppa.models import PPAUsers, Company, IndustryTypes, Students, Branches
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token

# /api/signup
class SignupResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument("email", type=str, required=True, help="Email is required")
        parser.add_argument(
            "password", type=str, required=True, help="Password is required"
        )
        parser.add_argument(
            "full_name",
            type=str,
            required=True,
            help="Please provide the full name of the user",
        )
        parser.add_argument(
            "role", type=str, required=True, help="Please provide the role of the user"
        )

        parser.add_argument("company_name", type=str, required=False)
        parser.add_argument("company_website", type=str, required=False)
        parser.add_argument("company_industry", type=str, required=False)
        parser.add_argument("company_description", type=str, required=False)

        parser.add_argument("student_roll_no", type=str, required=False)
        parser.add_argument("branch", type=str, required=False)
        parser.add_argument("year_of_study", type=int, required=False)
        parser.add_argument("current_cgpa", type=float, required=False)

        req_fields = parser.parse_args()

        existing_user = PPAUsers.query.filter_by(email=req_fields.get("email")).first()
        if existing_user:
            return jsonify(
                {"message": "User already exists!"}
            ), 409  # conflict with state of the system

        if req_fields.get("role") == "company_hr":
            if (
                not (req_fields.get("company_name") and req_fields.get("company_name").strip())
                or not (
                    req_fields.get("company_website")
                    and req_fields.get("company_website").strip()
                )
                or not (
                    req_fields.get("company_industry")
                    and req_fields.get("company_industry").strip()
                )
                or not (
                    req_fields.get("company_description")
                    and req_fields.get("company_description").strip()
                )
            ):
                return jsonify(
                    {"message": "Required fields are missing for the company hr role"}
                ), 400

            password_hash = bcrypt_instance.generate_password_hash(
                req_fields.get("password")
            ).decode("utf-8")
            company_hr = PPAUsers(
                full_name=req_fields.get("full_name"),
                email=req_fields.get("email"),
                password_hash=password_hash,
                role="company_hr",
            )
            db.session.add(company_hr)
            db.session.flush()

            company_industry_id = getattr(
                IndustryTypes.query.filter_by(
                    industry_name=req_fields.get("company_industry")
                ).first(),
                "id"
            )
            company_tuple = Company(
                company_hr_id=getattr(company_hr, "id"),
                company_name=req_fields.get("company_name"),
                company_website=req_fields.get("company_website"),
                company_industry_id=company_industry_id,
                company_description=req_fields.get("company_description"),
            )
            db.session.add(company_tuple)
            db.session.commit()

            role_claims = {"role": "company_hr"}
            expires_delta = timedelta(minutes=10)
            access_token = create_access_token(identity=str(getattr(company_hr, "id")), additional_claims=role_claims, expires_delta=expires_delta)

            return jsonify(
                {"message": "Created company and hr user successfully!", "access_token": access_token}
            ), 201

        if (
            not (
                req_fields.get("student_roll_no") and req_fields.get("student_roll_no").strip()
            )
            or not (req_fields.get("branch") and req_fields.get("branch").strip())
            or not (req_fields.get("year_of_study"))
            or not (req_fields.get("current_cgpa"))
        ):
            return jsonify(
                {"message": "Required fields are missing for Student role"}
            ), 400
        
        password_hash = bcrypt_instance.generate_password_hash(
            req_fields.get("password")
        ).decode("utf-8")
        student_user = PPAUsers(
            full_name=req_fields.get("full_name"),
            email=req_fields.get("email"),
            password_hash=password_hash,
            role=req_fields.get("role"),
        )
        db.session.add(student_user)
        db.session.flush()

        branch_id = getattr(Branches.query.filter_by(branch_name=req_fields.get("branch")).first(), "id")
        student_tuple = Students(id=getattr(student_user, "id"), student_roll_no=req_fields.get("student_roll_no"), branch_id=branch_id, year_of_study=req_fields.get("year_of_study"), current_cgpa=req_fields.get("current_cgpa"))
        db.session.add(student_tuple)
        db.session.commit()

        role_claims = {"role": "student"}
        expires_delta=timedelta(minutes=10)
        access_token = create_access_token(identity=str(getattr(student_user, "id")), additional_claims=role_claims ,expires_delta=expires_delta)
        return jsonify({"message": "Student user created successfully", "access_token":access_token}), 201

# /api/login
class LoginResource(Resource):
    def post():
        req_parser = reqparse.RequestParser()

        req_parser.add_argument("email", type=str, required=True, help="Email is required for Login")
        req_parser.add_argument("password", type=str, required=True, help="Password is required for Login")

        req_fields = req_parser.parse_args()

        user = PPAUsers.query.filter_by(email=req_fields.get("email")).first()

        start_time = time.time()

        MIN_TIME_SLEEP = 0.200

        if user and bcrypt_instance.check_password_hash(user.password, req_fields.get("password")):
            role_claims = {"role": getattr(user, "role")}
            expires_delta=timedelta(minutes=10)
            access_token = create_access_token(identity=getattr(user, "id"), additional_claims=role_claims, expires_delta=expires_delta)
            return jsonify(
                {
                    "message": "User authenticated successfully",
                    "access_token": access_token
                }
            ), 200
        
        auth_end_time = time.time()
        time_delta = auth_end_time - start_time
        if time_delta < MIN_TIME_SLEEP:
            time.sleep(MIN_TIME_SLEEP - time_delta)
        
        return jsonify(
            {
                "message": "email and password combination incorrect"
            }
        ), 401