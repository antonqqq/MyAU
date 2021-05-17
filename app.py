from flask import Flask, render_template, url_for, redirect, session
from flask import request
from login import LoginForm
from grades import GradeForm
from scraper import Login, get_grades

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
    # try:
        form2 = GradeForm()
        data = Login(session['username'], session['password'])
        return render_template('index.html', data = data, form2 = form2)
    # except:
    #     session.clear()
    #     return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/grades", methods=('GET', 'POST'))
def grades():
    # period = request.args.get('period')
    # sem = request.args.get('sem')
    # sy = request.args.get('sy')
    form2 = GradeForm()
    print(form2.period.data)
    print(form2.sem.data)
    print(form2.sy.data)
    data = Login(session['username'], session['password'], form2.period.data, form2.sem.data, form2.sy.data)
    return render_template('index.html', data = data, form2 = form2)

if __name__ == '__main__':
    app.run()
