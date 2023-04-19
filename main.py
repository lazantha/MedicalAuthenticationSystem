from flask import Flask,render_template,url_for,redirect,flash
from flask import request
from allForms import UserLog,AdminSignUp,UserSignUp,UserForm,AdminInterface,SuperAdminInterface,TimeSchedule
from flask_bcrypt import Bcrypt
from database import MySql,host,database,user

app=Flask(__name__)
app.config['SECRET_KEY']="kEY"
bcrypt=Bcrypt(app)
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
@app.route('/userlog',methods=['GET','POST'])
def userlog():
    new_user=UserLog()
    if new_user.validate_on_submit():
        user_name=new_user.user_name.data
        password=new_user.password.data
        if user_name=='lasantha' and password=='lasa123':
            return redirect('request')
        else:
            return redirect('userlog')

    return render_template('logIn/user.html',form=new_user)


#admin login page
@app.route('/adminlog',methods=['GET','POST'])
def adminlog():
    new_admin=UserLog()
    if new_admin.validate_on_submit():
        user_name=new_admin.user_name.data
        password=new_admin.password.data
        possition=new_admin.possition.data
        if user_name == 'sansa' and password=='sansa123':
            if possition=='office':
                return redirect('adminpanel')
            else:
                return redirect('superAdminPanel')
            
        else:
            return redirect('adminlog')
            
    
        
    return render_template('login/admin.html',form=new_admin)
#about page
@app.route('/about')
def about():
    return render_template('about.html')
#contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

#user Sign
@app.route('/userSign',methods=['GET','POST'])
def userSign():
    new_user=UserSignUp()
    new_data=MySql()
    if new_user.validate_on_submit():
        first_name=new_user.first_name.data
        last_name=new_user.last_name.data
        department=new_user.department.data
        email=new_user.email.data
        password=new_user.password.data
        confirm=new_user.confirm.data
        query="INSERT INTO user (first_name,last_name,department,email,password,confirm_password)VALUES(%s,%s,%s,%s,%s,%s)"
        data=(first_name,last_name,department,email,password,confirm)
        new_data.table(query,data,host,database,user)
        return redirect(url_for('userlog'))
        
        
        
        
        
        
        
    return render_template('signup/user.html',form=new_user)

#admin Sign
@app.route('/adminSign',methods=['GET','POST'])
def adminSign():
    new_admin=AdminSignUp()
    new_data=MySql()

    if new_admin.validate_on_submit():
        first_name=new_admin.first_name.data
        last_name=new_admin.last_name.data
        email=new_admin.email.data
        password=new_admin.password.data
        confirm_password=new_admin.confirm_password.data
        ati=new_admin.ati.data
        possition=new_admin.possition.data
        query=" INSERT INTO admin (first_name,last_name,email,password,confirm_possword,ati,possition) VALUES(%s,%s,%s,%s,%s,%s,%s) "
        data=(first_name,last_name,email,password,confirm_password,ati,possition)
        new_data.table(query,data,host,database,user)
        return redirect(url_for('adminlog'))
        
        
        
        
        
    return render_template('signup/admin.html',form=new_admin)

#main form
@app.route('/request',methods=['GET','POST'])
def request():
    new_req_form=UserForm()
    return render_template('interfaces/user/mainform.html',form=new_req_form)



#adminPanel
@app.route('/adminPanel',methods=['GET','POST'])
def adminPanel():
    new_admin_panel=AdminInterface()
    return render_template('interfaces/admin/admin.html',form=new_admin_panel)

#superAdmin
@app.route('/superAdminPanel',methods=['GET','POST'])
def superAdminPanel():
    new_super=SuperAdminInterface()
    return render_template('interfaces/superAdmin/superAdmin.html',form=new_super)

@app.route('/timetable',methods=['GET','POST'])
def timeTable():
    new_time_table=TimeSchedule()
    return render_template('interfaces/admin/timetable.html',form=new_time_table)
