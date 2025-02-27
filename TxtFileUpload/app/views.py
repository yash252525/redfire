from flask import render_template, flash,  url_for, redirect, send_file, send_from_directory
from app import app
from app.forms import FileUploadTXTForm
from email_validator import validate_email, EmailNotValidError
from uuid import uuid4
from werkzeug.utils import secure_filename
import os
import csv
import datetime
import io
import logging

def silent_remove(filepath):
    try:
        os.remove(filepath)
    except:
        pass
    return


@app.route("/")
def home():
    app.logger.debug("Debug")
    app.logger.info("Info")
    app.logger.warning("Warning")
    app.logger.error("Error")
    app.logger.critical("Critical")
    return render_template('home.html', name='Yash', title="Home")


@app.route('/upload_txt_file', methods=['GET', 'POST'])
def upload_txt_file():
    lines = []
    form = FileUploadTXTForm()
    if form.validate_on_submit():
        if form.file.data:
            unique_str = str(uuid4())
            filename = secure_filename(f'{unique_str}-{form.file.data.filename}')
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            app.logger.info(f'Saving file to: {filepath}')
            try:
                form.file.data.save(filepath)
                app.logger.info(f'File saved successfully to: {filepath}')

                # Check if the file exists
                if os.path.exists(filepath):
                    app.logger.info(f'File exists at: {filepath}')
                else:
                    app.logger.error(f'File does not exist at: {filepath}')

                with open(filepath, newline='') as txtFile:
                    for line in txtFile:
                        lines.append(line)
                flash(f'File Uploaded', 'success')
                return render_template('display_text.html', title='Display Text', lines=lines)
            except Exception as err:
                flash(f'File upload failed. Please try again', 'danger')
                app.logger.error(f'Exception occurred: {err}')


            # finally:
            #     silent_remove(filepath)
    return render_template('upload_file.html', title='Upload Text File', form=form)








# @app.route('/upload_txt_file', methods=['GET', 'POST'])
# def upload_txt_file():
#     lines = []
#     form = FileUploadTXTForm()
#     if form.validate_on_submit():
#         if form.file.data:
#             unique_str = str(uuid4())
#             filename = secure_filename(f'{unique_str}-{form.file.data.filename}')
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             form.file.data.save(filepath)
#             try:
#                 with open(filepath, newline='') as txtFile:
#                     for line in txtFile:
#                         lines.append(line)
#                 flash(f'File Uploaded', 'success')
#                 return render_template('display_text.html', title='Display Text', lines=lines)
#             except Exception as err:
#                 flash(f'File upload failed.'
#                       ' please try again', 'danger')
#                 app.logger.error(f'Exception occurred: {err=}')
#             finally:
#                 silent_remove(filepath)
#     return render_template('upload_file.html', title='Upload Text File', form=form)
