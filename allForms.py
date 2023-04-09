from flask_wtf import FlaskForm
from wtforms import StringField,validators,SelectField,TextAreaField,DateTimeField,DateField,RadioField,FileField,SubmitField,PasswordField
# from wtforms.validators import DataRequired,Length,Email,EqualTo



#user/admin Log in form
class UserLog(FlaskForm):
    user_name=StringField("User Name: ")
    password=PasswordField("Password: ")
    submit=SubmitField("Log In")


#user main form
class UserForm(FlaskForm):
    userName=StringField('Name with Initials')
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

#admin Sign Up
class AdminSignUp(FlaskForm):
    first_name=StringField("Frist Name: ")
    last_name=StringField("Last Name: ")
    email=StringField("Email: ")
    password=PasswordField("Password: ")
    confirm_pasas=PasswordField("Confirm Password: ")
    ati=StringField("ATI: ")
    possition=SelectField("Possision: ",choices=['Office','HOD'])
    submit=SubmitField("Submit")
    
#user SignUp
class UserSignUp(FlaskForm):
    first_name=StringField("First Name: ")
    last_name=StringField("Last Name: ")
    department=SelectField("Department: ",choices=['IT','ACCOUNTANCY','MANAGEMENT','TOURISM'])
    email=StringField("Email: ")
    password=StringField("Password: ")
    confirm=StringField("Confirm Password: ")
    submit=SubmitField("Submit")

    
#Admin Interface
class AdminInterface(FlaskForm):
    edit_time_table=SubmitField("Click To Edit Time Tables:")
    display=SubmitField("Display Requests") 
    accept=SubmitField("Accept")
    all_accept=SubmitField("ALL Accept")
    reject=SubmitField("Reject")
    all_reject=SubmitField("ALL Reject")
    
    
    

#Super Admin Interface
class SuperAdminInterface(FlaskForm):
    pass
