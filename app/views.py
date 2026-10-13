from flask import render_template, request, redirect, url_for
from . import app

@app.route('/')
@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
       
        print(f"Отримано повідомлення від {name} ({email}): {message}")
        return redirect(url_for('contacts'))
    return render_template('contacts.html')