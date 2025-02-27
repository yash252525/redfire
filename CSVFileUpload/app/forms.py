from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import  FileField, SubmitField


class FileUploadCSVForm(FlaskForm):
    file = FileField('Upload a CSV File', validators=[FileRequired(), FileAllowed(['csv'])])
    submit = SubmitField('Upload')