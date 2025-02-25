from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField,TextAreaField,FloatField
from wtforms.validators import DataRequired, EqualTo, Email,Length, NumberRange,ValidationError
from datetime import date, datetime, timedelta

try:
    from wtforms.fields import EmailField,TelField # WTForms 3.0+
except ImportError:
    from wtforms.fields.html5 import EmailField,TelField

def validate_dob(form,field):
    today = date.today()
    min_age_date = today - timedelta(days=365 *120)
    max_age_date = today - timedelta(days=365 *16)

    if field.data > today:
        raise ValidationError('Date of birth cannot be in the future')
    if field.data < min_age_date:
        raise ValidationError('Date if birth is too far in the past')
    if field.data > max_age_date:
        raise ValidationError('You must be atleast 16 years old to registeer')
class LoginForm(FlaskForm):
    email = EmailField('Email ID',validators=[Email(),DataRequired(),Length(min=5,max=25)])
    username = StringField('username',validators=[DataRequired(),Length(min=6,max=10)])
    dateofbirth = DateField('Date of birth, format=(YYYY-MM-DD)',validators=[DataRequired(),validate_dob])
    phonenum = TelField('Contact number',validators=[DataRequired(),Length(min=10,max=15)])
    address = TextAreaField('Address',validators=[DataRequired(),Length(max=40)])
    height = FloatField('Height in cm',validators=[DataRequired(),NumberRange(min=50,max=300,message="Height must be in between 50 to 300 cm")])
    weight = FloatField('Weight in kgs',validators=[DataRequired(),NumberRange(min=2,max=250,message='Weight must be in between 2 to 250 kg')])
    password1 = PasswordField('password',validators=[DataRequired(),Length(min=8,max=20)])
    password2 = PasswordField('re-type your password',validators=[DataRequired(),EqualTo('password1',message='Password must match')])
    submit = SubmitField('Register')