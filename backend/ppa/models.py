from sqlalchemy.orm import Mapped, mapped_column, relationship
from ppa import db
from enum import Enum
from datetime import datetime

'''
mapped_column me either we pass primary_key, String/Integer ki limit, nullable, unique, default, back_populates for 
relationships
'''

class PPAUsersRole(Enum):
    ADMIN_ROLE = "admin"
    STUDENT_ROLE = "student"
    COMPANY_HR_ROLE = "company_hr"

class PPAUsers(db.Model):
    __tablename__ = "ppa_users"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(db.String(50), nullable=False)
    email: Mapped[str] = mapped_column(db.String(150), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(db.String(255), nullable=False)
    role: Mapped[PPAUsersRole] = mapped_column(db.Enum(PPAUsersRole), nullable=False, default=PPAUsersRole.STUDENT_ROLE)

class UserStatus(Enum):
    APPROVED_ROLE = "approved"
    BLACKLISTED_ROLE = "blacklisted"
    PENDING_ROLE = "pending"

'''
- student status will be inme se koi ek, also creating the branch master table above the student makes sense, usse 
- when we create foreign relation in the Students then Branches table me certain branch ke naa hone ke wajah se application doesn't crash
- lafda ye hai ki if we initialize foreign key in the Branches table then the branch_id should be present in one of the rows in the students table, or else foreign key ka relationship tut jaayega 
'''

class Branches(db.Model):
    __tablename__ = "branches"
    id: Mapped[int] = mapped_column(primary_key=True)
    branch_name: Mapped[str] = mapped_column(db.String(100), nullable=False ,unique=True)
    students: Mapped[list["Students"]] = relationship(back_populates="branch_name")

class Skills(db.Model):
    __tablename__ = "skills"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    skill_name: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)

class Students(db.Model):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("ppa_users.id"), primary_key=True)
    student_roll_no: Mapped[str] = mapped_column(db.String(50), nullable=False, unique=True)
    branch_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("branches.id") ,nullable=False)
    year_of_study: Mapped[int] = mapped_column(db.Integer, nullable=False)
    current_cgpa: Mapped[float] = mapped_column(db.Numeric(4, 2), nullable=False)
    resume_file_url: Mapped[str] = mapped_column(db.String(500))
    status: Mapped[UserStatus] = mapped_column(db.Enum(UserStatus), nullable=False, default=UserStatus.PENDING_ROLE)
    branch_name: Mapped["Branches"] = relationship(back_populates="students")
    skills: Mapped[list["StudentSkills"]] = relationship()
    drives_applied: Mapped[list["StudentApplications"]] = relationship() 

'''
- we're not asking for the skills list anyways during signup, we'll ask for the skills credentials once the student logs into the portal
- another gotcha in the code is that db.Integer positional argument comes before the db.ForeignKey one
'''

class StudentSkills(db.Model):
    __tablename__ = "student_skills"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    skill_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("skills.id"), nullable=False)

'''
while creating new company during signup we have to create the hr user and then create this company
'''

class IndustryTypes(db.Model):
    __tablename__ = "industry_types"
    id: Mapped[int] = mapped_column(primary_key=True)
    industry_name: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)

class Company(db.Model):
    __tablename__ = "company"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    company_hr_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("ppa_users.id"), nullable=False, unique=True)
    company_name: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)
    company_website: Mapped[str] = mapped_column(db.String(500), nullable=False, unique=True)
    company_industry_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("industry_types.id"), nullable=False)
    company_description: Mapped[str] = mapped_column(db.Text, nullable=False)
    status: Mapped[UserStatus] = mapped_column(db.Enum(UserStatus), nullable=False, default=UserStatus.PENDING_ROLE)
    placement_drives: Mapped[list["PlacementDrives"]] = relationship()

class PlacementStatus(Enum):
    APPROVED_STATUS = "approved"
    PENDING_STATUS = "pending"
    CLOSED_STATUS = "closed"
    REJECTED_STATUS = "rejected"

class PlacementDrives(db.Model):
    __tablename__ = "placement_drives"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    job_title: Mapped[str] = mapped_column(db.String(150), nullable=False)
    job_description: Mapped[str] = mapped_column(db.Text, nullable=False)
    min_cgpa: Mapped[float] = mapped_column(db.Numeric(4,2), nullable=False)
    eligible_year: Mapped[int] = mapped_column(db.Integer, nullable=False) # can use pydantic for integrity constraints like these or tableargs from sqlalchemy, but mehhhh who cares for MAD2 lol
    location: Mapped[str] = mapped_column(db.String(100), nullable=False)
    salary_package: Mapped[int] = mapped_column(db.Integer, nullable=False)
    application_deadline: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)
    status: Mapped[PlacementStatus] = mapped_column(db.Enum(PlacementStatus), nullable=False, default=PlacementStatus.PENDING_STATUS)
    students_applied: Mapped[list["StudentApplications"]] = relationship()

'''
for creating application deadline in the backend, we'll use the datetime object only from the datetime package, something like this :- 

from datetime import datetime, timezone, timedelta

today = datetime.now(timezone.utc)

deadline_tonight = today.replace(hour=23, minute=59, second=0, microsecond=0)

future_date = today + timedelta(days=5)
deadline_future = future_date.replace(hour=23, minute=59, second=0, microsecond=0)
'''

class EligibleBranches(db.Model):
    __tablename__ = "eligible_branches"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    placement_drive_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("placement_drives.id"), nullable=False)
    branch_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("branches.id"), nullable=False)

class StudentApplicationStatus(Enum):
    PENDING_STATUS = "pending"
    SHORTLISTED_STATUS = "shortlisted"
    SELECTED_STATUS = "selected"
    REJECTED_STATUS = "rejected"

class StudentApplications(db.Model):
    __tablename__ = "student_applications"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    placement_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("placement_drives.id"), nullable=False)
    status: Mapped[StudentApplicationStatus] = mapped_column(db.Enum(StudentApplicationStatus), nullable=False, default=StudentApplicationStatus.PENDING_STATUS)