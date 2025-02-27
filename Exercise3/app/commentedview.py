from flask import render_template, redirect, url_for, flash, request
from app import app
from app.forms import ChooseForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm


<li class="nav-item">
    <a class="nav-link" aria-current="page" href="{{ url_for('table', num=3, multiplicand=12) }}">times 3</a>
</li>



class TimesForm(FlaskForm):
    base = IntegerField('Base', validators=[DataRequired(), NumberRange(min=1, max=1000)])
    multiplicand = IntegerField('Multiplicand', default=12, validators=[DataRequired(), NumberRange(min=1, max=1000)])
    submit = SubmitField('Generate Table')

@app.route("/display_times", methods=['GET', 'POST'])
def display_times():
    form = TimesForm()
    if form.validate_on_submit():
        base = form.base.data
        multiplicand = form.multiplicand.data
        return redirect(url_for('table', num=base, multiplicand=multiplicand))
    return render_template('display_times.html', title='Display Times', form=form)

@app.route("/times/<int:num>/<int:multiplicand>")
def table(num, multiplicand):
    if num < 1 or num > 1000 or multiplicand < 1 or multiplicand > 1000:
        flash('Number must be between 1 and 1000', 'danger')
        return redirect(url_for('home'))

    times_table = {'Base': num, 'Multiplicand': [], 'Product': []}
    for i in range(1, multiplicand + 1):
        times_table['Multiplicand'].append(i)
        times_table['Product'].append(num * i)

    return render_template('table.html', title='Multiplication Table', table=times_table)


from flask import render_template, redirect, url_for, flash, request, send_file
from app import app
from app.forms import ChooseForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm
import io
import csv

class TimesForm(FlaskForm):
    base = IntegerField('Base', validators=[DataRequired(), NumberRange(min=1, max=1000)])
    multiplicand = IntegerField('Multiplicand', default=12, validators=[DataRequired(), NumberRange(min=1, max=1000)])
    submit = SubmitField('Generate Table')

@app.route("/download_times", methods=['GET', 'POST'])
def display_times():
    form = TimesForm()
    if form.validate_on_submit():
        base = form.base.data
        multiplicand = form.multiplicand.data

        # Generate the multiplication table
        times_table = []
        for i in range(1, multiplicand + 1):
            times_table.append([base, i, base * i])

        # Create a CSV file in memory
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Base', 'Multiplicand', 'Product'])
        writer.writerows(times_table)
        output.seek(0)

        return send_file(io.BytesIO(output.getvalue().encode('utf-8')), mimetype='text/csv', as_attachment=True, download_name='times_table.csv')

    return render_template('display_times.html', title='Display Times', form=form)


