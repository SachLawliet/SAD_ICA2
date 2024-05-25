from flask import render_template, request, flash, redirect, url_for, Request, session
from carlease import app, db, bcrypt, bootstrap, mail
from carlease.forms import RegistrationForm, LoginForm, VerifyForm, NotificationForm, RequestResetForm, ResetPasswordForm
from carlease.models import User, Car, User_Verified
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import os

posts= [
    {
        'model': 'Fiat 500',
        'color': 'dark blue',
        'city': 'Praha'
    },
    {
        'model': 'Ferrarri F40',
        'color': 'red',
        'city': 'Brno'
    },
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/registration", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, full_name=form.full_name.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', form = form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember= form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful', 'danger')
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    user_info = User_Verified.query.filter_by(user_id=current_user.id).first()
    if user_info:
        return render_template('account.html', user_info=user_info, editable=False)
    else:
        form = VerifyForm()
        if form.validate_on_submit():
            user_info = User_Verified(
                user_id=current_user.id,
                phone=form.phone.data,
                address=form.address.data,
            )
            db.session.add(user_info)
            db.session.commit()
            return render_template('account.html', user_info=user_info, editable=False)
        return render_template('account.html', form=form, editable=True)



# <!----------------------------------------------!---------------------------------------------->
# Routes to account components
@app.route("/verification")
@login_required
def verification():
    return render_template('account-components/verification.html')

@app.route("/account-security")
@login_required
def accSecurity():
    return render_template('account-components/security.html')

@app.route('/delete-account')
@login_required
def deleteAcc():
    return render_template('account-components/delete-account.html')

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

