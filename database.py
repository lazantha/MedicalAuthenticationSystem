import mysql.connector

host='localhost'
database='medical_db'
user='root'
password=None

#For Tables
class Table:
    def table(self,query,host,database,user,password):
        try:
            connection=mysql.connector.connect(host=host,database=database,user=user,password=password)
            cursor=connection.cursor()
            cursor.execute(query)
            print ("Query Successfull !")
        except:
            print("Connection Failed !")
        finally:
            if connection.is_connected():
                connection.close()

new_table=Table()
drop_table=Table()
drop_admin="DROP TABLE admin"
drop_table.table(drop_admin,host,database,user,password)






            
    

