from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from carlease.models import User, User_Verified

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
            raise ValidationError('That email is already linked to an account, try to login ')


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

#RESET PW BEGIN

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError('No account with this email were found. Register!')
        

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8, max=32)])
    confirm_password = PasswordField('Confirm Password',
                             validators=[DataRequired(), Length(min=8, max=32), EqualTo('password')])
    submit = SubmitField('Reset Password')

#PASSWORD RESET END