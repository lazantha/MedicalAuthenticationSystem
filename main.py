from flask import Flask,render_template,url_for
app=Flask(__name__)

#error handling 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errorhandler/404.html'), 404
#error handling 500
def internal_server_error(e):
  return render_template('errorhandler/500.html'), 500
#home page
@app.route('/')
def index():
    return render_template('index.html')
#user login Page
@app.route('/userlog')
def userlog():
    return render_template('login/user.html')

#admin login page
@app.route('/adminlog')
def adminlog():
    return render_template('login/admin.html')
#about page
@app.route('/about')
def about():
    return render_template('about.html')
#contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

from wtforms import Form,StringField,validators,SelectField,TextAreaField,DateTimeField,DateField,RadioField,FileField,validators,SubmitField
#FileField for picture
class UserForm(Form):
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

#user main form 
@app.route('/user',methods=['GET,POST'])
def user():
    form=UserForm()
    return render_template('users/frmUser.html',form=form)

