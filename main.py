from flask import Flask,render_template,url_for,redirect,flash
from flask import request
from allForms import UserLog,AdminLog,AdminSignUp,UserSignUp,UserForm,AdminInterface,SuperAdminInterface,TimeSchedule
from flask_bcrypt import Bcrypt
from database import MySql,host,database,user
from datetime import datetime

app=Flask(__name__)
app.config['SECRET_KEY']="kEY"
bcrypt=Bcrypt(app)
#...............................................................
#error handling 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errorhandler/404.html'), 404
#error handling 500
def internal_server_error(e):
  return render_template('errorhandler/500.html'), 500
#...............................................................

#home page
@app.route('/')
def index():
    return render_template('index.html')

#...............................................................
#user login Page
@app.route('/userlog',methods=['GET','POST'])
def userlog():
    new_user=UserLog()
    new_row=MySql()
    if new_user.validate_on_submit():
        user_name=new_user.user_name.data
        password=new_user.password.data
        data_name=(user_name)
        data_password=(password)
        query_1="SELECT first_name FROM user WHERE first_name=%s"
        query_2="SELECT passowrd FROM user WHERE first_name=%s"
        
        name=new_row.getData(query_1,data_name,host,database,user)
        print(name)
        
        password=new_row.getData(query_2,data_password,host,database,user)
        print(password)
        if user_name==name and password==password:
            return redirect('request')
        else:
            return redirect('userlog')
        
        

    return render_template('login/user.html',form=new_user)

#user Sign
@app.route('/userSign',methods=['GET','POST'])
def userSign():
    new_sign=UserSignUp()
    new_sql=MySql()
    if new_sign.validate_on_submit():
        first_name=new_sign.first_name.data
        last_name=new_sign.last_name.data
        department=new_sign.department.data
        email=new_sign.email.data
        password=new_sign.password.data
        confirm_password=new_sign.confirm_password.data
        query="INSERT INTO user(first_name,last_name,department,email,password,confirm_password)VALUES(%s,%s,%s,%s,%s,%s);"
        data=(first_name,last_name,department,email,password,confirm_password)
        new_sql.table(query,data,host,database,user)
        return redirect('userlog')
        
    return render_template('signup/user.html',form=new_sign)

#...............................................................




#admin login page
@app.route('/adminlog',methods=['GET','POST'])
def adminlog():
    new_admin=AdminLog()
    if new_admin.validate_on_submit():
        user_name=new_admin.user_name.data
        password=new_admin.password.data
        possition=new_admin.possition.data
        if user_name == 'sansa' and password=='sansa123':
            if possition=="OFFICE":
                return redirect('adminPanel')
            else:
                return redirect('superAdminPanel')
            
        else:
            return redirect('adminlog')
            
    
        
    return render_template('login/admin.html',form=new_admin)


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
        query=" INSERT INTO admin (first_name,last_name,email,password,confirm_password,ati,possition) VALUES(%s,%s,%s,%s,%s,%s,%s) "
        data=(first_name,last_name,email,password,confirm_password,ati,possition)
        new_data.table(query,data,host,database,user)
        return redirect(url_for('adminlog'))
        
        
        
        
        
    return render_template('signup/admin.html',form=new_admin)



#..............................................................................
#about page
@app.route('/about')
def about():
    return render_template('about.html')
#contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')
#..............................................................................




#main form
@app.route('/request',methods=['GET','POST'])
def request():
    new_req_form=UserForm()
    new_data=MySql()
    if new_req_form.validate_on_submit():
        user_name=new_req_form.userName.data
        course=new_req_form.course.data
        year=new_req_form.year.data
        semester=new_req_form.semester.data
        attempt=new_req_form.attempt.data
        start_date=new_req_form.start_date.data
        end_date=new_req_form.end_date.data
        date_issued=new_req_form.date_issued.data
        type=new_req_form.type.data
        med_pic=new_req_form.med_pic.data
        query="INSERT INTO medical_infor (name,course,year,semester,attempt,date_begin,date_end,method,image,date_issued)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        data=(user_name,course,year,semester,attempt,start_date,end_date,type ,med_pic,date_issued)
        new_data.table(query,data,host,database,user)
        return redirect('request')
        
        
        
        
        
        
        
        
        
        
        
        
        

    return render_template('interfaces/user/mainform.html',form=new_req_form)




#superAdminIt
@app.route('/superAdminPanelIt',methods=['GET','POST'])
def superAdminPanelIt():
    new_super=SuperAdminInterface()
    return render_template('interfaces/superAdmin/it.html',form=new_super)

#superAdminAccount
@app.route('/superAdminPanelAccount',methods=['GET','POST'])
def superAdminPanelAccount():
    new_super=SuperAdminInterface()
    return render_template('interfaces/superAdmin/account.html',form=new_super)


#superAdmManagement
@app.route('/superAdminPanelManagement',methods=['GET','POST'])
def superAdminPanelManagement():
    new_super=SuperAdminInterface()
    return render_template('interfaces/superAdmin/management.html',form=new_super)

#superAdminEnglish
@app.route('/superAdminPanelEnglish',methods=['GET','POST'])
def superAdminPanelEnglish():
    new_super=SuperAdminInterface()
    return render_template('interfaces/superAdmin/english.html',form=new_super)

#superAdmin
@app.route('/superAdminPanelThm',methods=['GET','POST'])
def superAdminPanelThm():
    new_super=SuperAdminInterface()
    return render_template('interfaces/superAdmin/thm.html',form=new_super)


#time schedule
@app.route('/timetable',methods=['GET','POST'])
def timeTable():
    new_time_table=TimeSchedule()
    return render_template('interfaces/admin/timetable.html',form=new_time_table)
