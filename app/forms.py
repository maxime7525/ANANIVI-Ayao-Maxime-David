from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,BooleanField,SubmitField,EmailField
from wtforms.validators import DataRequired, EqualTo,Length,Email
from flask_wtf.recaptcha import RecaptchaField
from wtforms.widgets import PasswordInput


class LoginForm(FlaskForm):
    email = StringField('email',validators=[DataRequired(),Email()])
    password =PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Remember_me')
    submit = SubmitField('CONNECTER')
    #email = EmailField('Email')
    
class UserForm(FlaskForm):
    username = StringField('nom',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('email',validators=[DataRequired(),Email()])
    password =PasswordField('Password',validators=[DataRequired()],widget=PasswordInput(hide_value=False))
    submit = SubmitField('Connecter')
    
    
