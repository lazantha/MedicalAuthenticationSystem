from flask import Flask,render_template,url_for,request,redirect,Flask
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
    # if request.method=='POST':
    #     user_name=request.form['user_name']
    #     password=request.form['password']


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


@app.route('/user')
def user():
    # form=UserForm()
    # if form.method==['POST']:
    #     if form.validate_on_submit():
    #         name=form.userName.data

    return render_template('users/frmUser.html')

