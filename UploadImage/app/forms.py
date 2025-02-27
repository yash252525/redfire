from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
from flask_wtf.file import FileRequired,FileAllowed


class ImageUpload(FlaskForm):
    file = FileField('Upload image',validators=[FileRequired(),FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Upload')
