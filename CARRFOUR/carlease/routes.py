from flask import render_template, request, flash, redirect, url_for, Request
from carlease import app, db, bcrypt
from carlease.forms import RegistrationForm, LoginForm
from carlease.models import User, Car, Reservation
from flask_login import login_user, current_user, logout_user, login_required
import os

pictures = os.path.join('static','media')
app.config['UPLOAD_FOLDER'] = pictures

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
    skodaVision = os.path.join(app.config['UPLOAD_FOLDER'], 'skodaVision.jpeg')
    return render_template('index.html', user_image = skodaVision)

@app.route("/registration", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')
        return redirect(url_for('login'))
    return render_template('resgitration.html', form = form)

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
            flash('Login unsuccessful, please check email and password', 'danger')
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html')



@app.route("/product")
def product():
    return render_template('product.html', posts=posts)

