from flask import Blueprint
from flask_restful import Api
from ppa.routes.auth_routes import SignupResource, LoginResource
from ppa.routes.admin_routes import TestResource, TotalEntitiesResource, AllUsersResource, UpdateUserStatusResource, ApprovalResource
from ppa.routes.identity_routes import IdentityResource

api_bp = Blueprint("api", __name__)

api_instance = Api(api_bp)

# Adding identity resource below thsi*''/
api_instance.add_resource(IdentityResource, "/identity")

# Adding Auth resources
api_instance.add_resource(SignupResource, "/signup")
api_instance.add_resource(LoginResource, "/login")

# Adding Admin resources
api_instance.add_resource(TestResource, "/test")
api_instance.add_resource(TotalEntitiesResource, "/admin/total")
api_instance.add_resource(AllUsersResource, "/admin/users")
api_instance.add_resource(UpdateUserStatusResource, "/admin/status")
api_instance.add_resource(ApprovalResource, "/admin/approval")