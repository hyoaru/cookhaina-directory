from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email

class SignUpForm(FlaskForm):
    username = StringField(
        'Username',
        validators = [DataRequired(), Length(min=3, max=20),], )
    
    email = StringField(
        'Email address',
        validators = [DataRequired(), Email(),], )
    
    password = PasswordField(
        'Password',
        validators = [DataRequired(),], )

    submit = SubmitField('Create account')


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators = [DataRequired(), Length(min=3, max=20),], )
     
    password = PasswordField(
        'Password',
        validators = [DataRequired(),], )

    remember = BooleanField('Remember me')

    submit = SubmitField('Log in')