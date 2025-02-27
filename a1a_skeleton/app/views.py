from flask import render_template, redirect, url_for, flash, send_file, send_from_directory, request
from app import app
from app.forms import ChooseForm,TimesForm
import csv
import io

@app.route("/")
def home():
    return render_template('home.html', title="Home")


@app.route("/times/<int:num>")
def table(num):
    if num < 1 or num > 1000:
        flash('Number must be between 1 and 1000', 'danger')
        return redirect(url_for('home'))


    times_table = {'Base': num, 'Multiplicand': [], 'Product': []}
    for i in range(1, 13):
        times_table['Multiplicand'].append(i)
        times_table['Product'].append(num * i)

    return render_template('table.html', title='Multiplication Table', table=times_table)


@app.route("/display_times", methods=['GET', 'POST'])
def display_times():
    form = TimesForm()
    if form.validate_on_submit():
        base = form.base.data
        multiplicand = form.multiplicand.data
        return redirect(url_for('table', num=base, multiplicand=multiplicand))
    return render_template('display_times.html', title='Display Times', form=form)



@app.route("/download_times", methods=['GET', 'POST'])


def display_form_times():
    form = TimesForm()
    if form.validate_on_submit():
        base = form.base.data
        multiplicand = form.multiplicand.data


        times_table = []
        for i in range(1, multiplicand + 1):
            times_table.append([base, i, base * i])


        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Base', 'Multiplicand', 'Product'])
        writer.writerows(times_table)
        output.seek(0)

        return send_file(io.BytesIO(output.getvalue().encode('utf-8')), mimetype='text/csv', as_attachment=True, download_name='times_table.csv')

    return render_template('display_form_times.html', title='Display Times', form=form)





@app.route('/contents', methods=['GET', 'POST'])
def contents():
    numbers = list(range(1, 13))
    if request.method == 'POST':
        if 'display' in request.form:
            return redirect(url_for('display_table'))
        elif 'download' in request.form:
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['Number'])
            for number in numbers:
                writer.writerow([number])
            output.seek(0)
            return send_file(io.BytesIO(output.getvalue().encode('utf-8')), mimetype='text/csv', as_attachment=True, download_name='numbers.csv')
    return render_template('contents.html', title='Contents', numbers=numbers)


# Error handlers
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

# Error handler for 403 Forbidden
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