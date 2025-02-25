from flask import Flask, render_template, url_for,flash
from werkzeug.utils import redirect

from app import app
from app.login import LoginForm


@app.route('/')
def home():
    return render_template('Dashboardpage.html')

@app.route('/jinja')
def jinja():
    msg = "hello from views.py"
    return render_template('jinja.html', messageforjinja=msg)

@app.route('/<name>')
def functionnm(name):
    return render_template('namepage.html', name=name)

@app.route('/list')
def listing():
    list = ['yash','pashya','APK', 'kaushal','Mayuri']
    return render_template('list.html',list=list)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'User {form.username.data} logged in !!')
        print('From is valid')
        return redirect(url_for('home'))
    print('Form is not valid')
    return render_template('login.html',title="Login Page", form=form )

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash(f'User {form.username.data} logged in !!', 'success')
#         print(f'Flashing message: User {form.username.data} logged in !!')
#         return redirect(url_for('home'))
#
#     print('Form validation failed')
#     return render_template('login.html', title="Login Page", form=form)
