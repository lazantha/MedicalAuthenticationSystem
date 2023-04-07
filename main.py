from flask import Flask,render_template,url_for,request,redirect,flash
from allForms import UserLog
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
    return render_template('signup/user.html')

#admin Sign
@app.route('/adminSign')
def adminSign():
    return render_template('signup/admin.html')


