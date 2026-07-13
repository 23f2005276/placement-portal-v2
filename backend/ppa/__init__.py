from dotenv import load_dotenv
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from sqlalchemy.orm import DeclarativeBase
from ppa.extensions import db, bcrypt_instance

# models and routes
from ppa import models  # noqa: E402, F401
from ppa.routes import api_bp  # noqa: E402, F401

load_dotenv()

app = Flask(__name__) 

# during production, obviously this has to be moved to the .env, this will be used for creating jwt signatures

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["JWT_SECRET_KEY"] = os.getenv(
    "JWT_SECRET_KEY"
)  # for signing jwt tokens (i.e. authentication and authorization)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")  # for csrf tokens and dependencies needing secret key
app.config["JWT_TOKEN_LOCATION"] = os.getenv("JWT_TOKEN_LOCATION")
app.config["PROPAGATE_EXCEPTIONS"] = os.getenv("PROPAGATE_EXCEPTIONS") # for propogating exceptions from the flask_restful to flask_jwt_extended
app.config["JWT_ACCESS_COOKIE_NAME"] = os.getenv("JWT_ACCESS_COOKIE_NAME") # looks for cookie with this key value in the incoming requests
# Convert environment variable string to actual Boolean.
# In Python, bool("False") evaluates to True because it is a non-empty string. 
# Therefore, we explicitly compare it against the string "True".
app.config["JWT_COOKIE_CSRF_PROTECT"] = os.getenv("JWT_COOKIE_CSRF_PROTECT") == "True"

jwt_manager_instance = JWTManager(app)


class Base(DeclarativeBase):
    pass


db.init_app(app)
bcrypt_instance.init_app(app)
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "http://localhost:5173", 
                "http://localhost:5174",
                "http://localhost:5175",
                "http://127.0.0.1:5173",
                "http://127.0.0.1:5174",
                "http://127.0.0.1:5175"
            ]
        }
    },
    supports_credentials=True
)

app.register_blueprint(api_bp, url_prefix="/api")
