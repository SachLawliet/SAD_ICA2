import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a86fe86d8f95fe0cda48f9efb34c0424'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



SITE_KEY = os.environ.get('SITE_KEY')
SECRET_KEY_RECAPTCHA = os.environ.get('SECRET_KEY_RECAPTCHA')
VERIFY_URL= 'https://www.google.com/recaptcha/api/siteverify'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
bootstrap = Bootstrap(app)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
mail = Mail(app)


from carlease import routes

with app.app_context():
    # db.drop_all()
    db.create_all()
    pass
