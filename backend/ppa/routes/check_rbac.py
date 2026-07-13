from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt

# format is like this that you pass "admin", "student", "company_hr"
def check_jwt_and_role(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            jwt = get_jwt()

            role_claims = str(jwt.get("role")) # btw whatever that is passed as the additional_claims is the python dictionary that we get in return along with an additional attribute called sub (which is the indentity of the jwt that we assigned initially while signing the jwt)

            if role_claims in roles or role_claims == "admin":
                return fn(*args, **kwargs)
            
            return {
                "message": "You're not allowed to access that resource"
            }, 403 # btw no need to jsonify, flask_restful will intercept it and jsonify it 
        return wrapper
    return decorator          