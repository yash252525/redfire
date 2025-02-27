from flask import Flask,render_template,url_for,request,redirect,flash,send_file, send_from_directory
from app import app
from app.forms import FileUploadCSVForm
from email_validator import validate_email, EmailNotValidError
from uuid import uuid4
from werkzeug.utils import secure_filename
import os
import csv
import datetime
import io


def is_valid_email(email):
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as error:
        return False
    return True

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



@app.route('/upload_csv_file', methods=['GET', 'POST'])
def upload_csv_file():
    lines = []
    contacts = []
    form = FileUploadCSVForm()
    if form.validate_on_submit():
        if form.file.data:
            unique_str = str(uuid4())
            filename = secure_filename(f'{unique_str}-{form.file.data.filename}')
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.file.data.save(filepath)
            try:
                with open(filepath, newline='') as csvFile:
                    reader = csv.reader(csvFile)
                    error_count = 0
                    header_row = next(reader)
                    if header_row != ['Name', 'Email', 'Phone']:
                        form.file.errors.append(
                            'First row of file must be a Header row containing "Name,Email,Phone"')
                        raise ValueError()
                    contacts.append(header_row)
                    for idx, row in enumerate(reader):
                        row_num = idx + 2  # Spreadsheets have the first row as 0, and we skip the header
                        if error_count > 10:
                            form.file.errors.append('Too many errors found, any further errors omitted')
                            raise ValueError()
                        if len(row) != 3:
                            form.file.errors.append(f'Row {row_num} does not have precisely 3 fields')
                            error_count += 1
                            continue
                        if not is_valid_email(row[1]):
                            form.file.errors.append(f'Row {row_num} has an invalid email: "{row[1]}"')
                        if error_count == 0:
                            contacts.append(row)
                if error_count > 0:
                    raise ValueError
                flash(f'File Uploaded', 'success')
                return render_template('display_contacts.html', title='Display Contacts', contacts=contacts)
            except Exception as err:
                flash(f'File upload failed.'
                      ' Please correct your file and try again', 'danger')
                app.logger.error(f'Exception occurred: {err=}')
            finally:
                silent_remove(filepath)
    return render_template('upload_file.html', title='Upload CSV File', form=form)
