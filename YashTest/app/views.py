from flask import render_template,request,flash,url_for
from app import app
from app.forms import QuickForm
@app.route('/')
def home():
   return render_template('base.html')


@app.route('/quickforms',methods=['GET','POST'])
def quickforms():
    form = QuickForm()
    if form.validate_on_submit():
        return render_template('quickforms.html',form=form)
    return render_template('quickforms.html',form=form)



@app.route('/manualforms',methods=['GET','POST'])
def manualforms():
    form = QuickForm()
    if form.validate_on_submit():
        return render_template('manualforms.html',form=form)
    return render_template('manualforms.html', form=form)
