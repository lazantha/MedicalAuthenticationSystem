from flask import Flask,render_template,url_for,redirect,flash,session
from flask import jsonify,request
from allForms import UserLog,AdminLog,AdminSignUp,UserSignUp,UserForm,AdminInterface,SuperAdminInterface,TimeSchedule
from flask_bcrypt import Bcrypt
from database import MySql
from email_processor import email
from datetime import datetime
from binaryFiles import Binary
from logger import logging
from flask_mail import Mail,Message
import hashlib
from werkzeug.utils import secure_filename
import uuid
import os
host='localhost'
database='test_medical_db'
user='root'

app=Flask(__name__)

app.config['SECRET_KEY']="kEY"
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
#admin login page


@app.route('/adminlog',methods=['GET','POST'])
def adminlog():
    form=AdminLog()
    new_data=MySql(host,database,user)
    query="SELECT calling_name FROM departments;"
    department_list=new_data.fetchMultiVal(query)
    cleaned_data = [value[0].decode() for value in department_list]
    form.department.choices=cleaned_data
    if form.validate_on_submit():
        name=form.user_name.data
        password=form.password.data
        possition=form.possition.data
        department=form.department.data
        hashed_password=setHash(password)
        if possition=='HOD':
            
           
            query="SELECT sa.first_name,sa.password,dep.calling_name FROM super_admins AS sa INNER JOIN departments AS dep ON sa.dep_id=dep.id WHERE sa.first_name=%s AND sa.password=%s AND dep.calling_name=%s;"
            data=(name,hashed_password,department)
            exist_data=new_data.fetchAllMulForeing(query,data)
            if exist_data:
                
                session['super_name']=name
                session['super_password']=hashed_password
                
                page_list = {
                    'IT': 'itPanel',
                    'MANAGEMENT': 'managePanel',
                    'ACCOUNTANCY': 'accountPanel',
                    'ENGLISH': 'englishPanel',
                    'TOURISM': 'thmPanel'
                }
                page_name=page_list.get(department)
                if page_name:
                    
                    return redirect(url_for(page_name))
                else:
                    
                    return redirect('adminlog')
            else:
                return redirect('adminlog')
        
        else:
            
            #admin
            query="SELECT first_name,password FROM admins WHERE first_name=%s AND password=%s;"
            data=(name,hashed_password)
            print(data)
            exist_data=new_data.fetchAllMulForeing(query,data)
            print(exist_data)
            if exist_data:
                session['admin_name']=name
                session['admin_password']=hashed_password
                if 'admin_name' in session:
                    admin_name=session['admin_name']
                    return redirect(url_for('admin'))
            else:
                return redirect(url_for('adminlog'))
        

            
            


    return render_template('login/admin.html',form=form)


#super admins panels
#...............................................................................
@app.route('/itPanel',methods=['GET','POST'])
def itPanel():
    form=SuperAdminInterface()

    return render_template('interfaces/superAdmin/it.html',form=form)

@app.route('/managePanel',methods=['GET','POST'])
def managePanel():
    form=SuperAdminInterface()

    return render_template('interfaces/superAdmin/management.html',form=form)

@app.route('/accountPanel',methods=['GET','POST'])
def accountPanel():
    form=SuperAdminInterface()

    return render_template('interfaces/superAdmin/account.html',form=form)


@app.route('/englishPanel',methods=['GET','POST'])
def englishPanel():
    form=SuperAdminInterface()

    return render_template('interfaces/superAdmin/english.html',form=form)

@app.route('/thmPanel',methods=['GET','POST'])
def thmPanel():
    form=SuperAdminInterface()

    return render_template('interfaces/superAdmin/thm.html',form=form)


#...............................................................................

#admin Sign
@app.route('/adminSign',methods=['GET','POST'])
def adminSign():
    form=AdminSignUp()
    new_data=MySql(host,database,user)
    query="SELECT calling_name FROM departments;"
    department_list=new_data.fetchMultiVal(query)
    cleaned_data = [value[0].decode() for value in department_list]
    form.department.choices=cleaned_data
    
    if form.validate_on_submit():
        first_name=form.first_name.data
        last_name=form.last_name.data
        gender=form.gender.data
        email=form.email.data
        password=form.password.data
        possition=form.possition.data
        department=form.department.data
        hashed_password=setHash(password)
        
        if possition=="OFFICE":

            query="INSERT INTO admins (first_name,last_name,gender,email,password)VALUES(%s,%s,%s,%s,%s);"
            data=(first_name,last_name,gender,email,hashed_password)
            new_data.table(query,data)

            flash(f'Account Successfully created {first_name}!','success')
            return redirect(url_for('adminlog'))
        else:
            dep_query="SELECT id FROM departments WHERE calling_name =%s;"
            dep_data=(department,)
            dep_id=new_data.fetchOneForeing(dep_query,dep_data)
            query="INSERT INTO super_admins (dep_id,first_name,last_name,gender,email,password)VALUES(%s,%s,%s,%s,%s,%s);"
            data=(dep_id,first_name,last_name,gender,email,hashed_password)
            new_data.table(query,data)
            flash(f'Account Successfully created {first_name}!','success')
            return redirect(url_for('adminlog'))

        
        
    else:
        pass

        # print("Validation failed")
        # print(form.errors)

    
           
    return render_template('signup/admin.html',form=form)

#user login Page
@app.route('/userlog',methods=['GET','POST'])
def userlog():
    new_user=UserLog()
    new_data=MySql(host,database,user)
    if new_user.validate_on_submit():
        user_name=new_user.user_name.data
        password=new_user.password.data
        hashed_password=setHash(password)
        query="SELECT first_name,password FROM students WHERE first_name=%s AND password=%s"
        data=(user_name,hashed_password)
        exist=new_data.fetchAllMulForeing(query,data)
        
        if exist:
            session['student_name'] = user_name
            session['student_password']=hashed_password
            flash('Login Success ','success')
            return redirect(url_for('user_home'))
            
        else:
             flash('Please recheck user name and password','warning')
             return redirect(url_for('userlog'))
            # if 'name' in session:
            #     return redirect(url_for('user_home'))
            # return redirect(url_for('userlog'))
        
            # flash('Please recheck user name and password','warning')
    return render_template('login/user.html',form=new_user)

#user Sign
@app.route('/userSign',methods=['GET','POST'])
def userSign():
    new_sign=UserSignUp()
    new_sql=MySql(host,database,user)
    #department query
    query="SELECT calling_name FROM departments;"
    department_list=new_sql.fetchMultiVal(query)
    cleaned_data = [value[0].decode() for value in department_list]
    new_sign.department.choices=cleaned_data
    query="SELECT type FROM student_type;"
    student_type=new_sql.fetchMultiVal(query)
    cleaned_data = [value[0].decode() for value in student_type]
    new_sign.mode.choices=cleaned_data

    
    if new_sign.validate_on_submit():
        first_name=new_sign.first_name.data
        last_name=new_sign.last_name.data
        index_number=new_sign.index_number.data
        mode=new_sign.mode.data
        mode_query="SELECT id FROM student_type WHERE type=%s;"
        mode_data=(mode,)
        mode_id=new_sql.fetchOneForeing(mode_query,mode_data)
        gender=new_sign.gender.data
        department=new_sign.department.data
        dep_query="SELECT id FROM departments WHERE calling_name=%s;"
        dep_data=(department,)
        dep_id=new_sql.fetchOneForeing(dep_query,dep_data)   
        email=new_sign.email.data
        password=new_sign.password.data
        hashed_password=setHash(password)
        confirm_password=new_sign.confirm_password.data
        hashed_password_confirm=setHash(confirm_password)
        id_card=new_sign.id_card.data
        
        if hashed_password==hashed_password_confirm:
            # Grab image name
            img_name = secure_filename(id_card.filename)
            uniq_name = str(uuid.uuid1()) + '_' + img_name
            # Save image
            save_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], uniq_name)
            id_card.save(save_path)
            # Save to db
            id_card = uniq_name

            
            main_query="INSERT INTO students(department_id,student_type_id,first_name,last_name,index_number,gender,email,password,id_card)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            main_data=(dep_id,mode_id,first_name,last_name,index_number,gender,email,hashed_password_confirm,id_card)
            new_sql.table(main_query,main_data)
            return redirect('userlog')

        
        else:
            return redirect('userSign')
        
    return render_template('signup/user.html',form=new_sign)

#...............................................................
@app.route('/user_home',methods=['GET','POST'])
def user_home():
    if 'student_name' in session and 'student_password' in session:
        new_data=MySql(host,database,user)
        name=session['student_name']
        password=session['student_password']
        data=(name,password)
        # main_query="SELECT s.year,semester,subject_name,mi.attempt FROM users AS u INNER JOIN medical_infor AS mi ON u.user_id=mi.user_id INNER JOIN subjects AS s ON s.medical_id=mi.id WHERE u.first_name=%s AND u.password=%s"
        # result=new_data.fetchAllMulForeing(main_query,data)
        # cleaned_values = [
        #             tuple(value.decode('utf-8') if isinstance(value, bytearray) else value for value in row)
        #             for row in result
        #             ]
        
        query="SELECT s.saved_time FROM users AS u INNER JOIN medical_infor AS mi ON u.user_id=mi.user_id INNER JOIN subjects AS s ON mi.id=s.medical_id WHERE u.first_name=%s AND u.password=%s ORDER BY s.saved_time DESC LIMIT 1;"
        # last_saved=new_data.fetchOneForeing(query,data,host,database,user)
        last_saved=0
        
        # query="SELECT mi.year,semester,subject,attempt FROM  medical_infor AS mi INNER JOIN user AS u ON mi.user_id=u.user_id WHERE u.first_name=%s AND password=%s "

        # query_data=(name,password)
        
        # result=new_data.fetchAllMulForeing(query,query_data,host,database,user)
        # cleaned_result = [ (str(year), str(semester), subject.decode('utf-8'),str(attempt)) for year,semester,subject,attempt in result]
        #l
        return render_template('interfaces/user/user_account.html',name=name,
                            #    last_update=last_saved,
                            #    result=cleaned_values

                               )
    else:
        return redirect('userlog')








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
@app.route('/request_form',methods=['GET','POST'])
def request():
    from flask import request
    new_form=UserForm()
    new_data=MySql(host,database,user)
    new_binary=Binary()
    query="SELECT attempt FROM attempts;"
    attempts = new_data.fetchMultiVal(query)
    cleaned_data = [str(value[0].decode()) if isinstance(value[0], bytes) else str(value[0]) for value in attempts]
    new_form.attempt.choices=cleaned_data
    query="SELECT type FROM medical_type;"
    types=new_data.fetchMultiVal(query)
    cleaned_data = [value[0].decode() for value in types]
    new_form.med_type.choices=cleaned_data
    if 'student_name' in session and 'student_password' in session:
        name=session['student_name']
        password=session['student_password']
        query="SELECT dep.calling_name FROM departments AS dep INNER JOIN students AS s ON dep.id=s.department_id WHERE s.first_name=%s AND password=%s;"
        data=(name,password)
        department=new_data.fetchOneForeing(query,data).decode().strip()
        user_query="SELECT user_id FROM students WHERE first_name=%s AND password=%s;"
        user_id=new_data.fetchOneForeing(user_query,data)
        
        years=new_data.getUniqeCountYear(department) 
        years = [x[0] for x in years]
        new_form.year.choices=years
        semester=new_data.getUniqeCountSem(department)
        sem = [x[0] for x in semester]
        new_form.semester.choices=sem
        subject_list=new_data.getUniqeCountSub(department)
        subjects = [item[0].decode() for item in subject_list]
        new_form.subject.choices=subjects
        if new_form.validate_on_submit():
            
            date_issued=new_form.date_issued.data
            start_date=new_form.start_date.data
            end_date=new_form.end_date.data
            attempt=new_form.attempt.data
            doc_name=new_form.doc_name.data
            hospital=new_form.hospital.data
            med_type=new_form.med_type.data
            med_image=new_form.med_image.data
            year=new_form.year.data
            semester=new_form.semester.data
            subject=new_form.subject.data
            med_query="SELECT id FROM medical_type WHERE type=%s;"
            med_data=(med_type,)
            med_id=new_data.fetchOneForeing(med_query,med_data)
            attempt_query="SELECT id FROM attempts WHERE attempt=%s;"
            att_data=(attempt,)
            att_id=new_data.fetchOneForeing(attempt_query,att_data)
            sub_query="SELECT subject_id FROM subjects WHERE subject_name =%s;"
            sub_data=(subject,)
            sub_id=new_data.fetchOneForeing(sub_query,sub_data)
            #get values from exams acording to subject
            exam_query="SELECT held_date FROM exams WHERE subject_id=%s;"
            s_time_query="SELECT start_time FROM exams WHERE subject_id=%s;"
            e_time_query="SELECT end_time FROM exams WHERE subject_id=%s;"
            location_query="SELECT location FROM exams WHERE subject_id=%s;"
            med_data=(sub_id,)
            exam_date=new_data.fetchOneForeing(exam_query,med_data)
            start_time=new_data.fetchOneForeing(s_time_query,med_data)
            end_time=new_data.fetchOneForeing(e_time_query,med_data)
            location=new_data.fetchOneForeing(location_query,med_data).decode().strip()
            print(f"{exam_date}: {start_time}: {end_time}: {location}")


            
            
            


            
            # Grab image name
            img_name = secure_filename(med_image.filename)
            uniq_name = str(uuid.uuid1()) + '_' + img_name
            # Save image
            save_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], uniq_name)
            med_image.save(save_path)
            # Save to db
            med_image = uniq_name
            
            main_query="INSERT INTO medical_infor(user_id,med_type_id,subject_id,attempt_id,exam_date,started_time,end_time,exam_location,issued_date,from_date,to_date,doctor_name,hospital,medical_sheet)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            main_data=(user_id,med_id,sub_id,att_id,exam_date,start_time,end_time,location,date_issued,start_date,end_date,doc_name,hospital,med_image)
            new_data.table(main_query,main_data)
            
            flash("Form Susscessfully Submited ! We will notify you once your form has been accepted.")
            return redirect(url_for('user_home'))
        return render_template('interfaces/user/mainform.html',form=new_form)


#office
@app.route('/admin',methods=['GET','POST'])
def admin():
    from flask import request
    if 'admin_name' in session:
                user_name=session['admin_name']
                new_admin=AdminInterface()
                new_data=MySql(host,database,user)
                query="SELECT COUNT(*) FROM medical_infor;"
                total=new_data.fetchOne(query)
                it=new_data.getCount('IT')
                acc=new_data.getCount('ACCOUNTANCY')
                mng=new_data.getCount('MANAGEMENT')                
                eng=new_data.getCount('ENGLISH')
                thm=new_data.getCount('TOURISM')

            #main records
                result_it=new_data.getMain('IT')
                result_acc=new_data.getMain('ACCOUNTANCY')
                result_mng=new_data.getMain('MANAGEMENT')                
                result_eng=new_data.getMain('ENGLISH')
                result_thm=new_data.getMain('TOURISM')
                
                cleaned_values_it = [
                    tuple(value.decode('utf-8') if isinstance(value, bytearray) else value for value in row)
                    for row in result_it
                    ]
                
                cleaned_values_acc = [
                    tuple(value.decode('utf-8') if isinstance(value, bytearray) else value for value in row)
                    for row in result_acc
                    ]
                
                cleaned_values_mng = [
                    tuple(value.decode('utf-8') if isinstance(value, bytearray) else value for value in row)
                    for row in result_mng
                    ]
                
                
                cleaned_values_eng = [
                    tuple(value.decode('utf-8') if isinstance(value, bytearray) else value for value in row)
                    for row in result_eng
                    ]
                
                cleaned_values_thm = [
                    tuple(value.decode('utf-8') if isinstance(value, bytearray) else value for value in row)
                    for row in result_thm
                    ]
                
                
                

                action = request.args.get('action')
                def actionSelection(action):
                    if action=='itAccept':
                        row_id = request.args.get('row_id')
                        print(row_id)
                        # subject="Medical Authenticatation System"
                        # receiver="sglasanthapradeep@gmail.com"
                        # message_content="Testing Flask Mail !"
                        # email(receiver,subject,message_content)

                        return redirect('admin')

                        # query="INSERT INTO admin_it(admin_id,name,year,semester,subject,attempt,date_begin,date_end,method,image,date_issued)SELECT admin_id,name,year,semester,subject,attempt,date_begin,date_end,method,med_image,date_issued FROM medical_infor ORDER BY time ASC LIMIT 1"
                        # new_data.insertData(query,host,database,user)
                        # dlt_query="DELETE FROM medical_infor WHERE course='IT' ORDER BY time ASC LIMIT 1"
                        # new_data.delete(dlt_query,host,database,user)

                        
                        # dltQuery="DELETE  FROM medical_infor WHERE course='IT'  ORDER BY time ASC LIMIT 1 "
                        # new_data.delete(dltQuery,host,database,user)

                    elif action=='itReject':
                        row_id = request.args.get('row_id')
                        print(row_id)
                        # dlt_query="DELETE FROM medical_infor WHERE course='IT' ORDER BY time ASC LIMIT 1"
                        # new_data.delete(dlt_query,host,database,user)
                        # return redirect(url_for('admin'))
                    


                    elif action=='accAccept':
                        pass
                        # query="INSERT INTO admin_accountency(admin_id,name,year,semester,subject,attempt,date_begin,date_end,method,image,date_issued)SELECT admin_id,name,year,semester,subject,attempt,date_begin,date_end,method,med_image,date_issued FROM medical_infor ORDER BY time ASC LIMIT 1"
                        # new_data.insertData(query,host,database,user)
                        # dlt_query="DELETE FROM medical_infor WHERE course='ACCOUNTANCY' ORDER BY time ASC LIMIT 1"
                        # new_data.delete(dlt_query,host,database,user)
                        

                    elif action=='accReject':
                        pass

                        # dlt_query="DELETE FROM medical_infor WHERE course='ACCOUNTANCY' ORDER BY time ASC LIMIT 1"
                        # new_data.delete(dlt_query,host,database,user)
                        # return redirect(url_for('admin'))

                    elif action=='manaAccept':
                        pass
                        # query="INSERT INTO admin_management(admin_id,name,year,semester,subject,attempt,date_begin,date_end,method,image,date_issued)SELECT admin_id,name,year,semester,subject,attempt,date_begin,date_end,method,med_image,date_issued FROM medical_infor ORDER BY time ASC LIMIT 1"
                        # new_data.insertData(query,host,database,user)
                        # dlt_query="DELETE FROM medical_infor WHERE course='MANAGEMENT' ORDER BY time ASC LIMIT 1"
                        # new_data.delete(dlt_query,host,database,user)
                        

                    elif action=='manaReject':
                        pass
                        # dlt_query="DELETE FROM medical_infor WHERE course='MANAGEMENT' ORDER BY time ASC LIMIT 1"
                        # new_data.delete(dlt_query,host,database,user)
                    elif action=='thmAccept':
                        pass
                        # query="INSERT INTO admin_thm(admin_id,name,year,semester,subject,attempt,date_begin,date_end,method,image,date_issued)SELECT admin_id,name,year,semester,subject,attempt,date_begin,date_end,method,med_image,date_issued FROM medical_infor ORDER BY time ASC LIMIT 1"
                        # new_data.insertData(query,host,database,user)
                        # dlt_query="DELETE FROM medical_infor WHERE course='TOURISM' ORDER BY time ASC LIMIT 1"
                        # new_data.delete(dlt_query,host,database,user)
                        

                    elif action=='thmReject':
                        pass
                        # dlt_query="DELETE FROM medical_infor WHERE course='TOURISM' ORDER BY time ASC LIMIT 1"
                        # new_data.delete(dlt_query,host,database,user)

                    
                    elif action=='engAccept':
                        pass

                        # query="INSERT INTO admin_english(admin_id,name,year,semester,subject,attempt,date_begin,date_end,method,image,date_issued)SELECT admin_id,name,year,semester,subject,attempt,date_begin,date_end,method,med_image,date_issued FROM medical_infor ORDER BY time ASC LIMIT 1"
                        # new_data.insertData(query,host,database,user)
                        # dlt_query="DELETE FROM medical_infor WHERE course='ENGLISH' ORDER BY time ASC LIMIT 1"
                        # new_data.delete(dlt_query,host,database,user)

                    elif action=='engReject':
                        pass

                        # dlt_query="DELETE FROM medical_infor WHERE course='ENGLISH' ORDER BY time ASC LIMIT 1"
                        # new_data.delete(dlt_query,host,database,user)
                actionSelection(action)

    return render_template('interfaces/admin/admin.html',form=new_admin,
                            
                        #    manage_count=manage_count,thm_count=thm_count,
                        #    english_count=english_count,

                        #    
                        #    result_account=cleaned_result_account,
                        #    result_manage=cleaned_result_manage,
                        #    result_thm=cleaned_result_thm,
                        #    result_english=cleaned_result_english,

                            user_name=user_name,
                            count=total,
                            it_count=it,
                            account_count=acc,
                            manage_count=mng,
                            thm_count=thm,
                            english_count=eng,
                            result_it=cleaned_values_it,
                            result_thm=cleaned_values_thm,
                            result_en=cleaned_values_eng,
                            result_manage=cleaned_values_mng,
                            result_account=cleaned_values_acc

                           )




#time schedule 


from flask import request
import datetime
#for time table values
def heavyClean(values):
        cleaned_values=[]
        for val in values:
            cleaned_tuple = (

                val[0].decode(),  # Convert bytearray to string
                val[1].decode(),
                val[2].strftime('%B %d, %Y'),# Format date as "Month day, Year"
                str(val[3]),  # Convert timedelta to string
                str(val[4]),  # Convert timedelta to string
                val[5].decode()  # Convert bytearray to string 
                
            )
            cleaned_values.append(cleaned_tuple)
        return cleaned_values
@app.route('/exams', methods=['GET', 'POST'])
def exams():
    form = TimeSchedule()
    new_data = MySql(host, database, user)
    year_data = new_data.getUniqeCountYear('IT')
    semester_data = new_data.getUniqeCountSem('IT')
    years = [x[0] for x in year_data]
    semesters = [x[0] for x in semester_data]
    subject_query="SELECT s.subject_name FROM subjects AS s INNER JOIN departments AS dep ON dep.id=s.department_id WHERE dep.calling_name='IT';"
    subjects=new_data.fetchMultiVal(subject_query)
    cleaned_subjects = [item[0].decode() for item in subjects]
    form.subject_name.choices=cleaned_subjects
    data=('IT',)
    values=new_data.getValues(data)
    cleaned_values=heavyClean(values)
    

    if form.validate_on_submit():
        
        subject=form.subject_name.data
        date=form.date.data
        start_time=form.start_time.data
        end_time=form.end_time.data
        location=form.location.data
        sub_query="SELECT subject_id FROM subjects WHERE subject_name=%s;"
        sub_data=(subject,)
        sub_id=new_data.fetchOneForeing(sub_query,sub_data)
        syll_query="SELECT id FROM syllabus WHERE syllabus_type=%s;"
        syll_data=('OLD',)
        syll_id=new_data.fetchOneForeing(syll_query,syll_data)
        
        if 'super_name' and 'super_password' in session:
            name=session['super_name']
            password=session['super_password']
            super_query="SELECT admin_id FROM super_admins WHERE first_name=%s AND password=%s;"
            super_data=(name,password)
            super_id=new_data.fetchOneForeing(super_query,super_data)
        
        main_query="INSERT INTO exams(subject_id,syllabus_id,super_admin_id,held_date,start_time,end_time,location)VALUES(%s,%s,%s,%s,%s,%s,%s);"
        main_data=(sub_id,syll_id,super_id,date,start_time,end_time,location)
        new_data.table(main_query,main_data)
        return redirect(url_for('exams'))   

    return render_template('interfaces/superAdmin/exams.html', form=form,form_data=cleaned_values)


   