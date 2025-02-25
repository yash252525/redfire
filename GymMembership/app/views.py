from flask import Flask, url_for, request, render_template,flash, redirect


from app import app
from app.forms import LoginForm
from app.ordermenu import MealForm


@app.route('/Registration', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'User {form.username.data} registered successfully!', 'success')
        return redirect(url_for('register'))

    # Debugging: Print errors if form submission fails
    if form.errors:
        print(form.errors)  # Check console logs for validation errors

    return render_template('Registration.html', form=form)


@app.route('/orderfood',methods=['GET','POST'])
def meal():
    mealform = MealForm()
    if mealform.validate_on_submit():
        starter = mealform.starter.data
        main_course = mealform.main_course.data
        dessert = mealform.dessert.data
        flash(f'Order submitted: Starter: {starter}, Main Course: {main_course}, Dessert: {dessert}', 'success')
        return redirect(url_for('meal'))
    return render_template('order.html',form=mealform)
# @app.route('/Registration',methods=['GET','POST'])
# def register():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash(f'User {form.username.data} registered.')
#         return redirect(url_for('register'))
#     return render_template('Registration.html',form=form)