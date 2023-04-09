from flask import Flask,render_template,url_for,request,redirect,flash
from allForms import UserLog,AdminSignUp,UserSignUp,UserForm,AdminInterface
app=Flask(__name__)
app.config['SECRET_KEY']="kEY"

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
    new_user=UserLog()
    return render_template('logIn/user.html',form=new_user)


#admin login page
@app.route('/adminlog')
def adminlog():
    new_user=UserLog()
    return render_template('login/admin.html',form=new_user)
#about page
@app.route('/about')
def about():
    return render_template('about.html')
#contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

#user Sign
@app.route('/userSign')
def userSign():
    new_user=UserSignUp()
    return render_template('signup/user.html',form=new_user)

#admin Sign
@app.route('/adminSign')
def adminSign():
    new_admin=AdminSignUp()
    return render_template('signup/admin.html',form=new_admin)

#main form
@app.route('/request')
def request():
    new_req_form=UserForm()
    return render_template('mainForm/mainform.html',form=new_req_form)



#adminPanel
@app.route('/adminPanel')
def adminPanel():
    new_admin_panel=AdminInterface()
    return render_template('interfaces/admin/admin.html',form=new_admin_panel)

#superAdmin
@app.route('/superAdminPanel')
def superAdminPanel():
    return render_template('interfaces/superAdmin/superAdmin.html')