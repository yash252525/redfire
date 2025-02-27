from flask import render_template, flash,  url_for, redirect, send_file, send_from_directory
from app import app
from app.forms import ChooseForm
from email_validator import validate_email, EmailNotValidError
from uuid import uuid4
from werkzeug.utils import secure_filename
import os
import csv
import datetime
import io

@app.route("/")
def home():
    return  render_template('home.html',name='Yash',title='Home')



@app.route('/download_file', methods=['GET', 'POST'])
def download_file():
    form=ChooseForm()
    if form.validate_on_submit():
        chosen = form.choice.data
        try:
            if chosen == 'Static':
                return send_from_directory('static', 'phonebook.xlsx', as_attachment=True, download_name='sample.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            elif chosen == 'Dynamic':
                text = f'This is a text file dynamically generated on {datetime.datetime.now()}'
                mem = io.BytesIO()
                mem.write(text.encode(encoding="utf-8"))
                mem.seek(0)
                return send_file(mem, as_attachment=True, download_name='output.txt', mimetype='text/plain')
        except Exception as err:
            flash(f'File Download failed.'
                  ' please try again', 'danger')
            app.logger.error(f'Exception occurred in File Download: {err=}')
    return render_template('download.html', title='Download', form=form)