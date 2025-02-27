from flask import render_template, flash,  url_for, redirect, send_file, send_from_directory
from app import app
from app.forms import ImageUpload

from uuid import uuid4
from werkzeug.utils import secure_filename
import os
import csv
import datetime
import io

@app.route("/")
def home():
    app.logger.debug("Debug")
    app.logger.info("Info")
    app.logger.warning("Warning")
    app.logger.error("Error")
    app.logger.critical("Critical")
    return render_template('home.html', name='Yash', title="Home")

@app.route('/upload_image',methods=['GET','POST'])
def img_upload():
    form = ImageUpload()
    if form.validate_on_submit():
        if form.file.data:
            unique_str = str(uuid4())
            filename = secure_filename(f'{unique_str}-{form.file.data.filename}')
            filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            form.file.data.save(filepath)
            flash('File uploaded','success')
            return render_template('uploadcomplete.html',title = 'Upload Successful',user_image=url_for('download_img', name=filename))

    return render_template('uploadimage.html',title='Please Upload Image',form=form)


@app.route('/upload_complete/<name>')
def download_img(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)
