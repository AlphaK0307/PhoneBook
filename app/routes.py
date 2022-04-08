# from re import template
from crypt import methods
from app import app
from flask import redirect, render_template, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from app.forms import SignUpForm, RegisterePhoneForm, LoginForm
from app.models import User, Post, Phone

@app.route('/')
def index():
    title='Home'
    phones=Phone.query.all()
    return render_template('index.html', title=title, phones=phones)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    title= 'Sign Up'
    form = SignUpForm()
    if form.validate_on_submit():
        email=form.email.data
        username=form.username.data
        password=form.password.data
        #Create if there is a user with email or username
        users_with_that_info = User.query.filter((User.username==username)|(User.email==email)).all()
        if users_with_that_info:
            flash(f"Username and/or Email already exist. Please try again", "danger")
            return render_template('signup.html', title=title, form=form)
        # create new user instance
        new_user=User(email=email,username=username, password=password)
        #flash message
        flash(f"{new_user.username} has been successfully Signed Up!", "success")
        return redirect(url_for('index'))
    return render_template('signup.html', title=title, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title= 'Login In'
    form=  LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Check user with that username
        user= User.query.filter_by(username=username).first()
        # Check if not user with that username and make sure pass is correct
        if user and user.check_password(password):
            # log the user in with flasak login
            login_user(user)
            flash(f'{user} has successfully logged in', 'success')
            return redirect(url_for('index'))
        else:
            flash(f'Username and/or password is incorrect', 'danger')
    return render_template('login.html', title=title, form=form)


@app.route('/register-phone', methods=['GET', 'POST'])
@login_required
def register_phone():
    title= 'Register your Phone'
    form= RegisterePhoneForm()
    phones=Phone.query.all()
    if form.validate_on_submit():
        first_name=form.first_name.data
        last_name=form.last_name.data
        phone_number=form.phone_number.data
        city=form.city.data
        Phone(first_name=first_name, last_name=last_name, phone_number=phone_number, city=city)
        flash(f'New PhoneNumber Entry has been made for {first_name}', 'primary')
        return redirect(url_for('index'))
    return render_template('register_phone.html', title=title, form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash(f'You have logged out', 'primary')
    return redirect(url_for('index'))

@app.route('/my-phones')
@login_required
def my_phones():
    title = 'My Phone Numbers'
    phones = current_user.phones.all()
    return render_template('my_phones.html', title=title, phones=phones)