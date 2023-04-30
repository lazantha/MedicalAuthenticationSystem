from flask_wtf import FlaskForm
from wtforms import StringField,validators,SelectField,TextAreaField,DateTimeField,DateField,RadioField,FileField,SubmitField,PasswordField,TimeField
from wtforms.validators import DataRequired, Length, EqualTo
from email_validator import validate_email



#admin Log in form
class AdminLog(FlaskForm):
    user_name=StringField("User Name: ",validators=[DataRequired(), Length(min=3, max=10)])
    password=PasswordField("Password: ",validators=[DataRequired(),Length(min=4)])
    possition=SelectField("Possition",choices=['OFFICE','HOD'])
    department=SelectField("Department",choices=['IT','MANAGEMENT','ACCOUNTANCY','ENGLISH','TOURISM'])
    submit=SubmitField("Log In")
    

#user Log in form
class UserLog(FlaskForm):
    user_name=StringField("User Name: ",validators=[DataRequired(),Length(min=3, max=10)])
    password=PasswordField("Password: ")
    submit=SubmitField("Log In")


#user main form
class UserForm(FlaskForm):
    userName=StringField('Name with Initials',validators=[DataRequired(),Length(min=3, max=10)])
    course=SelectField("Course",choices=['IT','Accountency','Management','Tourism'],validators=[DataRequired()])
    year=SelectField("Year",choices=['1','2','3','4'],validators=[DataRequired()])
    semester=SelectField("Semester",choices=['1','2'],validators=[DataRequired()])
    attempt=SelectField("Attemp",choices=['1','2','3','4'],validators=[DataRequired()])
    start_date=DateField("Start Date",validators=[DataRequired()])
    end_date=DateField("End Date",validators=[DataRequired()])
    date_issued=DateField("Issued Date",validators=[DataRequired()])
    type=RadioField("Medical By",choices=['Government','Private'],validators=[DataRequired()])
    med_pic=FileField("Upload picture of Medical Sheet",validators=[DataRequired()])
    submit=SubmitField("Save")

#admin Sign Up
class AdminSignUp(FlaskForm):
    first_name=StringField("Frist Name: ",validators=[DataRequired(),Length(min=3, max=10)])
    last_name=StringField("Last Name: ",validators=[DataRequired(),Length(min=3, max=10)])
    email=StringField("Email: ",[validators.Email()])
    password=PasswordField("Password: ",validators=[DataRequired()])
    confirm_password=PasswordField("Confirm Password: ",validators=[DataRequired(),EqualTo('password')])
    ati=SelectField(choices=['KANDY'])
    possition=SelectField("Possision: ",choices=['OFFICE','HOD'],validators=[DataRequired()])
    department=SelectField("Department: ",choices=['IT','ACCOUNTANCY','MANAGEMENT','TOURISM','ENGLISH'],validators=[DataRequired()])
    submit=SubmitField("Submit")
 
#user SignUp
class UserSignUp(FlaskForm):
    first_name=StringField("First Name: ",validators=[DataRequired(),Length(min=3, max=10)])
    last_name=StringField("Last Name: ",validators=[DataRequired(),Length(min=3, max=10)])
    department=SelectField("Department: ",choices=['IT','ACCOUNTANCY','MANAGEMENT','TOURISM','ENGLISH'],validators=[DataRequired(),])
    email=StringField("Email: ",[validators.Email()])
    password=PasswordField("Password: ",validators=[DataRequired()])
    confirm_password=PasswordField("Confirm Password: ",validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField("Submit")

    
#Admin Interface
class AdminInterface(FlaskForm):
    edit_time_table=SubmitField("Click To Edit Time Tables:")
    display=SubmitField("Display Requests") 
    accept=SubmitField("Accept")
    all_accept=SubmitField("ALL Accept")
    reject=SubmitField("Reject")
    all_reject=SubmitField("ALL Reject")
    submit=SubmitField("Submit To HOD")
    abort=SubmitField("Abort")
    download=SubmitField("Download List")
    
    
    

#Super Admin Interface
class SuperAdminInterface(FlaskForm):
    edit_time_table=SubmitField("Click To Edit Time Tables:")
    display=SubmitField("Display Requests") 
    authenticate=SubmitField("Authenticate")
    all_authenticate=SubmitField("ALL Authenticate")
    reject=SubmitField("Reject")
    all_reject=SubmitField("ALL Reject")
    

#timetable

class TimeSchedule(FlaskForm):
    department=SelectField("Department",choices=['HNDIT','HNDTHM','HNDM','HNDE'])
    year=SelectField("Academic Year",choices=[1,2,3,4])
    semester=SelectField("Semester",choices=[1,2,3,4])
    submit=SubmitField('Show Table')
    
    # date=DateField()
    # start_time=TimeField("Start Time")
    # end_time=TimeField("End Time")
    # subject_code=SelectField("Subject Code",choices=['From Db'])
    # subject_name=SelectField('Subject Name',choices=['From DB'])
    # newSlot=SubmitField('New Slot')
   
