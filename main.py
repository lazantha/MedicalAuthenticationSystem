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
    session.pop('user_name',None)
    return redirect(url_for('adminlog'))

# Sessions  English Admin logging out
@app.route('/englishAdminLogOut')
def englishAdminLogOut():
    session.pop('user_name',None)
    return redirect(url_for('adminlog'))

# Sessions  account Admin logging out
@app.route('/accountAdminLogOut')
def accountAdminLogOut():
    session.pop('user_name',None)
    return redirect(url_for('adminlog'))

# Sessions  it Admin logging out
@app.route('/itAdminLogOut')
def itAdminLogOut():
    session.pop('user_name',None)
    return redirect(url_for('adminlog'))
    


# Sessions  management Admin logging out
@app.route('/managementAdminLogOut')
def managementAdminLogOut():
    session.pop('user_name',None)
    return redirect(url_for('adminlog'))

# Sessions  thm Admin logging out
@app.route('/thmAdminLogOut')
def thmAdminLogOut():
    session.pop('user_name',None)
    return redirect(url_for('adminlog'))

@app.route('/userLogOut')
def userLogOut():
    session.pop('user',None)
    return redirect(url_for('userlog'))




#password encryption method
def setHash(password):

	template=hashlib.new('SHA256')
	template.update(password.encode())
	hashed_password=template.hexdigest()
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
        hashed_password=setHash(password)
        query="SELECT first_name,password FROM user WHERE first_name=%s AND password=%s"
        data=(user_name,hashed_password)
        exist=new_data.fetchAllMulForeing(query,data,host,database,user)
        
        if exist:
            session['name'] = user_name
            session['password']=hashed_password
            return redirect(url_for('user_home'))
            flash('Login Success ','success')
        else:
            if 'name' in session:
                return redirect(url_for('user_home'))
            return redirect(url_for('userlog'))
            flash('Please recheck user name and password','warning')
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
        hashed_password=setHash(password)
        confirm_password=new_sign.confirm_password.data
        hashed_password_confirm=setHash(confirm_password)

        if hashed_password==hashed_password_confirm:
            admin_query="SELECT admin_id FROM admin WHERE possition =%s;"
            admin_data=('OFFICE',)
            admin_id=(new_sql.fetchOneForeing(admin_query,admin_data,host,database,user))
    
            main_query="INSERT INTO user(admin_id,first_name,last_name,department,email,password,confirm_password)VALUES(%s,%s,%s,%s,%s,%s,%s);"
            main_data=(admin_id,first_name,last_name,department,email,hashed_password,hashed_password_confirm)
            new_sql.table(main_query,main_data,host,database,user)

            return redirect('userlog')
        else:
            return redirect('userSign')
        
    return render_template('signup/user.html',form=new_sign)

#...............................................................
@app.route('/user_home',methods=['GET','POST'])
def user_home():
    if 'name' in session and 'password' in session:
        new_data=MySql()
        name=session['name']
        password=session['password']
        
        query="SELECT mi.year,semester,subject,attempt FROM  medical_infor AS mi INNER JOIN user AS u ON mi.user_id=u.user_id WHERE u.first_name=%s AND password=%s "

        query_data=(name,password)
        
        result=new_data.fetchAllMulForeing(query,query_data,host,database,user)
        
        
        return render_template('interfaces/user/user_account.html',name=name,result=result)
    else:
        return redirect('userlog')





#admin login page
@app.route('/adminlog',methods=['GET','POST'])
def adminlog():
    new_admin=AdminLog()
    new_data=MySql()
    if new_admin.validate_on_submit():
        user_name=new_admin.user_name.data
        password=new_admin.password.data
        hashed_password=setHash(password)
        possition=new_admin.possition.data
        department=new_admin.department.data
        query = "SELECT first_name,password FROM admin WHERE first_name = %s AND password = %s"
        data = (user_name, hashed_password)
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
                    session['user_name']=user_name
                    page_name=page_list.get(department)
                    if page_name:
                        return redirect(url_for(page_name))
                    else:
                        return redirect(url_for('adminlog'))
            else:
                session['user_name']=user_name
                return redirect(url_for('admin'))
        else:
            return redirect(url_for('adminlog'))
     
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
        hashed_password=setHash(password)
        confirm_password=new_admin.confirm_password.data
        hashed_password_confirm=setHash(confirm_password)
        ati=new_admin.ati.data
        possition=new_admin.possition.data
        department=new_admin.department.data
        if possition=='OFFICE':
            department='ADMIN'
        if possition=='HOD':
            possition="HOD"
        
        if hashed_password==hashed_password_confirm:
            query=" INSERT INTO admin (first_name,last_name,email,password,confirm_password,ati,possition,department) VALUES(%s,%s,%s,%s,%s,%s,%s,%s) "
            data=(first_name,last_name,email,hashed_password,hashed_password_confirm,ati,possition,department)
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
    name=session['name']
    password=session['password']
    if new_req_form.validate_on_submit():
        user_name=new_req_form.userName.data
        gender=new_req_form.gender.data
        course=new_req_form.course.data
        subject=new_req_form.subject.data
        year=new_req_form.year.data
        semester=new_req_form.semester.data
        attempt=new_req_form.attempt.data
        start_date=new_req_form.start_date.data
        end_date=new_req_form.end_date.data
        date_issued=new_req_form.date_issued.data
        type=new_req_form.type.data
        red_book=new_req_form.red_book.data
        med_pic=new_req_form.med_pic.data
        image=new_binary.convertToBinary(med_pic)    
        admin_query="SELECT admin_id FROM admin WHERE possition= %s"
        admin_data=('OFFICE',)
        admin_id=new_data.fetchOneForeing(admin_query,admin_data,host,database,user)
        print(admin_id)
        user_query="SELECT user_id FROM user WHERE first_name=%s AND password =%s"
        user_data=(name,password)
        user_id=new_data.fetchOneForeing(user_query,user_data,host,database,user)
        print(user_id)
        main_query="INSERT INTO medical_infor(user_id,admin_id,name,gender,course,subject,year,semester,attempt,date_begin,date_end,method,id_image,med_image,date_issued)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        main_data=(user_id,admin_id,user_name,gender,course,subject,year,semester,attempt,start_date,end_date,type,red_book,med_pic,date_issued)
        new_data.table(main_query,main_data,host,database,user)
        return redirect(url_for('user_home'))
    return render_template('interfaces/user/mainform.html',form=new_req_form)


#office
@app.route('/admin',methods=['GET','POST'])
def admin():
    from flask import request
    if 'user_name' in session:
                user_name=session['user_name']
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
                main_query_it="SELECT name,gender,course id_image,med_image FROM medical_infor WHERE course= %s"
                result_it=new_data.fetchAllMulForeing(main_query_it,it_data,host,database,user)
                main_query_account="SELECT name,gender,course id_image,med_image FROM medical_infor WHERE course= %s"
                result_account=new_data.fetchAllMulForeing(main_query_account,account_data,host,database,user)    
                main_query_manage="SELECT name,gender,course id_image,med_image FROM medical_infor WHERE course= %s"
                result_manage=new_data.fetchAllMulForeing(main_query_manage,manage_data,host,database,user)    
                main_query_thm="SELECT name,gender,course id_image,med_image FROM medical_infor WHERE course= %s"
                result_thm=new_data.fetchAllMulForeing(main_query_thm,thm_data,host,database,user) 
                main_query_english="SELECT name,gender,course id_image,med_image FROM medical_infor WHERE course= %s"
                result_english=new_data.fetchAllMulForeing(main_query_english,english_data,host,database,user)
                action = request.args.get('action')
                def actionSelection(action):
                    if action=='itAccept':
                        query="INSERT INTO admin_it(admin_id,name,year,semester,subject,attempt,date_begin,date_end,method,image,date_issued)SELECT admin_id,name,year,semester,subject,attempt,date_begin,date_end,method,med_image,date_issued FROM medical_infor LIMIT 1"
                        new_data.insertData(query,host,database,user)
                        dltQuery="DELETE  FROM medical_infor WHERE course='IT'  ORDER BY time ASC LIMIT 1 "
                        new_data.delete(dltQuery,host,database,user)



                    elif action=='itReject':
                        # dltQuery="DELETE  FROM medical_infor WHERE course='IT'  ORDER BY time ASC LIMIT 1 "
                        # new_data.delete(dltQuery,host,database,user)
                        pass


                    elif action=='accAccept':
                        query="INSERT INTO admin_accountency(admin_id,name,year,semester,subject,attempt,date_begin,date_end,method,image,date_issued)SELECT admin_id,name,year,semester,subject,attempt,date_begin,date_end,method,med_image,date_issued FROM medical_infor LIMIT 1"
                        new_data.insertData(query,host,database,user)
                        

                    elif action=='accReject':
                        pass

                    elif action=='manaAccept':
                        query="INSERT INTO admin_management(admin_id,name,year,semester,subject,attempt,date_begin,date_end,method,image,date_issued)SELECT admin_id,name,year,semester,subject,attempt,date_begin,date_end,method,med_image,date_issued FROM medical_infor LIMIT 1"
                        new_data.insertData(query,host,database,user)
                        

                    elif action=='manaReject':
                        pass
                    elif action=='thmAccept':
                        query="INSERT INTO admin_thm(admin_id,name,year,semester,subject,attempt,date_begin,date_end,method,image,date_issued)SELECT admin_id,name,year,semester,subject,attempt,date_begin,date_end,method,med_image,date_issued FROM medical_infor LIMIT 1"
                        new_data.insertData(query,host,database,user)
                        

                    elif action=='thmReject':
                        pass

                    
                    elif action=='engAccept':
                        query="INSERT INTO admin_english(admin_id,name,year,semester,subject,attempt,date_begin,date_end,method,image,date_issued)SELECT admin_id,name,year,semester,subject,attempt,date_begin,date_end,method,med_image,date_issued FROM medical_infor LIMIT 1"
                        new_data.insertData(query,host,database,user)

                    elif action=='engReject':
                        pass
                    actionSelection(action)

    return render_template('interfaces/admin/admin.html',form=new_admin,
                           count=count,it_count=it_count,account_count=account_count,
                           manage_count=manage_count,thm_count=thm_count,
                           english_count=english_count,
                           result_it=result_it,
                           result_account=result_account,
                           result_manage=result_manage,
                           result_thm=result_thm,
                           result_english=result_english,
                           user_name=user_name
                           )



#superAdminIt
@app.route('/superAdminPanelIt',methods=['GET','POST'])
def superAdminPanelIt():
    if 'user_name' in session:
        user_name=session['user_name']
        new_super=SuperAdminInterface()
        new_data=MySql()
        count="SELECT COUNT(*) FROM `admin_it`"
        count=new_data.fetchOne(count,host,database,user)

        query="SELECT name,subject,image FROM admin_it "
        result=new_data.fetchMultiVal(query,host,database,user)
        return render_template('interfaces/superAdmin/it.html',form=new_super,user_name=user_name,count=count,result=result)
    else:
        return redirect('adminlog')
    

#superAdminAccount
@app.route('/superAdminPanelAccount',methods=['GET','POST'])
def superAdminPanelAccount():
    if 'user_name' in session:
        user_name=session['user_name']
        new_super=SuperAdminInterface()
        new_data=MySql()
        count="SELECT COUNT(*) FROM `admin_accountency`"
        count=new_data.fetchOne(count,host,database,user)

        query="SELECT name,subject,image FROM admin_accountency"
        result=new_data.fetchMultiVal(query,host,database,user)
        return render_template('interfaces/superAdmin/account.html',form=new_super,user_name=user_name,count=count,result=result)
    else:
        return redirect('adminlog')

#superAdmManagement
@app.route('/superAdminPanelManagement',methods=['GET','POST'])
def superAdminPanelManagement():
    if 'user_name' in session:
        user_name=session['user_name']
        new_super=SuperAdminInterface()
        new_data=MySql()
        count="SELECT COUNT(*) FROM `admin_management`"
        count=new_data.fetchOne(count,host,database,user)

        query="SELECT name,subject,image FROM admin_management"
        result=new_data.fetchMultiVal(query,host,database,user)
        return render_template('interfaces/superAdmin/management.html',form=new_super,user_name=user_name,count=count,result=result)
    else:
        return redirect('adminlog')

#superAdminEnglish
@app.route('/superAdminPanelEnglish',methods=['GET','POST'])
def superAdminPanelEnglish():
    if 'user_name' in session:
        user_name=session['user_name']
        new_super=SuperAdminInterface()
        new_data=MySql()
        count="SELECT COUNT(*) FROM `admin_english`"
        count=new_data.fetchOne(count,host,database,user)

        query="SELECT name,subject,image FROM admin_english"
        result=new_data.fetchMultiVal(query,host,database,user)
        return render_template('interfaces/superAdmin/english.html',form=new_super,user_name=user_name,count=count,result=result)
    else:
        return redirect('adminlog')

#superAdminThm
@app.route('/superAdminPanelThm',methods=['GET','POST'])
def superAdminPanelThm():
    if 'user_name' in session:
        user_name=session['user_name']
        new_super=SuperAdminInterface()
        new_data=MySql()
        count="SELECT COUNT(*) FROM `admin_thm`"
        count=new_data.fetchOne(count,host,database,user)

        query="SELECT name,subject,image FROM admin_thm"
        result=new_data.fetchMultiVal(query,host,database,user)
        return render_template('interfaces/superAdmin/thm.html',form=new_super,user_name=user_name,count=count,result=result)
    else:
        return redirect('adminlog')


#time schedule later
# @app.route('/timetable',methods=['GET','POST'])
# def timeTable():
#     from flask import request
#     new_time_table=TimeSchedule()
#     new_data=MySql()
#     action = request.args.get('action')
#     if new_time_table.validate_on_submit():
#         department=new_time_table.department.data
#         year=new_time_table.year.data
#         semester=new_time_table.semester.data
#         if department == 'HNDIT':
#             # query="INSRT INTO it (year,semester) VALUES(%s,%s);"
#             # data=(year,semester)
#             # new_data.table(query,data,host,database,user)
#             if action=='insert':
#                 subject_name=new_time_table.subject_name.data
#                 subject_code=new_time_table.subject_code.data
#                 date=new_time_table.date.data
#                 start_time=new_time_table.start_time.data
#                 end_time=new_time_table.end_time.data            
#                 idquery='SELECT id FROM it WHERE year=%s AND semester=%s'
#                 idData=(year,semester)
#                 itId=new_data.fetchOneForeing(idquery,idData,host,database,user)
#                 adminQuery='SELECT admin_id FROM admin WHERE admin_id=%s'
#                 adminData=(1,)
#                 adminId=new_data.fetchOneForeing(adminQuery,adminData,host,database,user)

#                 mainQuery='INSERT INTO subject(it,subject_name,subject_code,date,start_time,end_time,admin_id)VALUES(%s,%s,%s,%s,%s,%s,%s);'
#                 mainData=(itId,subject_name,subject_code,date,start_time,end_time,adminId)
#                 new_data.table(mainQuery,mainData,host,database,user)



#         elif department == 'HNDTHM':
#             pass

#         elif department == 'HNDM':
#             pass

#         elif department == 'HNDE':
#             pass
        
        
#     return render_template('interfaces/admin/timetable.html',form=new_time_table)

#time schedule 


@app.route('/timetable', methods=['GET', 'POST'])
def timeTable():
    new_time_table = TimeSchedule()
    from flask import request
    action = request.args.get('action')
    row = request.args.get('row')
    
    
    new_data = MySql()
    
    
    return render_template('interfaces/admin/timetable.html', form=new_time_table)

   