# Importing necessary libraries
import sqlite3
import os
from pathlib import Path

# Define custom exceptions for database and table errors
class DataBase_Error(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)

class Table_Error(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)

# Define the DataBase class
class DataBase():
    path = Path('./database/')  # Set the default path for the database
    db_name : str  # Database name
    tb_name_: str  # Table name
    conn_ = ''  # Connection string

    # Initialize the database with a name and optional path
    def __init__(self,db_name,path_ = '') -> None:
        self.db_name = db_name
        if path_ != '':
            self.path += path_
        if not self.path.exists():
            self.path.mkdir()
        self.conn

    # Method to execute SQL queries
    def exec(self,query) -> list:
        try:
            cursor = self.conn_.cursor()
            cursor.execute(query)
            self.conn_.commit()
            return [True,cursor]
        except Exception as e:
            return [False,e]

    # Method to get a table from the database
    def get_table(self,tb_name):
        if self.if_db_exists:
            return Table(self.db_name,tb_name)

    # Method to rename the database
    def rename(self,db_name):
        os.rename(r'./database/'+self.db_name+'.db',r'./database/'+db_name+'.db')
        self.db_name = db_name
        self.relaod
        return True

    # Method to reload the database connection
    @property
    def reload(self):
        self.conn_ = sqlite3.connect('./database/'+str(self.db_name).lower()+'.db')
        return self.conn_

    # Method to get the connection to the database
    @property
    def conn(self):
        if self.conn_ == '':
            if not self.if_db_exists:
                self.conn_ = sqlite3.connect('./database/'+str(self.db_name).lower()+'.db')
                self.conn_.commit()
            else:
                self.conn_ = sqlite3.connect('./database/'+str(self.db_name).lower()+'.db')
            return self.conn_

    # Method to get all tables from the database
    @property
    def get_tables(self):
        status, cursor = self.exec("SELECT name FROM sqlite_master WHERE type='table';")
        if status:
            tabelas = cursor.fetchall()
            return [tname[0] for tname in tabelas]
        return status

    # Method to check if a database exists
    @property
    def if_db_exists(self):
        for (dirpath, dirnames, filenames) in os.walk('./database'):
            if f"{self.db_name}.db" in filenames:
                return True
            else:
                return False

    # Method to delete a database
    def __delattr__(self, name):
        if self.if_db_exists(self.db_name):
            os.remove(r".\API\DBS"+r'\ '.replace(' ','')+str(self.db_name)+'.db')
            return True
        return False

# Define the Table class
class Table(object):
    database: DataBase  # Database object
    tb_name : str  # Table name
    bluk = False  # Bulk operation flag
    bluk_break = 500  # Maximum number of queries in a bulk operation
    bluk_querys = []  # List of queries for a bulk operation

    # Initialize the table with a database and table name
    def __init__(self,database,table_name) -> None:
        self.tb_name = table_name
        self.database = DataBase(database)

    # Method to check if a table is blocked
    @property 
    def block(self):
        if self.database.get_tables == False:
            return True
        return self.tb_name not in self.database.get_tables

    # Method to generate a table with given variables
    def gen(self,variables):
        if self.block:
            sqlcomd = f"CREATE TABLE IF NOT EXISTS {str(self.tb_name)} ( ell text,{variables})"
            self.database.exec(sqlcomd)
            conn = self.database.conn_
            conn.commit()

    # Method to get all rows from a table
    @property
    def get_rows(self):
        if not self.block:
            sqlcomd = "SELECT * FROM "+str(self.tb_name)
            status,info = self.database.exec(sqlcomd)
            if status:
                names = list(map(lambda x: x[0], info.description))
                return names
            else:
                print(f' {self.tb_name} not found plz add the table to get rows')
                return False
        raise Table_Error("[Table-Block] To Unlock the table use table_obj.gen('var1,...,varN')")

    # Method to get data from a table
    def get(self,code = '',value = '',Expecial=''):
        if not self.block:
            info = ''
            if Expecial != '':
                sqlcomd = "SELECT * FROM "+str(self.tb_name) + " " + str(Expecial)
            elif value == '':
                sqlcomd = "SELECT * FROM "+str(self.tb_name)+" WHERE ell = 'All'"
            elif code != '' and value == '':
                sqlcomd = "SELECT * FROM " + str(self.tb_name) + " WHERE " + str(code)
            else:
                sqlcomd = "SELECT * FROM "+str(self.tb_name)+" WHERE "+str(code)+" = '"+str(value)+"'"
            stats,info = self.database.exec(sqlcomd)
            if stats:
                for i in info.fetchall():
                    yield i
            return stats

    # Method to update a table
    def update(self,target,set):
        sqlcmd = f"UPDATE {self.tb_name} SET {set[0]} = '{set[1]}' WHERE {target[0]} = '{target[1]}'" # set = "column = value"
        self.database.exec(sqlcmd)
        return True

    # Method to rename a table
    def rename(self,tabel_name):
        try:
            sql = "RENAME TABLE " + str(self.tb_name) +' TO '+ str(tabel_name)+";"
            self.database.exec(sql)
            self.database.reload
            self.tb_name = tabel_name
            return True
        except:
            return False

    # Method to handle bulk operations
    def bluk_headler(self,query):
        if not self.block:
            if self.bluk == True:
                self.bluk_querys.append(query)
                if len(self.bluk_querys) % self.bluk_break == 0:
                    status,cursor = self.database.exec('BEGIN TRANSACTION')
                    for query in self.bluk_querys:
                        cursor.execute(query)
                    cursor.execute('COMMIT')
                    self.bluk_querys = []
                return False
            return True
        raise Table_Error("[Table-Block] To Unlock the table use table_obj.gen('var1,...,varN')")

    # Method to add data to a table
    def __iadd__(self, str_data: object) -> bool:
        if not self.block:
            rows = self.get_rows
            row_data = str(str_data).split(',')
            sqlcmd = "INSERT INTO "+self.tb_name+"("
            for conta,(row) in enumerate(rows):
                if conta == len(rows)-1:
                    sqlcmd += f"{row}"
                else:
                    sqlcmd += f"{row},"
            sqlcmd += ") VALUES ('All',"
            for conta,(info) in enumerate(row_data):
                if conta == len(row_data)-1:
                    sqlcmd += f"'{info}'"
                else:
                    sqlcmd += f"'{info}',"
            sqlcmd += ");"
            if self.bluk_headler(sqlcmd):
                self.database.exec(sqlcmd)
            return self
        raise Table_Error("[Table-Block] To Unlock the table use table_obj.gen('var1,...,varN')")

    # Method to delete data from a table
    def __isub__(self,str_query):
        if not self.block:
            code = str_query.split(',')
            if len(code) >= 2:
                value = code[1]
            if len(code) == 3:
                sp = code [2]
            code = code[0]
            if value == '':
                sqlcmd = "DELETE from "+str(self.tb_name)+" where * = *;"
            elif code != '' and value == '':
                sqlcmd = "DELETE from " + str(self.tb_name) + " where " + str(code) + "';"
            elif code == '' and value == '' and sp != '':
                sqlcmd = "DELETE from " + str(self.tb_name) + " where " + str(sp) + "';"
            else:
                sqlcmd = "DELETE from " + str(self.tb_name) + " where "+str(code)+" = '"+str(value)+"';"
            self.database.exec(sqlcmd)
            return self

    # Method to delete a table
    def __delattr__(self,name):
        try:
            sql = "DROP TABLE "+str(self.tb_name)+";"
            self.database.exec(sql)
        except:
            return False
