from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt 

class IdentityResource(Resource):
    @jwt_required()
    def get(self):
        jwt = get_jwt()

        role = jwt.get("role")

        return {
            "message": "User Identified successfully",
            "role": role
        }, 200