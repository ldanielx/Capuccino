import pyodbc
from pandas import read_csv

'''
    Author: Silvio Lacerda
    Last Update: 06/13/2020
'''

class Data:
    @staticmethod
    def extractCSV(filename, sep = ','):
        data = read_csv(filename, sep=sep)
        return data.values

class Table:
    class Field:
        def __init__(self, name, dataType, key = '', specification = '', required = False, data = None):
            self.name = name
            self.data = data
            self.dataType = dataType
            self.required = required
            self.key = key
            self.specification = specification

        def setData(self, data):
            self.data = data


    def __init__(self, name, fields = [], conn = None):
        self.conn = conn
        self.name = name
        self.fields = fields

    def setConnection(self, conn):
        self.conn = conn

    def setFields(self, fields):
        self.fields = fields

    def insertInto(self, data):
        if self.conn is not None:
            query = """
                insert into """ + self.name + """ 
            """
            for row in range(len(data)):
                query += ' select '
                for col in range(len(data[row])):
                    final =  ', ' if col < len(data[row])-1 else ''
                    query += "'" + str(data[row][col]) + "'" + final
                
                if row < len(data)-1:
                    query += ' union all '

            self.conn.RunQuery(query)
        else:
            print('Please, set a connection')


    def deleteWhere(self, stringKey = '', value = '', customSyntax = '', operator = '='):
        if self.conn is not None:
            query = ''
            
            if customSyntax <> '':
                query = """
                    delete from """ + self.name + """
                    where """ + customSyntax
            
            else:
                query = """
                    delete from """ + self.name + """
                    where 
                        """ + stringKey + """ """ + operator + """ '""" + value + """'
                    """

            self.conn.RunQuery(query)
        else:
            print('Please, set a connection')
            

    def create(self):
        if self.conn is not None:
            query = """
                if not exists (select * from sysobjects where name='""" + self.name + """' and xtype='U')
                    create table """ + self.name + """ (
            """

            for index, field in enumerate(self.fields):
                required = ' not null ' if field.required == True else ' '
                final =  ',' if index < len(self.fields)-1 else ''
                tempString = field.name + ' ' + field.dataType + required + field.key + ' ' + field.specification + final
                query += tempString

            query += " )"

            self.conn.RunQuery(query)
        else:
            print('Please, set a connection')