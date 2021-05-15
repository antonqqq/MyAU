from flask import Flask, render_template, url_for, redirect, session
from login import LoginForm
from scraper import Login

app = Flask(__name__)
app.config['SECRET_KEY'] = '2898289899aA'

username = "aufantonq"
password = "antonquiambao"

@app.route("/", methods=('GET', 'POST'))
def login():
    if session.get('username'):
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # return home(form.username.data, form.password.data)
        session['username'] = form.username.data
        session['password'] = form.password.data
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route("/home")
def home():
    try:
        data = Login(session['username'], session['password'])
        return render_template('index.html', data = data)
    except:
        session.clear()
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
