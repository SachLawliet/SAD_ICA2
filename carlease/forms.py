from flask import flash
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from carlease.models import User, User_Verified
from datetime import date

# <!----------------------------------------------!---------------------------------------------->

# Registration Form
class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name',
                            validators=[DataRequired(), Length(max=120)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8, max=16)])
    confirm_password = PasswordField('Confirm Password',
                             validators=[DataRequired(), Length(min=8, max=16), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Incorrect details ')
        
# <!----------------------------------------------!---------------------------------------------->

# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8, max=16)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class NotificationForm(FlaskForm):
    promotional_emails = BooleanField('Receive promotional emails')
    no_notifications = BooleanField('Do not receive any emails or notifications')
    submit = SubmitField('Save Preferences')


class VerifyForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired(), Length(max=64)])
    submit = SubmitField('Get Verified')

    def validate_phone(self, phone):
        user = User_Verified.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('This phone number is already linked to an account')
        
# <!----------------------------------------------!---------------------------------------------->

#RESET PW BEGIN
class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8, max=32)])
    confirm_password = PasswordField('Confirm Password',
                             validators=[DataRequired(), Length(min=8, max=32), EqualTo('password')])
    submit = SubmitField('Reset Password')
#PASSWORD RESET END

# <!----------------------------------------------!---------------------------------------------->

# Appointment form
class AppointmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    date = DateField('Appointment Date', format='%Y-%m-%d', validators=[DataRequired()], id='appointment_date')
    city = SelectField('City', choices=[('Praha', 'Praha'), ('Ostrava', 'Ostrava'), ('Brno', 'Brno'), ('Karlovy Vary', 'Karlovy Vary')], validators=[DataRequired()])
