from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from cookhaina_directory.instances import bcrypt

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

class CommentForm(FlaskForm):
    comment = StringField(
        'Comment',
        validators = [DataRequired(), Length(max = 1500, message = 'Comment must be under 1500 characters')], )
    
    submit = SubmitField('Submit')


class AccountForm(FlaskForm):
    username = StringField(
        'Username',
        validators = [Length(min=3, max=20),], )
    
    email = StringField(
        'Email address',
        validators = [Email(),], )

    submit = SubmitField('Save changes')


class UpdatePasswordForm(FlaskForm):
    def validate_password(self, current_password):
        if not bcrypt.check_password_hash(pw_hash = current_user.password, password = current_password.data):
            raise ValidationError(message = 'Incorrect password')
        
    current_password = PasswordField(
        'Current password',
        validators = [
            DataRequired(message = 'Must provide current password'),
            validate_password,], )
    
    new_password = PasswordField(
        'Password',
        validators = [
            DataRequired(message = 'Must provide a new password'),
            Length(min = 8, max = 50, message = 'Password must be between 8 and 40 characters long'),], )
    
    submit = SubmitField('Save changes')