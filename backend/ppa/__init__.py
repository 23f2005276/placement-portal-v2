from dotenv import load_dotenv
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from sqlalchemy.orm import DeclarativeBase
load_dotenv()

app = Flask(__name__)

app.secret_key = "a4ac2e4b5282d0db8d43f2149109eacd30ea618890c3aa2e" # generated this using os.urandom(24).hex()

# during production, obviously this has to be moved to the .env, this will be used for creating jwt signatures

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY") # for signing jwt tokens (i.e. authentication and authorization)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") # for csrf tokens

jwt_manager_instance = JWTManager(app)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app, model_class=Base)

api = Api(app)

bcrypt_instance = Bcrypt(app)

# importing routes and models

from ppa import models  # noqa: E402, F401

# adding api resources below this