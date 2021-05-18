from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class LoginForm(FlaskForm):
    username = StringField('Username', render_kw={'autofocus': True})
    password = PasswordField('Password')
    submit =  SubmitField("Login")