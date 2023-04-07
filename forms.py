from flask_wtf import FlaskForms
from wtforms import StringField,validators,SelectField,TextAreaField,DateTimeField,DateField,RadioField,FileField,SubmitField,PasswordField
from wtforms.validators import DataRequired

#user Log in form
class UserLog(FlaskForms):
    user_name=StringField("user Name",validators=[DataRequired()])
    pasword=PasswordField("Enter Passowrd")
    submit=SubmitField("Log In")


#user main form
class UserForm(FlaskForms):
    userName=StringField('Name with Initials',validators=[DataRequired()])
    course=SelectField("Course",choices=['IT','Accountency','Management','Tourism'])
    year=SelectField("Year",choices=['1','2','3','4'])
    semeseter=SelectField("Semester",choices=['1','2'])
    attempt=SelectField("Attemp",choices=['1','2','3','4'])
    comment=TextAreaField("Signs and Symptoms Observed By Medical Officer")
    start_date=DateField("Start Date")
    end_date=DateField("End Date")
    doc_name=StringField("Name of the Medical Officer")
    type=RadioField("Medical By",choices=['Government','Private'])
    med_pic=FileField("Upload picture of Medical Sheet")
    date_issued=DateField("Enter Date")
    submit=SubmitField("Save")

