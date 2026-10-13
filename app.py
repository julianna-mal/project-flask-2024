from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)