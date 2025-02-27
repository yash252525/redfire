from app import app
from flask import Flask,render_template,request,redirect,url_for,flash
from app.forms import ItemForm


@app.route('/')
def home():
    return render_template('home.html',name='Yash',title='Home')



my_list=['Lemon','Apple','Orange']

@app.route('/show_list')
def show_list():
    form = ItemForm()
    return render_template('list.html',my_list=my_list,title='List',form=form)


@app.route('/delete', methods=['GET','POST'])
def delete_item():
    form = ItemForm()
    if form.validate_on_submit():
         choice = int(form.choice.data)
         if choice > len(my_list):
             flash(f'Error','error')
         else:
             my_list.pop(choice)
         flash(f'Item deleted', 'info')
    return redirect(url_for('show_list'))


@app.route('/reset',methods=['GET','POST'])
def reset_items():
    form = ItemForm()
    if form.validate_on_submit():
        my_list.clear()
        my_list.extend(['Lemon','Apple','Orange'])
        flash(f'Items reset', 'success')
        return redirect(url_for('show_list'))