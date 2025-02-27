from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired,FileAllowed
from wtforms import FileField,SubmitField


class FileUploadTXTForm(FlaskForm):
    file = FileField('Upload a txt extension file.', validators=[FileRequired(),FileAllowed(['txt'])])
    submit = SubmitField('Upload')