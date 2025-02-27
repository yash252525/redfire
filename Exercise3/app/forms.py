from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField,HiddenField
from flask_wtf.file import FileAllowed,FileRequired

class FileUploadCSVForm(FlaskForm):
    file = FileField('Upload CSV File', validators=[FileRequired(),FileAllowed(['csv'])])
    submit = SubmitField('Upload')

class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')
    choice2 = HiddenField('Choice2')
