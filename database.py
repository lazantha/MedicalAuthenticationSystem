# Sucess !
import mysql.connector
host='localhost'
database='medical_db'
user='root'


class MySql:
	#for insertions
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
	
	def insertData(self,query,host,database,user):
		try:
			connection=None
			connection=mysql.connector.connect(host=host,database=database,user=user,password=None)
			cursor=connection.cursor(prepared=True)
			cursor.execute(query)
			connection.commit()
			print("Success !")
		except mysql.connector.Error as error:
			print("query failed {}".format(error))
		finally:
			if connection != None and connection.is_connected():
				connection.close()
				print("Connection Closed !")
	
	# For parameter Binding and foreing keys
	#use comma after created tuple when binding arguments if it has One Argument 
	def fetchOneForeing(self,query,data,host,database,user):
		try:
			connection=None
			connection=mysql.connector.connect(host=host,database=database,user=user,password=None)
			cursor=connection.cursor(prepared=True)
			cursor.execute(query,data)
			result=cursor.fetchone()
			return(result[0])
			print("getting success !")
		except mysql.connector.Error as error:
			print("query failed {}".format(error))
		finally:
			if connection != None and connection.is_connected():
				connection.close()
				print("Connection Closed !")

	#For multiple foreing keys data bind
	def fetchAllMulForeing(self,query,data,host,database,user):
		try:
			connection=None
			connection=mysql.connector.connect(host=host,database=database,user=user,password=None)
			cursor=connection.cursor(prepared=True)
			cursor.execute(query,data)
			result=cursor.fetchall()
			return(result)
			print("getting success !")
		except mysql.connector.Error as error:
			print("query failed {}".format(error))
		finally:
			if connection != None and connection.is_connected():
				connection.close()
				print("Connection Closed !")



		

	# FOR SINGLE QUERY
	def fetchOne(self,query,host,database,user):
		try:
			connection=None
			connection=mysql.connector.connect(host=host,database=database,user=user,password=None)
			cursor=connection.cursor(prepared=True)
			cursor.execute(query)
			result=cursor.fetchone()
			return result[0]
			print("getting success !")
		except mysql.connector.Error as error:
			print("query failed {}".format(error))
		finally:
			if connection != None and connection.is_connected():
				connection.close()
				print("Connection Closed !")
	
	#FOR SINGLE QUERY WITHOUT BINDING 
	def fetchMultiVal(self,query,host,database,user):
		try:
			connection=None
			connection=mysql.connector.connect(host=host,database=database,user=user,password=None)
			cursor=connection.cursor(prepared=True)
			cursor.execute(query)
			result=cursor.fetchall()
			return result
			print("getting success !")
		except mysql.connector.Error as error:
			print("query failed {}".format(error))
		finally:
			if connection != None and connection.is_connected():
				connection.close()
				print("Connection Closed !")
		
	
	def delete(self,query,host,database,user):
		try:
			connection=None
			connection=mysql.connector.connect(host=host,database=database,user=user,password=None)
			cursor=connection.cursor(prepared=True)
			cursor.execute(query)
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
