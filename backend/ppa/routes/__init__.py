from flask import Blueprint
from flask_restful import Api
from ppa.routes.auth_routes import SignupResource, LoginResource

api_bp = Blueprint("api", __name__)

api_instance = Api(api_bp)

api_instance.add_resource(SignupResource, "/signup")
api_instance.add_resource(LoginResource, "/login")