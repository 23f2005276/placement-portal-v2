from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import DeclarativeBase

app = Flask(__name__)

app.secret_key = "a4ac2e4b5282d0db8d43f2149109eacd30ea618890c3aa2e" # generated this using os.urandom(24).hex()

# during production, obviously this has to be moved to the .env, this will be used for creating jwt signatures

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PPA.db'

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app, model_class=Base)

api = Api(app)

bcrypt_instance = Bcrypt(app)

# importing routes and models

from ppa import models

# adding api resources below this