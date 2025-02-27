from flask_wtf import FlaskForm
from wtforms import HiddenField



class ItemForm(FlaskForm):
    choice = HiddenField('Choice')