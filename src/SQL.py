import pyodbc

"""
    Author: Silvio Lacerda
    Last Update: 04/19/2020
"""


class SQLReturn:
    def __init__(self, columns, rowData, callback, father=None):
        # initialize seting default values to manipulate
        self.rowCount = 0
        self.columns = columns
        self.rowData = rowData
        self.callback = callback
        self.isRunning = False
        self.father = father

    def ReturnData(self):
        # verify if nothing is running
        if not self.isRunning:
            self.isRunning = True
            if len(self.rowData) > 0:
                for i in range(len(self.rowData)):
                    # get the number of the counter
                    self.rowCount = i
                    # if there is a function, i run
                    if self.callback:
                        self.callback(self.father, self)

    def getDataByName(self, name):
        index = -1
        for idx, column in enumerate(self.columns):
            if column == name:
                index = idx
                break
        if index == -1:
            print("This field does not exist.")
        else:
            return self.rowData[self.rowCount][index]


class SQL:
    def __init__(
        self,
        server,
        database,
        username,
        password,
        driver="{ODBC Driver 17 for SQL Server}",
        father=None,
    ):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.driver = driver
        self.SQLConnection = pyodbc.connect(
            "DRIVER="
            + driver
            + ";SERVER="
            + server
            + ";PORT=1433;DATABASE="
            + database
            + ";UID="
            + username
            + ";PWD="
            + password
        )
        self.cursor = self.SQLConnection.cursor()
        self.father = father

    def RunQuery(self, query, callback=None):
        try:
            self.rowData = []
            self.cursor.execute(query)
            self.SQLConnection.commit()

            if self.cursor.description is not None:
                if len(self.cursor.description) > 0:
                    # get the cols and rows of the query
                    self.columns = [column[0] for column in self.cursor.description]

                    self.rowData = list(self.cursor)

                    # pass the values of the query
                    QueryResult = SQLReturn(
                        self.columns, self.rowData, callback, self.father
                    )

                    QueryResult.ReturnData()
            pass
        except:
            print('An error occurred in the query: "' + query + '"')
            pass
