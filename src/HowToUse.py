from SQL import SQL, SQLReturn
from SQLAppendices import Table, Data

SERVER = "99.999.999.99"
DATABASE = "NAME_OF_DATABASE"
USERNAME = "USERNAME"
PASSWORD = "AN_SECURITY_PASSWORD"

sqlConn = SQL(SERVER, DATABASE, USERNAME, PASSWORD)


# something more beautiful
class ClassToGetData:
    def __init__(self, example1, example2):
        self.example1 = example1
        self.example2 = example2


class FatherClass:
    def Callback(self, father, sqlReturn):
        value = ClassToGetData(
            sqlReturn.getDataByName("example1"), sqlReturn.getDataByName("example2")
        )
        father.dataList.append(value)

    def LoadExample(self):
        self.dataList = []
        self.sqlConnection.RunQuery(
            "select example1, example2 from t_table", self.Callback
        )

    def __init__(self):
        self.sqlConnection = SQL(SERVER, DATABASE, USERNAME, PASSWORD)
        self.sqlConnection.father = self
        self.LoadExample()


fatherClass = FatherClass()

for value in fatherClass.dataList:
    print(value.example1)


# or something more simple
sqlConn.RunQuery("exec s_some_proc")


# if you want a query with parameters
sqlConn = SQL(SERVER, DATABASE, USERNAME, PASSWORD)
query = "exec s_some_proc " + "'parameter'"
sqlConn.RunQuery(query)


# using tables
fields = [
    Table.Field("id", "int", "primary key", "identity(1,1)"),
    Table.Field("name", "varchar(100)"),
    Table.Field("description", "varchar(100)"),
]
table = Table("t_Test", fields, sqlConn)
# table.setFields(fields)
# table.setConnection(sqlConn)
table.create()

table.insertInto(Data.extractCSV("../index.csv"))
table.deleteWhere("id", "1")
