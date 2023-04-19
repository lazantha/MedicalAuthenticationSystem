# Sucess !
import mysql.connector
host='localhost'
database='medical_db'
user='root'


class MySql:
	def table(self,query,data,host,database,user):
		try:
			connection=None
			connection=mysql.connector.connect(host=host,database=database,user=user,password=None)
			cursor=connection.cursor(prepared=True)
			cursor.execute(query,data)
			connection.commit()
			print("Success !")
		except mysql.connector.Error as error:
			print("query failed {}".format(error))
		finally:
			if connection != None and connection.is_connected():
				connection.close()
				print("Connection Closed !")


 



# newSql=MySql()
# query="INSERT INTO user VALUES(2,'nimal','nimalPass');"
# newSql.table(query,host,database,user,password)
