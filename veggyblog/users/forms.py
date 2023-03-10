from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from veggyblog.models import User


class SignupForm(FlaskForm):
    username = StringField(label= 'Username', 
                           validators=[DataRequired(), Length(min=3, max=30)])
    
    email = StringField(label= 'Email', 
                        validators=[DataRequired(), Email()])
    
    password= PasswordField(label= 'Password', 
                            validators=[DataRequired(), Length(min=8, max=30)])
    
    confirm_password= PasswordField(label= 'Confirm Password', 
                            validators=[DataRequired(), EqualTo('password')])
    
    agree=BooleanField( validators=[DataRequired()])
    
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        
        user = User.query.filter_by( username = username.data).first() # if there's a user, get the first value back from db. If there's a user, will return none
                
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    
    def validate_email(self, email):
        
        email = User.query.filter_by( email = email.data).first() # if there's a user, get the first value back from db. If there's a user, will return none
                
        if email:
            raise ValidationError('That email is taken. Please choose a different one.')
        
class LoginForm(FlaskForm):
        
    email = StringField(label= 'Email', 
                        validators=[DataRequired(), Email()])
    
    password= PasswordField(label= 'Password', 
                            validators=[DataRequired(), Length(min=8, max=30)])
    # allow users to stay logged in for sometime after their browser closes using a secure cookie
    remember = BooleanField('Remember Me') 
    
    submit = SubmitField('Log In')

class UpdateAccountForm(FlaskForm):
    username = StringField(label= 'Username', 
                           validators=[DataRequired(), Length(min=2, max=30)])
    
    email = StringField(label= 'Email', 
                        validators=[DataRequired(), Email()])
    picture = FileField(label= 'Update Profile Piciture', validators=[FileAllowed(['jpg', 'png'])])    
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by( username = username.data).first() # if there's a user, get the first value back from db. If there's a user, will return none
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by( email = email.data).first() # if there's a user, get the first value back from db. If there's a user, will return none 
            if email:
                raise ValidationError('That email is taken. Please choose a different one.')
            
class RequestResetForm(FlaskForm):
    email = StringField(label= 'Email', 
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    def validate_email(self, email):
            
        user = User.query.filter_by( email = email.data).first() # if there's a user, get the first value back from db. If there's a user, will return none
                
        if user is None:
            raise ValidationError('There is no account assicated with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password= PasswordField(label= 'Password', 
                            validators=[DataRequired(), Length(min=8, max=30)])
    
    confirm_password= PasswordField(label= 'Confirm Password', 
                            validators=[DataRequired(), EqualTo('password')])       
    submit = SubmitField('Reset Password')
 
# for save post   
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit') 