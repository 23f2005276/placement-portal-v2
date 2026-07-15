from flask import Blueprint
from flask_restful import Api
from ppa.routes.auth_routes import SignupResource, LoginResource, LogoutResource
from ppa.routes.admin_routes import (
    TestResource, TotalEntitiesResource, AllUsersResource, UpdateUserStatusResource,
    ApprovalResource, AdminInfoResource, UserInfoResource, AdminPlacementDrivesResource,
    AdminPlacementReportsResource
)
from ppa.routes.identity_routes import IdentityResource
from ppa.routes.company_routes import ProfileResource as CompanyProfileResource, CreatePlacementDriveResource, ActivePlacementDrivesResource, DriveApplicationsResource, CompanyStudentInfoResource, CompanyPlacementDrivesResource
from ppa.routes.student_routes import (
    StudentDashboardResource, StudentProfileResource, StudentResumeUploadResource,
    StudentResumeDownloadResource, StudentApplyDriveResource, StudentReportsResource,
    StudentDriveDetailsResource
)

api_bp = Blueprint("api", __name__)

api_instance = Api(api_bp)

# Adding identity resource below thsi*''/
api_instance.add_resource(IdentityResource, "/identity")

# Adding Auth resources
api_instance.add_resource(SignupResource, "/signup")
api_instance.add_resource(LoginResource, "/login")
api_instance.add_resource(LogoutResource, "/logout")

# Adding Admin resources
api_instance.add_resource(TestResource, "/test")
api_instance.add_resource(TotalEntitiesResource, "/admin/total")
api_instance.add_resource(AllUsersResource, "/admin/users")
api_instance.add_resource(UpdateUserStatusResource, "/admin/status")
api_instance.add_resource(ApprovalResource, "/admin/approval")
api_instance.add_resource(AdminInfoResource, "/admin/info")
api_instance.add_resource(UserInfoResource, "/admin/user")
api_instance.add_resource(AdminPlacementDrivesResource, "/admin/drives")
api_instance.add_resource(AdminPlacementReportsResource, "/admin/placement_reports")

api_instance.add_resource(CompanyProfileResource, "/company/profile")
api_instance.add_resource(CreatePlacementDriveResource, "/company_hr/create")
api_instance.add_resource(ActivePlacementDrivesResource, "/company_hr/active_drives")
api_instance.add_resource(DriveApplicationsResource, "/company_hr/drive/applications")
api_instance.add_resource(CompanyStudentInfoResource, "/company_hr/student")
api_instance.add_resource(CompanyPlacementDrivesResource, "/company_hr/drives")
api_instance.add_resource(StudentDashboardResource, "/student/dashboard")
api_instance.add_resource(StudentProfileResource, "/student/profile")
api_instance.add_resource(StudentResumeUploadResource, "/student/resume/upload")
api_instance.add_resource(StudentResumeDownloadResource, "/student/resume/download")
api_instance.add_resource(StudentApplyDriveResource, "/student/apply")
api_instance.add_resource(StudentReportsResource, "/student/reports")
api_instance.add_resource(StudentDriveDetailsResource, "/student/drive")