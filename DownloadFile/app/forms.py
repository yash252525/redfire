from flask_wtf import FlaskForm
from wtforms import HiddenField


class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')