# Sucess !
import mysql.connector
host='localhost'
database='testdb'
user='root'
password=None


class MySql:
	def table(self,query,data,host,database,user,password):
		try:
			connection=mysql.connector.connect(host=host,database=database,user=user,password=password)
			cursor=connection.cursor(prepared=True)
			cursor.execute(query,data)
			connection.commit()
			print("Success !")
		except mysql.connector.Error as error:
			print("query failed {}".format(error))
		# finally:
		# 	if connection.is_connected():
		# 		connection.close()
		# 		print("Connection CLosed !")



# newSql=MySql()
# query="INSERT INTO user VALUES(2,'nimal','nimalPass');"
# newSql.table(query,host,database,user,password)
