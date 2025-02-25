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
                    if header_row != ['Name', 'Email', 'Phone', 'Birthdate']:
                        form.file.errors.append(
                            'First row of file must be a Header row containing "Name,Email,Phone,Birthdate"')
                        raise ValueError()
                    contacts = [header_row]
                    names = set()
                    duplicate_count = 0
                    for idx, row in enumerate(reader):
                        row_num = idx + 2  # Spreadsheets have the first row as 0, and we skip the header
                        if error_count > 10:
                            form.file.errors.append('Too many errors found, any further errors omitted')
                            raise ValueError()
                        if len(row) != 4:
                            form.file.errors.append(f'Row {row_num} does not have precisely 4 fields')
                            error_count += 1
                            continue
                        if not is_valid_email(row[1]):
                            form.file.errors.append(f'Row {row_num} has an invalid email: "{row[1]}"')
                            error_count += 1
                        if not is_valid_birthdate(row[3]):
                            form.file.errors.append(f'Row {row_num} has an invalid birthdate: "{row[3]}"')
                            error_count += 1
                        if row[0] in names:
                            duplicate_count += 1
                            continue
                        names.add(row[0])
                        contacts.append(row)
                    if error_count > 0:
                        raise ValueError
                    if duplicate_count > 0:
                        flash(f'{duplicate_count} duplicate entries were removed.', 'warning')
                    flash(f'File Uploaded', 'success')
                    return render_template('display_contacts.html', title='Display Contacts', contacts=contacts)
            except Exception as err:
                flash(f'File upload failed. Please correct your file and try again', 'danger')
                app.logger.error(f'Exception occurred: {err=}')
            finally:
                os.remove(filepath)
    return render_template('upload_file.html', title='Upload CSV File', form=form)