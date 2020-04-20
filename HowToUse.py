# first use 'pip install pyodbc' at your terminal or cmd to download the library that i used
# to connect with SQL Server

# i did not created 'pyodbc', all rights reserved

# now you need to import SQL or just copy the code, and just use it bro

from SQL import SQL, SQLReturn

SERVER = '99.999.999.99'
DATABASE = 'NAME_OF_DATABASE'
USERNAME = 'USERNAME'
PASSWORD = 'AN_SECURITY_PASSWORD'

# something more beautiful
class ClassToGetData:
    def __init__(self, example1, example2):
        self.example1       = example1   
        self.example2       = example2

class FatherClass:
    def Callback(self, father, sqlReturn):
        value = ClassToGetData(
                    sqlReturn.getDataByName('example1'),
                    sqlReturn.getDataByName('example2')
                    )
        father.dataList.append(value)

    def LoadExample(self):
        self.dataList = []
        self.sqlConnection.RunQuery('select example1, example2 from t_table', self.Callback)

    def __init__(self):
        self.sqlConnection = SQL(SERVER,DATABASE,USERNAME,PASSWORD)
        self.sqlConnection.father = self
        self.LoadExample()

fatherClass = FatherClass()

for value in fatherClass.dataList:
    print(value.example1)


# or something more simple
sqlConn = SQL(SERVER,DATABASE,USERNAME,PASSWORD)
sqlConn.RunQuery('exec s_some_proc')

# if you want a query with parameters
sqlConn = SQL(SERVER,DATABASE,USERNAME,PASSWORD)
query = "exec s_some_proc "+ "'parameter'"
sqlConn.RunQuery(query)