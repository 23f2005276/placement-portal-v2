from functools import wraps
from flask_restful import Resource
from flask_jwt_extended import verify_jwt_in_request, get_jwt


# format is like this that you pass "admin", "student", "company_hr"
def check_rbac(*role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            role_claims = get_jwt()

            if role_claims.get("role") == role[0] or role_claims.get("role") == "admin":
                return fn(*args, **kwargs)

            return {
                "message": "You are not allowed to access that resources"
            }, 403

        return wrapper

    return decorator


class TestResource(Resource):
    def get(self):
        return {"message": "api is up and running"}, 200