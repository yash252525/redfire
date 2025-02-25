from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
try:
    from wtforms.fields import EmailField # WTForms 3.0+
except ImportError:
    from wtforms.fields.html5 import EmailField  # Older versions
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    boolean = BooleanField('bool')

    submit = SubmitField('Sign In')
