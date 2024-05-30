from carlease import db, login_manager, app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, current_user
from wtforms import StringField, DateField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# <!----------------------------------------------!---------------------------------------------->

# Add User table to database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String(120), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    date_creation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    verified_info = db.relationship('User_Verified', backref='private', lazy=True)
    email_verified = db.Column(db.Boolean, default=False)

#RESET PW BEGIN
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    def get_verification_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    @staticmethod
    def verify_verification_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
# Email verification end
#RESET PW END

# <!----------------------------------------------!---------------------------------------------->

# Add Login Attempts to database
class LoginAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    success = db.Column(db.Boolean, nullable=False, default=False)

# <!----------------------------------------------!---------------------------------------------->

# Email verification
class EmailVerificationToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(120), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
# <!----------------------------------------------!---------------------------------------------->
def __repr__(self):
        return f"User('{self.email}', '{self.id}', '{self.phone}')"
    
# <!----------------------------------------------!---------------------------------------------->

# Add car table to database
class Car(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    model= db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    license_plate = db.Column(db.String(60), nullable=False)
    car_picture = db.Column(db.String(20), nullable=False, default='default.jpg')
    kilometers =db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    #rents = db.relationship('Reservation', backref="car_lease", lazy=True)

    def __repr__(self):
        return f"Car('{self.model}', '{self.car_picture}', '{self.color}')"

# <!----------------------------------------------!---------------------------------------------->

# Add verified users to database
class User_Verified(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, phone, address):
        self.phone = phone
        self.address = address
        self.user_id = current_user.id

    def __repr__(self):
        return f"User('{self.phone}', '{self.user_id}', {self.address}')"
    
# <!----------------------------------------------!---------------------------------------------->

# Add appointment details to database    
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)

# <!----------------------------------------------!---------------------------------------------->

# Add password reset details to database
class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)