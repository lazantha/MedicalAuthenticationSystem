import mysql.connector

class NewMySql:
    def __init__(self, host, database, user):
        self.host = host
        self.database = database
        self.user = user

    def connect(self):
        return mysql.connector.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=None
        )

    def execute_query(self, query, data=None):
        try:
            connection = self.connect()
            cursor = connection.cursor(prepared=True)
            cursor.execute(query, data)
            connection.commit()
            print("Success!")
            return cursor.fetchall()
        except mysql.connector.Error as error:
            print("Query failed: {}".format(error))
        finally:
            if connection is not None and connection.is_connected():
                cursor.close()
                connection.close()
                print("Connection closed!")

    def table(self, query, data):
        self.execute_query(query, data)

    def insertData(self, query):
        self.execute_query(query)

    def fetchOneForeing(self, query, data):
        return self.execute_query(query, data)[0][0]

    def fetchAllMulForeing(self, query, data):
        return self.execute_query(query, data)

    def fetchOne(self, query):
        return self.execute_query(query)[0][0]

    def fetchMultiVal(self, query):
        return self.execute_query(query)

    def delete(self, query):
        self.execute_query(query)

    def deleteMulti(self, query):
        self.execute_query(query)

    def getCount(self, department):
        query = "SELECT count(*) FROM subjects AS s INNER JOIN medical_infor AS mi ON s.subject_id=mi.subject_id INNER JOIN departments AS dep ON s.department_id=dep.id WHERE dep.calling_name=%s;"
        return self.execute_query(query, (department,))[0][0]

    def getMain(self, department):
        query = "SELECT st.email,first_name,id_card,mi.medical_sheet FROM students AS st INNER JOIN medical_infor AS mi ON st.user_id =mi.user_id INNER JOIN departments AS dep ON st.department_id=dep.id WHERE dep.calling_name=%s ORDER BY mi.recorded_time DESC;"
        return self.execute_query(query, (department,))

    def getUniqeCountYear(self, department):
        query = "SELECT DISTINCT s.year FROM subjects AS s INNER JOIN departments AS dep ON s.department_id=dep.id WHERE dep.calling_name=%s;"
        return self.execute_query(query, (department,))

    def getUniqeCountSem(self, department):
        query = "SELECT DISTINCT s.semester FROM subjects AS s INNER JOIN departments AS dep ON s.department_id=dep.id WHERE dep.calling_name=%s;"
        return self.execute_query(query, (department,))

    def getUniqeCountSub(self, department):
        query = "SELECT sub.subject_name FROM subjects AS sub INNER JOIN exams AS ex ON ex.subject_id=sub.subject_id INNER JOIN departments AS dep ON dep.id=sub.department_id WHERE dep.calling_name=%s;"
        return self.execute_query(query, (department,))

    def getValues(self, data):
        query = "SELECT sub.subject_name,subject_code,ex.held_date,start_time,end_time,location FROM departments AS dep INNER JOIN subjects AS sub ON dep.id=sub.department_id INNER JOIN exams AS ex ON sub.subject_id=ex.subject_id WHERE dep.calling_name=%s;"
        return self.execute_query(query, data)

    def getMainSuper(self, row_id):
        query = "SELECT stu.email,sub.subject_name ,att.attempt,mi.exam_date,exam_location FROM subjects AS sub INNER JOIN medical_infor AS mi ON"

    def update(self, query, data=None):
        self.execute_query(query, data)





