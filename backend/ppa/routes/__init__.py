from flask import Blueprint
from flask_restful import Api
from ppa.routes.auth_routes import SignupResource, LoginResource
from ppa.routes.admin_routes import TestResource
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