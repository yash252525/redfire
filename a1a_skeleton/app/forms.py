from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, NumberRange

class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')

class TimesForm(FlaskForm):
    base = IntegerField('Base', validators=[DataRequired(), NumberRange(min=1, max=1000)])
    multiplicand = IntegerField('Multiplicand', default=12, validators=[DataRequired(), NumberRange(min=1, max=1000)])
    submit = SubmitField('Generate Table')