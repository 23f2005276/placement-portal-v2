import os
from flask import request, current_app, send_from_directory
from flask_restful import Resource, reqparse
from datetime import datetime
from sqlalchemy import func
from ppa.extensions import db, bcrypt_instance
from ppa.routes.check_rbac import check_jwt_and_role
from ppa.models import (
    Students, PPAUsers, Branches, PlacementDrives, StudentApplications,
    EligibleBranches, Skills, StudentSkills, StudentApplicationStatus,
    Company, StudentPlacementStatus, StudentPlacementState
)

class StudentDashboardResource(Resource):
    @check_jwt_and_role("student")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True, location="args")
        args = parser.parse_args()

        student_stmt = (
            db.select(Students, PPAUsers, Branches)
            .join(PPAUsers, Students.id == PPAUsers.id)
            .join(Branches, Students.branch_id == Branches.id)
            .where(Students.id == args.get("user_id"))
        )
        res = db.session.execute(student_stmt).first()
        if not res:
            return {"message": "Student not found"}, 404
        student, user, branch = res

        eligible_stmt = (
            db.select(PlacementDrives, Company)
            .join(Company, PlacementDrives.company_id == Company.id)
            .join(EligibleBranches, PlacementDrives.id == EligibleBranches.placement_drive_id)
            .where(EligibleBranches.branch_id == getattr(student, "branch_id"))
            .where(PlacementDrives.status == "approved")
        )
        drives_res = db.session.execute(eligible_stmt).all()

        now = datetime.now()
        eligible_drives = []
        for drive, comp in drives_res:
            deadline = getattr(drive, "application_deadline")
            if deadline >= now:
                applied = db.session.scalar(
                    db.select(StudentApplications)
                    .where(StudentApplications.student_id == getattr(student, "id"))
                    .where(StudentApplications.placement_id == getattr(drive, "id"))
                ) is not None

                if not applied:
                    eligible_drives.append({
                        "id": getattr(drive, "id"),
                        "company_name": getattr(comp, "company_name"),
                        "job_title": getattr(drive, "job_title"),
                        "salary_package": getattr(drive, "salary_package"),
                        "location": getattr(drive, "location"),
                        "application_deadline": deadline.isoformat(),
                        "applied": False
                    })

        applied_stmt = (
            db.select(StudentApplications, PlacementDrives, Company)
            .join(PlacementDrives, StudentApplications.placement_id == PlacementDrives.id)
            .join(Company, PlacementDrives.company_id == Company.id)
            .where(StudentApplications.student_id == getattr(student, "id"))
        )
        apps_res = db.session.execute(applied_stmt).all()

        my_applications = []
        for app, drive, comp in apps_res:
            my_applications.append({
                "id": getattr(app, "id"),
                "company_name": getattr(comp, "company_name"),
                "job_title": getattr(drive, "job_title"),
                "status": getattr(app, "status"),
                "date_applied": "N/A"
            })

        return {
            "student_info": {
                "id": getattr(student, "id"),
                "full_name": getattr(user, "full_name"),
                "branch_name": getattr(branch, "branch_name"),
                "current_cgpa": float(getattr(student, "current_cgpa")),
                "resume_file_url": getattr(student, "resume_file_url")
            },
            "eligible_drives": eligible_drives,
            "my_applications": my_applications
        }, 200

class StudentProfileResource(Resource):
    @check_jwt_and_role("student")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True, location="args")
        args = parser.parse_args()

        student_stmt = (
            db.select(Students, PPAUsers, Branches)
            .join(PPAUsers, Students.id == PPAUsers.id)
            .join(Branches, Students.branch_id == Branches.id)
            .where(Students.id == args.get("user_id"))
        )
        res = db.session.execute(student_stmt).first()
        if not res:
            return {"message": "Student not found"}, 404
        student, user, branch = res

        skills_stmt = (
            db.select(Skills)
            .join(StudentSkills, Skills.id == StudentSkills.skill_id)
            .where(StudentSkills.student_id == getattr(student, "id"))
        )
        skills_res = db.session.scalars(skills_stmt).all()
        skills_list = [getattr(s, "skill_name") for s in skills_res]

        return {
            "id": getattr(student, "id"),
            "full_name": getattr(user, "full_name"),
            "email": getattr(user, "email"),
            "student_roll_no": getattr(student, "student_roll_no"),
            "branch": getattr(branch, "branch_name"),
            "year_of_study": getattr(student, "year_of_study"),
            "current_cgpa": float(getattr(student, "current_cgpa")),
            "resume_file_url": getattr(student, "resume_file_url"),
            "skills": skills_list
        }, 200

    @check_jwt_and_role("student")
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True, location="json")
        parser.add_argument("full_name", type=str, required=True, location="json")
        parser.add_argument("email", type=str, required=True, location="json")
        parser.add_argument("password", type=str, required=False, location="json")
        parser.add_argument("skills", type=list, required=False, location="json")
        args = parser.parse_args()

        user = db.session.scalar(db.select(PPAUsers).where(PPAUsers.id == args.get("user_id")))
        if not user:
            return {"message": "User not found"}, 404

        existing_user = db.session.scalar(
            db.select(PPAUsers)
            .where(PPAUsers.email == args.get("email"))
            .where(PPAUsers.id != args.get("user_id"))
        )
        if existing_user:
            return {"message": "Email is already in use"}, 400

        user.full_name = args.get("full_name")
        user.email = args.get("email")

        password = args.get("password")
        if password and password.strip():
            user.password_hash = bcrypt_instance.generate_password_hash(password.strip()).decode("utf-8")

        skills = args.get("skills")
        if skills is not None:
            existing_skills_stmt = (
                db.select(StudentSkills, Skills)
                .join(Skills, StudentSkills.skill_id == Skills.id)
                .where(StudentSkills.student_id == args.get("user_id"))
            )
            existing_res = db.session.execute(existing_skills_stmt).all()

            existing_skills_map = {}
            for rel, sk in existing_res:
                existing_skills_map[getattr(sk, "skill_name")] = rel

            new_skills_set = {s.strip() for s in skills if s.strip()}
            new_skills_set_lower = {s.lower() for s in new_skills_set}

            for skill_name in new_skills_set:
                has_relation = False
                for old_name in existing_skills_map.keys():
                    if old_name.lower() == skill_name.lower():
                        has_relation = True
                        break

                if not has_relation:
                    sk = db.session.scalar(
                        db.select(Skills).where(func.lower(Skills.skill_name) == func.lower(skill_name))
                    )
                    if not sk:
                        sk = Skills(skill_name=skill_name)
                        db.session.add(sk)
                        db.session.flush()

                    rel = StudentSkills(student_id=args.get("user_id"), skill_id=getattr(sk, "id"))
                    db.session.add(rel)

            for old_name, rel in existing_skills_map.items():
                if old_name.lower() not in new_skills_set_lower:
                    db.session.delete(rel)

        db.session.commit()
        return {"message": "Profile updated successfully"}, 200

class StudentResumeUploadResource(Resource):
    @check_jwt_and_role("student")
    def post(self):
        user_id = request.form.get("user_id")
        if not user_id:
            return {"message": "User ID is required"}, 400

        student = db.session.scalar(db.select(Students).where(Students.id == int(user_id)))
        if not student:
            return {"message": "Student not found"}, 404

        if "file" not in request.files:
            return {"message": "No file uploaded"}, 400

        file = request.files["file"]
        if file.filename == "":
            return {"message": "Empty file name"}, 400

        if not file.filename.lower().endswith(".pdf"):
            return {"message": "Only PDF files are allowed"}, 400

        upload_dir = os.path.join(current_app.root_path, "..", "files")
        os.makedirs(upload_dir, exist_ok=True)

        filename = f"resume_student_{user_id}.pdf"
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)

        student.resume_file_url = filename
        db.session.commit()

        return {"message": "Resume uploaded successfully", "filename": filename}, 200

class StudentResumeDownloadResource(Resource):
    @check_jwt_and_role("student")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True, location="args")
        parser.add_argument("student_id", type=int, required=True, location="args")
        args = parser.parse_args()

        student = db.session.scalar(db.select(Students).where(Students.id == args.get("student_id")))
        if not student:
            return {"message": "Student not found"}, 404

        if not getattr(student, "resume_file_url"):
            return {"message": "Resume file not found"}, 404

        upload_dir = os.path.join(current_app.root_path, "..", "files")
        return send_from_directory(upload_dir, getattr(student, "resume_file_url"))

class StudentApplyDriveResource(Resource):
    @check_jwt_and_role("student")
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True, location="json")
        parser.add_argument("drive_id", type=int, required=True, location="json")
        args = parser.parse_args()

        student = db.session.scalar(db.select(Students).where(Students.id == args.get("user_id")))
        if not student:
            return {"message": "Student not found"}, 404

        drive = db.session.scalar(db.select(PlacementDrives).where(PlacementDrives.id == args.get("drive_id")))
        if not drive:
            return {"message": "Placement drive not found"}, 404

        if getattr(drive, "status") != "approved":
            return {"message": "Applications are not allowed for this drive"}, 400

        now = datetime.now()
        if getattr(drive, "application_deadline") < now:
            return {"message": "The application deadline has passed"}, 400

        eligible_branch = db.session.scalar(
            db.select(EligibleBranches)
            .where(EligibleBranches.placement_drive_id == args.get("drive_id"))
            .where(EligibleBranches.branch_id == getattr(student, "branch_id"))
        )
        if not eligible_branch:
            return {"message": "You are not eligible for this branch"}, 400

        existing = db.session.scalar(
            db.select(StudentApplications)
            .where(StudentApplications.student_id == args.get("user_id"))
            .where(StudentApplications.placement_id == args.get("drive_id"))
        )
        if existing:
            return {"message": "You have already applied to this drive"}, 400

        app = StudentApplications(
            student_id=args.get("user_id"),
            placement_id=args.get("drive_id"),
            status=StudentApplicationStatus.PENDING_STATUS
        )
        db.session.add(app)
        db.session.commit()

        return {"message": "Applied successfully"}, 201

class StudentReportsResource(Resource):
    @check_jwt_and_role("student")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True, location="args")
        args = parser.parse_args()

        apps = db.session.scalars(
            db.select(StudentApplications).where(StudentApplications.student_id == args.get("user_id"))
        ).all()

        total = len(apps)
        shortlisted = sum(1 for app in apps if getattr(app, "status") == "shortlisted")
        placed = sum(1 for app in apps if getattr(app, "status") == "selected")
        rejected = sum(1 for app in apps if getattr(app, "status") == "rejected")

        applied_stmt = (
            db.select(StudentApplications, PlacementDrives, Company)
            .join(PlacementDrives, StudentApplications.placement_id == PlacementDrives.id)
            .join(Company, PlacementDrives.company_id == Company.id)
            .where(StudentApplications.student_id == args.get("user_id"))
        )
        apps_res = db.session.execute(applied_stmt).all()

        my_applications = []
        for app, drive, comp in apps_res:
            my_applications.append({
                "id": getattr(app, "id"),
                "company_name": getattr(comp, "company_name"),
                "job_title": getattr(drive, "job_title"),
                "status": getattr(app, "status"),
                "date_applied": "N/A"
            })

        return {
            "total_applied": total,
            "shortlisted": shortlisted,
            "placed": placed,
            "rejected": rejected,
            "applications_history": my_applications
        }, 200

class StudentDriveDetailsResource(Resource):
    @check_jwt_and_role("student")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True, location="args")
        parser.add_argument("drive_id", type=int, required=True, location="args")
        args = parser.parse_args()

        student = db.session.scalar(db.select(Students).where(Students.id == args.get("user_id")))
        if not student:
            return {"message": "Student not found"}, 404

        drive_stmt = (
            db.select(PlacementDrives, Company)
            .join(Company, PlacementDrives.company_id == Company.id)
            .where(PlacementDrives.id == args.get("drive_id"))
        )
        res = db.session.execute(drive_stmt).first()
        if not res:
            return {"message": "Placement drive not found"}, 404
        drive, company = res

        branches_stmt = (
            db.select(Branches)
            .join(EligibleBranches, Branches.id == EligibleBranches.branch_id)
            .where(EligibleBranches.placement_drive_id == args.get("drive_id"))
        )
        branches = db.session.scalars(branches_stmt).all()
        branch_names = [getattr(b, "branch_name") for b in branches]

        applied = db.session.scalar(
            db.select(StudentApplications)
            .where(StudentApplications.student_id == args.get("user_id"))
            .where(StudentApplications.placement_id == args.get("drive_id"))
        ) is not None

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
            "eligible_branches": branch_names,
            "applied": applied
        }, 200
