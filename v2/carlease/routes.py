from flask import render_template, request, flash, redirect, url_for, Request, session, abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import requests
from carlease import app, db, bcrypt, bootstrap, mail, SITE_KEY, SECRET_KEY, VERIFY_URL
from carlease.forms import RegistrationForm, LoginForm, VerifyForm, NotificationForm, RequestResetForm, ResetPasswordForm, AppointmentForm
from carlease.models import User, Car, User_Verified, Appointment
from carlease.decorators import admin_required
from carlease.dao import UserDAO, CarDAO, User_VerifiedDAO
import os

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET','POST'])
def account():
    return render_template('account.html')

@app.route("/verified", methods=['GET', 'POST'])
@login_required
def verification():
    user_info = User_Verified.query.filter_by(user_id=current_user.id).first()
    
    form = VerifyForm()
    
    if user_info:
        print(f"Phone: {user_info.phone}, Address: {user_info.address}")
        return render_template('verified.html', user_info=user_info, editable=False)
    else:
        if form.validate_on_submit():
            new_user_info = User_Verified(

                phone=form.phone.data,
                address=form.address.data
            )
            db.session.add(new_user_info)
            db.session.commit()
            flash('Your account has been verified!', 'success')
            return redirect(url_for('account'))
    
    return render_template('verified.html', form=form, editable=True, user_info=user_info)

# <!----------------------------------------------!---------------------------------------------->
# Routes to account components
"""@app.route("/verification")
@login_required
def verification():
    return render_template('account-components/verification.html')"""

@app.route("/account-security")
@login_required
def accSecurity():
    return render_template('account-components/security.html')

@app.route('/delete_account', methods=['GET','POST'])
@login_required
def deleteAcc():
    if request.method == 'POST':
        user = User.query.filter_by(id=current_user.id).first()
        verified = User_Verified.query.filter_by(user_id=current_user.id).first()
        if user and verified:
            db.session.delete(user)
            db.session.delete(verified)
            db.session.commit()
            logout_user()
            flash('Your account has been deleted successfully.', 'success')
            return redirect(url_for('register'))
        elif user:
            db.session.delete(user)
            db.session.commit()
            logout_user()
            flash('Your account has been deleted successfully.', 'success')
            return redirect(url_for('register'))            
        else:
            flash('Account deletion failed. User not found.', 'danger')
            return redirect(url_for('account'))
    return render_template('account-components/delete_account.html')

@app.route("/notifications", methods=['GET', 'POST'])
@login_required
def notifications():
    form = NotificationForm()
    if form.validate_on_submit():
        # Handle form submission and save preferences
        promotional_emails = form.promotional_emails.data
        no_notifications = form.no_notifications.data
        flash('Your preferences have been updated.', 'success')
        return redirect(url_for('account'))
    return render_template('account-components/notifications.html', form=form)

#RESET PW BEGIN

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                  sender='noreply@demo.com', 
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_request', token=token, _external=True)}

If you did not make this request, simply ignore this email
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with insctructions to restter your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated, you are now able to Login!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

#RESET PW END

@app.route("/registration", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        recaptcha_response = request.form.get('g-recaptcha-response')
        if not recaptcha_response:
            flash('reCAPTCHA verification failed. Please try again.', 'danger')
            return redirect(url_for('register'))

        data = {
            'secret': SITE_KEY,
            'response': recaptcha_response
        }
        verify_response = requests.post(VERIFY_URL, data=data).json()

        if verify_response.get('success') :
            flash('Captcha failed, try to register again')
            return redirect(url_for('register'))

        if current_user.is_authenticated:
            return redirect(url_for('home'))

        form = RegistrationForm()
        if form.validate_on_submit():
            UserDAO.create_user(form.full_name.data, form.email.data, form.password.data)
            flash('Your account has been created!', 'success')
            return redirect(url_for('login'))

        return render_template('registration.html', title='Register', form=form, SITE_KEY=SITE_KEY)

    form = RegistrationForm()
    return render_template('registration.html', title='Register', form=form, SITE_KEY=SITE_KEY)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = UserDAO.get_user_by_email(form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/admin")
@login_required
@admin_required
def admin():
    users = User.query.all()
    return render_template('admin.html', users=users)


@app.route("/product")
def products():
    cars = Car.query.order_by(Car.id.desc())
    return render_template('product.html', cars = cars)

# <!----------------------------------------------!---------------------------------------------->
# Setting up appointment booking
@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    form = AppointmentForm()
    if form.validate_on_submit():
        appointment = Appointment(
            name=form.name.data,
            email=form.email.data,
            date=form.date.data
        )
        db.session.add(appointment)
        db.session.commit()

        send_confirmation_email(appointment)

        flash('Appointment booked successfully. Check your email for confirmation.')
        return redirect(url_for('index'))
    return render_template('book_appointment.html', form=form)

def send_confirmation_email(appointment):
    msg = Message('Appointment Confirmation', sender='carlease4@gmail.com', recipients=[appointment.email])
    msg.body = f"Hi {appointment.name},\n\nYour appointment on {appointment.date.strftime('%Y-%m-%d')} has been successfully booked.\n\nThank you!"
    mail.send(msg)