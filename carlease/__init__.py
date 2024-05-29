import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_postgresql import PostgreSQL
from flask_bootstrap import Bootstrap
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a86fe86d8f95fe0cda48f9efb34c0424'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:sadcar@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
bootstrap = Bootstrap(app)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'timothyglazer@gmail.com'
app.config['MAIL_PASSWORD'] = 'udyavmfqcblhykqm'
mail = Mail(app)

SITE_KEY = '6Le6uOgpAAAAAOB8UclqUV0G9_1WI1ovxNDFVm-C'
SECRET_KEY = '6Le6uOgpAAAAAGSqKxIU5VkwB7rUmHpoe6gvmrpX'
VERIFY_URL= 'https://www.google.com/recaptcha/api/siteverify'

from carlease import routes

with app.app_context():
    db.drop_all()
    db.create_all()
    pass
