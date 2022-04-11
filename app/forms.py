# import email
from ast import Pass
from email.mime import image
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo

class SignUpForm(FlaskForm):
    email= StringField('Email', validators=[DataRequired(), Email()])
    username= StringField('Username', validators=[DataRequired()])
    password= PasswordField('Password', validators=[DataRequired()])
    confirm_pass= PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit= SubmitField('SignUp')


class LoginForm(FlaskForm):
    username= StringField('Username', validators=[DataRequired()])
    password= PasswordField('Password', validators=[DataRequired()])
    submit= SubmitField('Log In')


class RegisterePhoneForm(FlaskForm):
    first_name= StringField('First Name', validators=[DataRequired()])
    last_name= StringField('Last Name', validators=[DataRequired()])
    phone_number= StringField('Phone Number', validators=[DataRequired()])
    city= StringField('City', validators=[DataRequired()])
    image=FileField('Image')
    submit= SubmitField('Register')

class SearchForm(FlaskForm):
    search = StringField('Search',validators=[DataRequired()])
    submit= SubmitField('Search')

