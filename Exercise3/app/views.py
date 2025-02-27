from app import app
from flask import Flask,render_template,redirect,url_for,request,flash,send_file
from app.forms import FileUploadCSVForm,ChooseForm
from email_validator import validate_email,EmailNotValidError
import csv
import os
from uuid import uuid4
from werkzeug.utils import secure_filename
from _datetime import datetime,timedelta
import io
import tempfile

def silent_remove(filepath):
    try:
        os.remove(filepath)
    except:
        pass
    return



def is_valid_email(email):
    try:
        validate_email(email,check_deliverability=False)
    except EmailNotValidError as error:
        return  False
    return True

def is_valid_birthdate(birthdate_str):
    try:

        birthdate = datetime.strptime(birthdate_str, '%d/%m/%Y').date()
        today = datetime.today().date()
        max_age = today - timedelta(days=120 * 365)
        min_age = today

        if birthdate > min_age or birthdate < max_age:
            return False
        return True
    except ValueError:
        return False

def calculate_age(birthdate_str):

    birthdate = datetime.strptime(birthdate_str, '%d/%m/%Y').date()
    today = datetime.today().date()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


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
                    expected_header = ['Name', 'Email', 'Phone', 'Birthdate']
                    if [col.strip() for col in header_row] != expected_header:
                        form.file.errors.append(
                            'First row of file must be a Header row containing "Name,Email,Phone,Birthdate"')
                        raise ValueError()
                    contacts = [header_row + ['Age']]  # Add 'Age' to the header
                    names = set()
                    duplicate_count = 0
                    for idx, row in enumerate(reader):
                        row_num = idx + 2  # Spreadsheets have the first row as 0, and we skip the header
                        if error_count > 10:
                            form.file.errors.append('Too many errors found, any further errors omitted')
                            raise ValueError()
                        if len(row) != 4:  # Check for 4 fields
                            form.file.errors.append(f'Row {row_num} does not have precisely 4 fields')
                            error_count += 1
                            continue
                        if not is_valid_email(row[1]):
                            form.file.errors.append(f'Row {row_num} has an invalid email: "{row[1]}"')
                            error_count += 1
                        if not is_valid_birthdate(row[3]):
                            form.file.errors.append(f'Row {row_num} has an invalid birthdate: "{row[3]}"')
                            error_count += 1
                        if row[0] in names:  # Check for duplicate names
                            duplicate_count += 1
                            continue  # Skip this row
                        names.add(row[0])  # Add the name to the set
                        age = calculate_age(row[3])  # Calculate age
                        contacts.append(row + [age])  # Append the row with age to the contacts list
                    if error_count > 0:
                        raise ValueError
                    if duplicate_count > 0:
                        flash(f'{duplicate_count} duplicate entries were removed.', 'warning')
                    flash(f'File Uploaded', 'success')
                    return render_template('display_contacts.html', title='Display Contacts', contacts=contacts)
            except Exception as err:
                flash(f'File upload failed. Please correct your file and try again', 'danger')
                app.logger.error(f'Exception occurred: {err}')
                app.logger.error(f'Row causing error: {row}')  # Log the problematic row
            finally:
                os.remove(filepath)
    return render_template('upload_file.html', title='Upload CSV File', form=form)





@app.route('/download_csv')
def download_csv():
    # Get the contacts data from the query parameter
    contacts = request.args.get('contacts')
    contacts = eval(contacts)  # Convert the string back to a list

    # Create a temporary file to hold the CSV data
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv') as temp_file:
        writer = csv.writer(temp_file, delimiter=',')  # Explicitly set delimiter to comma

        # Write each row to the CSV file (excluding the age column)
        for row in contacts:
            writer.writerow(row[:4])  # Only include the first 4 columns (Name, Email, Phone, Birthdate)

        temp_file_path = temp_file.name

    # Return the CSV file as a downloadable attachment
    return send_file(
        temp_file_path,
        mimetype='text/csv',
        as_attachment=True,
        download_name='new_contacts.csv'
    )


@app.route('/mylist')
def mylist():
    form = ChooseForm()
    lst = ['Car', 'House', 'TV']
    return render_template('list.html', lst=lst, title="MyList", form=form, chosen=-1, chosen2=-1)

@app.route('/choose', methods=['POST'])
def choose():
    lst = ['Car', 'House', 'TV']
    form = ChooseForm()
    if form.validate_on_submit():
        action = request.form.get('action')  # Get the action (primary or secondary)
        chosen = int(form.choice.data)
        chosen2 = int(form.choice2.data)

        if action == 'primary':
            chosen = int(request.form.get('choice'))  # Update only the primary choice
            chosen2 = int(form.choice2.data)  # Keep the secondary choice unchanged
        elif action == 'secondary':
            chosen2 = int(request.form.get('choice2'))  # Update only the secondary choice
            chosen = int(form.choice.data)  # Keep the primary choice unchanged

        # Validate that primary and secondary choices are not the same
        if chosen == chosen2 and chosen != -1:
            flash('Primary and secondary items cannot be the same.', 'danger')
        else:
            if chosen != -1:
                flash(f'{lst[chosen]} chosen as primary', 'success')
            if chosen2 != -1:
                flash(f'{lst[chosen2]} chosen as secondary', 'success')
            if chosen == -1 and chosen2 == -1:
                flash('Selection reset', 'success')

        return render_template('list.html', lst=lst, title='ChoiceList', form=form, chosen=chosen, chosen2=chosen2)

    return render_template('list.html', lst=lst, title='ChoiceList', form=form, chosen=-1, chosen2=-1)




def read_menu():
    menu = {'Starter':[], 'Main':[], 'Desert':[]}
    with open('app/data/menu.csv' , newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            menu[row['Course']].append(row)
        return menu

@app.route('/menu', methods=['GET', 'POST'])
def display_menu():
    menu = read_menu()

    if request.method == 'POST':
        # Get selected items (default to 'None' if not provided)
        starter = request.form.get('starter', 'None')
        main = request.form.get('main', 'None')
        dessert = request.form.get('dessert', 'None')

        total = 0
        receipt = []

        if starter != 'None':
            item = next(item for item in menu['Starter'] if item['Dish'] == starter)
            receipt.append(f"Starter: {item['Dish']} - £{item['Price']}")
            total += float(item['Price'])

        if main != 'None':
            item = next(item for item in menu['Main'] if item['Dish'] == main)  # Fixed: Use 'main' instead of 'starter'
            receipt.append(f"Main: {item['Dish']} - £{item['Price']}")
            total += float(item['Price'])

        if dessert != 'None':
            item = next(item for item in menu['Desert'] if item['Dish'] == dessert)  # Fixed: Use 'dessert' instead of 'starter'
            receipt.append(f"Dessert: {item['Dish']} - £{item['Price']}")
            total += float(item['Price'])

        receipt.append(f"Total: £{total:.2f}")  # Fixed: Use '.2f' for two decimal places

        # Create a text file
        receipt_text = "\n".join(receipt)
        receipt_file = io.BytesIO(receipt_text.encode('utf-8'))
        receipt_file.seek(0)

        return send_file(receipt_file, as_attachment=True, download_name='receipt.txt', mimetype='text/plain')
        # return render_template('receipt.html', receipt=receipt,title='Receipt')  # Return the receipt template

    # For GET requests, display the menu
    return render_template('menu.html', starters=menu['Starter'], mains=menu['Main'], desserts=menu['Desert'], title='Menu')


@app.route('/upload_sort_menu', methods=['GET', 'POST'])
def upload_and_sort():
    form = FileUploadCSVForm()
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return "No file uploaded", 400

        file = request.files['file']

        # Validate file type
        if file.filename.endswith('.csv'):
            # Read the CSV file
            file_stream = io.StringIO(file.read().decode('utf-8'))
            reader = csv.DictReader(file_stream)
            menu = list(reader)

            # Sort by course and price
            menu.sort(key=lambda x: (x['Course'], float(x['Price'])))

            # Create a downloadable CSV
            sorted_csv = io.StringIO()
            writer = csv.DictWriter(sorted_csv, fieldnames=['Course', 'Dish', 'Price'])
            writer.writeheader()
            writer.writerows(menu)

            sorted_csv.seek(0)
            return send_file(io.BytesIO(sorted_csv.getvalue().encode('utf-8')), as_attachment=True,
                             download_name='sorted_menu.csv', mimetype='text/csv')
        else:
            return "Invalid file type. Please upload a CSV file.", 400

    return render_template('upload.html',title='Upload & Sort',form=form)

@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', title='Error'), 403

# Handler for 404 Not Found
@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Error'), 404

@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html', title='Error'), 413

# 500 Internal Server Error
@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='Error'), 500