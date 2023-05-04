from flask import Flask,render_template,url_for,redirect,flash,session
from flask import request
from allForms import UserLog,AdminLog,AdminSignUp,UserSignUp,UserForm,AdminInterface,SuperAdminInterface,TimeSchedule
from flask_bcrypt import Bcrypt
from database import MySql,host,database,user
from datetime import datetime
from binaryFiles import Binary
import hashlib

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

# Sessions Admin logging out
@app.route('/adminLogOut')
def adminLogOut():
    pass

# Sessions  English Admin logging out
@app.route('/englishAdminLogOut')
def englishAdminLogOut():
    pass

# Sessions  account Admin logging out
@app.route('/accountAdminLogOut')
def accountAdminLogOut():
    pass

# Sessions  it Admin logging out
@app.route('/itAdminLogOut')
def itAdminLogOut():
    pass

# Sessions  management Admin logging out
@app.route('/managementAdminLogOut')
def managementAdminLogOut():
    pass

# Sessions  thm Admin logging out
@app.route('/thmAdminLogOut')
def thmAdminLogOut():
    pass


#password encryption method
def hashPassword(password):

	encode=hashlib.new('SHA256')
	encode.update(password.encode())
	hashed_password=encode.hexdigest()
	return hashed_password

#home page
@app.route('/')
def index():
    return render_template('index.html')

#...............................................................
#user login Page
@app.route('/userlog',methods=['GET','POST'])
def userlog():
    new_user=UserLog()
    new_data=MySql()
    if new_user.validate_on_submit():
        user_name=new_user.user_name.data
        password=new_user.password.data
        query="SELECT first_name,password FROM user WHERE first_name=%s AND password=%s"
        data=(user_name,password)
        exist=new_data.fetchAllMulForeing(query,data,host,database,user)
        if exist:
            return redirect(url_for('request'))
        else:
            return redirect(url_for('userlog'))
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
        admin_query="SELECT admin_id FROM admin WHERE possition=%s "
        admin_data=('OFFICE',)
        admin_id=new_sql.fetchOneForeing(admin_query,admin_data,host,database,user)
        main_query="INSERT INTO user(admin_id,first_name,last_name,department,email,password,confirm_password)VALUES(%s,%s,%s,%s,%s,%s,%s);"
        main_data=(admin_id,first_name,last_name,department,email,password,confirm_password)
        new_sql.table(main_query,main_data,host,database,user)
        return redirect('userlog')
        
    return render_template('signup/user.html',form=new_sign)

#...............................................................
@app.route('/user',methods=['GET','POST'])
def user():

    return render_template('interfaces/user/user_account.html')





#admin login page
@app.route('/adminlog',methods=['GET','POST'])
def adminlog():
    new_admin=AdminLog()
    new_data=MySql()
    if new_admin.validate_on_submit():
        user_name=new_admin.user_name.data
        password=new_admin.password.data
        possition=new_admin.possition.data
        department=new_admin.department.data
        query = "SELECT first_name,password FROM admin WHERE first_name = %s AND password = %s"
        data = (user_name, password)
        exist_data = new_data.fetchAllMulForeing(query, data, host, database, user)
        page_list={
            'IT':'superAdminPanelIt',
            'MANAGEMENT':'superAdminPanelManagement',
            'ACCOUNTANCY':'superAdminPanelAccount',
            'ENGLISH':'superAdminPanelEnglish',
            'TOURISM':'superAdminPanelThm'
        }
        if exist_data:
            if possition=="HOD":
                query_possition = "SELECT first_name,department FROM admin WHERE first_name= %s AND department= %s"
                data_possition = (user_name, department)
                exist_possition=new_data.fetchAllMulForeing(query_possition,data_possition,host,database,user)                
                if exist_possition:
                    page_name=page_list.get(department)
                    if page_name:
                        return redirect(url_for(page_name))
                    else:
                        return redirect(url_for('login'))
            else:
                return redirect(url_for('admin'))
        else:
            return redirect(url_for('login'))
     
    return render_template('login/admin.html',form=new_admin)


#admin Sign
@app.route('/adminSign',methods=['GET','POST'])
def adminSign():
    new_admin=AdminSignUp()
    new_data=MySql()
    possition="OFFICE"
    if new_admin.validate_on_submit():
        first_name=new_admin.first_name.data
        last_name=new_admin.last_name.data
        email=new_admin.email.data
        password=new_admin.password.data
        confirm_password=new_admin.confirm_password.data
        ati=new_admin.ati.data
        possition=new_admin.possition.data
        department=new_admin.department.data
        if possition=='OFFICE':
            department='ADMIN'
        if possition=='HOD':
            possition="HOD"
        
        query=" INSERT INTO admin (first_name,last_name,email,password,confirm_password,ati,possition,department) VALUES(%s,%s,%s,%s,%s,%s,%s,%s) "
        data=(first_name,last_name,email,password,confirm_password,ati,possition,department)
        new_data.table(query,data,host,database,user)
        flash(f'Account Successfully created {first_name}!','success')
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
    new_binary=Binary()
    if new_req_form.validate_on_submit():
        user_name=new_req_form.userName.data
        gender=new_req_form.gender.data
        course=new_req_form.course.data
        year=new_req_form.year.data
        semester=new_req_form.semester.data
        attempt=new_req_form.attempt.data
        start_date=new_req_form.start_date.data
        end_date=new_req_form.end_date.data
        date_issued=new_req_form.date_issued.data
        type=new_req_form.type.data
        med_pic=new_req_form.med_pic.data
        image=new_binary.convertToBinary(med_pic)    
        admin_query="SELECT admin_id FROM admin WHERE possition= %s"
        admin_data=('OFFICE',)
        admin_id=new_data.fetchOneForeing(admin_query,admin_data,host,database,user)
        user_query="SELECT user_id FROM user ORDER BY user_id DESC"
        user_id=new_data.fetchOne(user_query,host,database,user)
        main_query="INSERT INTO medical_infor(user_id,admin_id,name,gender,course,year,semester,attempt,date_begin,date_end,method,image,date_issued)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        main_data=(user_id,admin_id,user_name,gender,course,year,semester,attempt,start_date,end_date,type,med_pic,date_issued)
        new_data.table(main_query,main_data,host,database,user)
    return render_template('interfaces/user/mainform.html',form=new_req_form)


#office
@app.route('/admin',methods=['GET','POST'])
def admin():
    from flask import request

    action = request.args.get('action')
    print(action)

    new_admin=AdminInterface()
    new_data=MySql()
    query="SELECT COUNT(id)FROM medical_infor"
    count=new_data.fetchOne(query,host,database,user)
    it_query="SELECT COUNT(id) FROM medical_infor WHERE course =%s"
    it_data=('IT',)
    account_query="SELECT COUNT(id) FROM medical_infor WHERE course =%s"
    account_data=('ACCOUNTANCY',)
    manage_query="SELECT COUNT(id) FROM medical_infor WHERE course =%s"
    manage_data=('MANAGEMENT',)
    thm_query="SELECT COUNT(id) FROM medical_infor WHERE course =%s"
    thm_data=('TOURISM',)
    english_query="SELECT COUNT(id) FROM medical_infor WHERE course =%s"
    english_data=('ENGLISH',)
    it_count=new_data.fetchOneForeing(it_query,it_data,host,database,user)
    account_count=new_data.fetchOneForeing(account_query,account_data,host,database,user)
    manage_count=new_data.fetchOneForeing(manage_query,manage_data,host,database,user)
    thm_count=new_data.fetchOneForeing(thm_query,thm_data,host,database,user)
    english_count=new_data.fetchOneForeing(english_query,english_data,host,database,user)

    #main records
    main_query_it="SELECT name,gender,course FROM medical_infor WHERE course= %s"
    result_it=new_data.fetchAllMulForeing(main_query_it,it_data,host,database,user)
    main_query_account="SELECT name,gender,course FROM medical_infor WHERE course= %s"
    result_account=new_data.fetchAllMulForeing(main_query_account,account_data,host,database,user)    
    main_query_manage="SELECT name,gender,course FROM medical_infor WHERE course= %s"
    result_manage=new_data.fetchAllMulForeing(main_query_manage,manage_data,host,database,user)    
    main_query_thm="SELECT name,gender,course FROM medical_infor WHERE course= %s"
    result_thm=new_data.fetchAllMulForeing(main_query_thm,thm_data,host,database,user) 
    main_query_english="SELECT name,gender,course FROM medical_infor WHERE course= %s"
    result_english=new_data.fetchAllMulForeing(main_query_english,english_data,host,database,user)



    # if action=='accept':
    #     print(action)s
    

    #     new_data=MySql()
    #     admin="SELECT admin_id FROM admin WHERE first_name=%s"
    #     data=('arya',)
    #     admin_id=new_data.fetchOneForeing(admin,data,host,database,user)
    #     query="INSERT INTO admin_accountency(admin_id,name,year,semester,attempt,date_begin,date_end,method,image)SELECT admin_id,name,year,semester,attempt,date_begin,date_end,method,image FROM medical_infor WHERE admin_id=%s LIMIT =%s"
    #     data=(2,1)
    #     new_data.table(query,data,host,database,user)


    # elif action=='reject':
    #     pass

    


        # perform the reject action using the row_id


    return render_template('interfaces/admin/admin.html',form=new_admin,
                           count=count,it_count=it_count,account_count=account_count,
                           manage_count=manage_count,thm_count=thm_count,
                           english_count=english_count,
                           result_it=result_it,
                           result_account=result_account,
                           result_manage=result_manage,
                           result_thm=result_thm,
                           result_english=result_english
                           )



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

#superAdminThm
@app.route('/superAdminPanelThm',methods=['GET','POST'])
def superAdminPanelThm():
    new_super=SuperAdminInterface()
    return render_template('interfaces/superAdmin/thm.html',form=new_super)


#time schedule later
@app.route('/timetable',methods=['GET','POST'])
def timeTable():
    new_time_table=TimeSchedule()
    new_data=MySql()
    if new_time_table.validate_on_submit():
        department=new_time_table.department.data
        year=new_time_table.year.data
        semester=new_time_table.semester.data
        
    return render_template('interfaces/admin/timetable.html',form=new_time_table)
