from flask import render_template, request, flash, redirect, url_for, Request, session, abort, make_response
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer as Serializer
import requests
from carlease import app, db, bcrypt, bootstrap, mail, SITE_KEY, SECRET_KEY, VERIFY_URL
from carlease.forms import RegistrationForm, LoginForm, VerifyForm, NotificationForm, RequestResetForm, ResetPasswordForm, AppointmentForm
from carlease.models import User, Car, User_Verified, Appointment, PasswordResetToken
from carlease.decorators import admin_required
from carlease.dao import UserDAO, CarDAO, User_VerifiedDAO
from datetime import datetime, timedelta
import os
import secrets
from sqlalchemy import func
import logging

# <!----------------------------------------------!---------------------------------------------->

# Setting up logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# <!----------------------------------------------!---------------------------------------------->

# Route for home page
@app.route("/")
@app.route("/home")
def home():
    logger.info('Home page accessed')
    return render_template('index.html')


# <!----------------------------------------------!---------------------------------------------->
@app.route("/registration", methods=['GET', 'POST'])
def register():
    logger.info('Registration page accessed')
    if request.method == 'POST':
        recaptcha_response = request.form.get('g-recaptcha-response')
        if not recaptcha_response:
            logger.warning('reCAPTCHA verification failed')
            flash('reCAPTCHA verification failed. Please try again.', 'danger')
            return redirect(url_for('register'))

        data = {
            'secret': os.environ.get('6Le6uOgpAAAAAOB8UclqUV0G9_1WI1ovxNDFVm-C'),
            'response': recaptcha_response
        }
        verify_response = requests.post(VERIFY_URL, data=data).json()

        if verify_response.get('success') :
            logger.warning('Captcha failed')
            flash('Captcha failed, try to register again')
            return redirect(url_for('register'))

        if current_user.is_authenticated:
            return redirect(url_for('home'))

        form = RegistrationForm()
        if form.validate_on_submit():
            UserDAO.create_user(form.full_name.data, form.email.data, form.password.data)
            logger.info('New user registered: %s', form.email.data)
            flash('Your account has been created!', 'success')
            return redirect(url_for('login'))

        return render_template('registration.html', title='Register', form=form, SITE_KEY=SITE_KEY)

    form = RegistrationForm()
    return render_template('registration.html', title='Register', form=form, SITE_KEY=SITE_KEY)
# <!----------------------------------------------!---------------------------------------------->

MAX_LOGIN_ATTEMPTS = 5
BLOCK_DURATION_SECONDS = 30

@app.route("/login", methods=['GET', 'POST'])
def login():
    logger.info('Login page accessed')
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = UserDAO.get_user_by_email(form.email.data)
        
        # Check if the user is currently blocked
        if 'login_cooldown_timestamp' in session:
            cooldown_end = datetime.strptime(session['login_cooldown_timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            if datetime.utcnow() < cooldown_end:
                flash('Too many login attempts. Please try again later.', 'danger')
                return render_template('login.html', title='Login', form=form)
            else:
                # Cooldown period has passed, reset attempts
                session.pop('login_cooldown_timestamp', None)
                session.pop('login_attempts', None)
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            logger.info('User logged in: %s', form.email.data)
            session.pop('login_attempts', None)  # Reset login attempts on successful login
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            # Increment login attempts
            email = form.email.data
            if 'login_attempts' in session:
                session['login_attempts'] += 1
            else:
                session['login_attempts'] = 1
            
            if session['login_attempts'] >= MAX_LOGIN_ATTEMPTS:
                logger.warning('Login blocked for email: %s', email)
                flash('Too many login attempts. Please try again later.', 'danger')
                session['login_cooldown_timestamp'] = (datetime.utcnow() + timedelta(seconds=BLOCK_DURATION_SECONDS)).strftime('%Y-%m-%d %H:%M:%S.%f')
            else:
                logger.warning('Login failed for email: %s', email)
                flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html', title='Login', form=form)

#Route for logout
@app.route("/logout")
def logout():
    logger.info('User logged out')
    logout_user()
    return redirect(url_for('home'))

# <!----------------------------------------------!---------------------------------------------->

#Route for acount page
@app.route("/account", methods=['GET','POST'])
def account():
    logger.info('Account page accessed')
    return render_template('account.html')

# <!----------------------------------------------!---------------------------------------------->

#Route for user verification page
@app.route("/verified", methods=['GET', 'POST'])
@login_required
def verification():
    user_info = User_Verified.query.filter_by(user_id=current_user.id).first()
    logger.info(f'User verification page accessed for user ID: {current_user.id}')
    form = VerifyForm()
    
    if user_info:
        print(f"Phone: {user_info.phone}, Address: {user_info.address}")
        logger.info(f'User information found: Phone: {user_info.phone}, Address: {user_info.address}')
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
@app.route('/delete_account', methods=['GET','POST'])
@login_required
def deleteAcc():
    logger.info('Delete account page accessed')
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
    logger.info('Notifications page accessed')
    form = NotificationForm()
    if form.validate_on_submit():
        logger.info('User updated notification preferences')
        flash('Your preferences have been updated.', 'success')
        return redirect(url_for('account'))
    return render_template('account-components/notifications.html', form=form)

# <!----------------------------------------------!---------------------------------------------->

# RESET PW BEGINNING
def send_reset_email(user):
    token = user.get_reset_token()
    reset_url = url_for('reset_token', token=token, _external=True)
    msg = Message('Password Reset Request', 
                  sender='noreply@demo.com', 
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{reset_url}

'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if current_user and within_reset_limit(current_user):
        flash('You have exceeded the password reset limit. Please try again later.', 'warning')
        return redirect(url_for('login'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = secrets.token_hex(16)
            reset_token = PasswordResetToken(user_id=user.id, token=token)
            db.session.add(reset_token)
            db.session.commit()
            send_reset_email(user)

            if current_user:
                current_user.last_reset_request = datetime.utcnow()
                db.session.commit()

            flash('An email has been sent with instructions to reset your password.', 'info')  
            return redirect(url_for('login'))
        else:
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
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

def within_reset_limit(user, limit=3, timeframe=timedelta(hours=1)):
    """
    Check if the user has exceeded the password reset request limit within the specified timeframe.
    """
    if isinstance(user, User) and user.last_reset_request:
        earliest_time = datetime.utcnow() - timeframe

        recent_requests = PasswordResetToken.query \
                            .filter_by(user_id=user.id) \
                            .filter(PasswordResetToken.timestamp > earliest_time) \
                            .filter(PasswordResetToken.expired == False) \
                            .group_by(PasswordResetToken.token) \
                            .count()

        return recent_requests >= limit
    else:
        return False
# RESET PW END

# <!----------------------------------------------!---------------------------------------------->

# Registration route
def send_verification_email(user):
    token = user.get_verification_token()
    verification_url = url_for('confirm_email', token=token, _external=True)
    msg = Message('Email Verification', 
                  sender='timothyglazer@gmail.com', 
                  recipients=[user.email])
    msg.body = f'''Please verify your email address by clicking the link below:
{verification_url}

'''
    mail.send(msg)

@app.route("/request_verification_email", methods=['GET', 'POST'])
def request_verification_email():
    if current_user.is_authenticated and not current_user.is_confirmed:
        send_verification_email(current_user)
        flash('A verification email has been sent to your email address.', 'info')
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route("/confirm_email/<token>")
def confirm_email(token):
    try:
        serializer = Serializer(app.config['SECRET_KEY'])
        user_id = serializer.loads(token)['user_id']
        user = User.query.get(user_id)
        if user:
            token = secrets.token_hex(16)
            db.session.add(reset_token)
            db.session.commit()
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('login'))
        else:
            flash('Invalid or expired verification link.', 'danger')
    except:
        flash('Invalid or expired verification link.', 'danger')
    return redirect(url_for('home'))

# <!----------------------------------------------!---------------------------------------------->

@app.route("/admin")
@login_required
@admin_required
def admin():
    logger.info('Admin panel accessed')
    users = User.query.all()
    return render_template('admin.html', users=users)

# <!----------------------------------------------!---------------------------------------------->

# Product page route
@app.route("/product")
def products():
    logger.info('Products page accessed')
    cars = Car.query.order_by(Car.id.desc())
    return render_template('product.html', cars = cars)

# <!----------------------------------------------!---------------------------------------------->

# Setting up appointment booking
@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    logger.info('Appointment booking page accessed')
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
        
        return redirect(url_for('home'))
    return render_template('book_appointment.html', form=form)

def send_confirmation_email(appointment):
    msg = Message('Appointment Confirmation', sender='timothyglazer@gmail.com', recipients=[appointment.email])
    msg.body = f"Hi {appointment.name},\n\nYour appointment on {appointment.date.strftime('%Y-%m-%d')} has been successfully booked.\n\nThank you!"
    mail.send(msg)

# <!----------------------------------------------!---------------------------------------------->

@app.route("/terms_conditions")
def terms_conditions():
    # Assuming tc.pdf is in the static directory
    return redirect(url_for('static', filename='tc.pdf'))

