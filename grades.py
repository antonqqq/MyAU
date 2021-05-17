from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

class GradeForm(FlaskForm):
    period = SelectField('Period', choices=[('Prelim', 'Prelim'), ('Midterm', 'Midterm'), ('Final', 'Final')])
    sem = SelectField('Semester', choices=[('1', '1st Semester'), ('2', '2nd Semester')])
    sy =  SelectField("SY", choices=[('2020-2021'), ('2019-2020'), ('2018-2019')])
    submit =  SubmitField("Submit")