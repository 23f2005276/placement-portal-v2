from datetime import timedelta
from ppa.extensions import db, bcrypt_instance
from ppa.models import PPAUsers, Company, IndustryTypes, Students, Branches, StudentPlacementStatus, CompanyPlacementData
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from flask import jsonify, make_response

# /api/signup?category=student/company_hr>
class SignupResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("category", required=True, location="args")
        req_fields = parser.parse_args()

        if req_fields.get("category") == "student":
            branches_list = db.session.scalars(db.select(Branches)).all()    
            branch_dict = dict({
                "content": [getattr(branch, "branch_name") for branch in branches_list]
            })
            return {"message": "fetched branches successfully", "branches_list": branch_dict}, 200 

        if req_fields.get("category") == "company_hr":
            industry_list = db.session.scalars(db.select(IndustryTypes)).all()
            industry_dict = dict(
                {
                    "content": [getattr(industry, "industry_name") for industry in industry_list]
                }
            )
            return {"message": "fetched industries successfully", "industry_list": industry_dict}, 200 
        
        return {
            "message": "You are not allowed to access that"
        }, 403
    
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument("email", type=str, required=True, help="Email is required", location="json")
        parser.add_argument(
            "password", type=str, required=True, help="Password is required", location="json"
        )
        parser.add_argument(
            "full_name",
            type=str,
            required=True,
            help="Please provide the full name of the user",
            location="json",
        )
        parser.add_argument(
            "role", type=str, required=True, help="Please provide the role of the user", location="json"
        )

        parser.add_argument("company_name", type=str, required=False, location="json")
        parser.add_argument("company_website", type=str, required=False, location="json")
        parser.add_argument("company_industry", type=str, required=False, location="json")
        parser.add_argument("company_description", type=str, required=False, location="json")

        parser.add_argument("student_roll_no", type=str, required=False, location="json")
        parser.add_argument("branch", type=str, required=False, location="json")
        parser.add_argument("year_of_study", type=int, required=False, location="json")
        parser.add_argument("current_cgpa", type=float, required=False, location="json")

        req_fields = parser.parse_args()

        if (req_fields.get("role") in ["admin"]) or (req_fields.get("role") not in ["company_hr", "student"]) :
            return {"message":"You are not allowed to do that"}, 403

        existing_user = db.session.scalars(db.select(PPAUsers).filter_by(email=req_fields.get("email"))).first()
        if existing_user:
            return {
                "message": "User already exists!"
            }, 409  # conflict with state of the system

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
                return {
                    "message": "Required fields are missing for the company hr role"
                }, 400

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

            company_industry_id = db.session.scalars(db.select(IndustryTypes.id).filter_by(industry_name=req_fields.get("company_industry"))).first()

            if not company_industry_id:
                return {
                    "message": "Company Industry Not Found"
                }, 400 

            company_tuple = Company(
                company_hr_id=getattr(company_hr, "id"),
                company_name=req_fields.get("company_name"),
                company_website=req_fields.get("company_website"),
                company_industry_id=company_industry_id,
                company_description=req_fields.get("company_description"),
            )
            db.session.add(company_tuple)
            db.session.flush()

            company_placement_data = CompanyPlacementData(company_id=getattr(company_tuple, "id"))
            db.session.add(company_placement_data)
            db.session.commit()

            role_claims = {"role": "company_hr"}
            expires_delta = timedelta(minutes=10)
            access_token = create_access_token(identity=str(getattr(company_hr, "id")), additional_claims=role_claims, expires_delta=expires_delta)

            payload = {
                "message": "Created company and hr user successfully"
            }

            response = make_response(jsonify(payload), 201)

            response.set_cookie(
                key='token',
                value=str(access_token),
                httponly=True,
                secure=True,
                samesite='Lax',
                path="/"
            )

            return response

        if (
            not (
                req_fields.get("student_roll_no") and req_fields.get("student_roll_no").strip()
            )
            or not (req_fields.get("branch") and req_fields.get("branch").strip())
            or not (req_fields.get("year_of_study"))
            or not (req_fields.get("current_cgpa"))
        ):
            return {
                "message": "Required fields are missing for Student role"
            }, 400

        existing_roll_no = db.session.scalars(db.select(Students.student_roll_no).filter_by(student_roll_no=req_fields.get("student_roll_no"))).first()

        if existing_roll_no:
            return {
                "message": "Student with the given roll number is already registered in the portal"
            }, 409
        
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

        branch_id = db.session.scalars(db.select(Branches.id).filter_by(branch_name=req_fields.get("branch"))).first()

        if not branch_id:
            return {
                "message": "Invalid Branch"
            }, 400

        student_tuple = Students(id=getattr(student_user, "id"), student_roll_no=req_fields.get("student_roll_no"), branch_id=branch_id, year_of_study=req_fields.get("year_of_study"), current_cgpa=req_fields.get("current_cgpa"))
        db.session.add(student_tuple)

        student_placement_status = StudentPlacementStatus(student_id=getattr(student_user, "id"))
        db.session.add(student_placement_status)

        db.session.commit()

        role_claims = {"role": "student"}
        expires_delta=timedelta(minutes=10)
        access_token = create_access_token(identity=str(getattr(student_user, "id")), additional_claims=role_claims ,expires_delta=expires_delta)

        response = make_response(jsonify({
            "message": "Student user created successfully"
        }), 201)

        response.set_cookie(
            key='token',
            value=str(access_token),
            httponly=True,
            samesite='Lax',
            secure=True,
            path="/"
        )
        return response

# /api/login
class LoginResource(Resource):
    def post(self):
        req_parser = reqparse.RequestParser()

        req_parser.add_argument("email", type=str, required=True, help="Email is required for Login", location="json")
        req_parser.add_argument("password", type=str, required=True, help="Password is required for Login", location="json")

        req_fields = req_parser.parse_args()

        user = db.session.scalars(db.select(PPAUsers).filter_by(email=req_fields.get("email"))).first()

        if user and bcrypt_instance.check_password_hash(getattr(user, "password_hash"), req_fields.get("password")):
            role_claims = {"role": getattr(user, "role")}
            expires_delta=timedelta(minutes=10)
            access_token = create_access_token(identity=str(getattr(user, "id")), additional_claims=role_claims, expires_delta=expires_delta)

            response = make_response(jsonify({
                "message": "User authenticated successfully",
                "role": str(getattr(user, "role"))
            }), 200)

            response.set_cookie(
                key='token',
                value=access_token,
                httponly=True,
                samesite='Lax',
                secure=True,
                path='/'
            )

            return response

        return {
            "message": "email and password combination incorrect"
        }, 401