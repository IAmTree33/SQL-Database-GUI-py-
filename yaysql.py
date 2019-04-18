import sqlite3

class DB:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.curtable = ""
        self.connection = connection

    def list_col(self):
        
        self.cursor.execute(f"PRAGMA table_info({self.curtable})")
        data = self.cursor.fetchall()
        retdata = []

        for tup in data:
            inner_layer = []
            inner_layer.append(tup[1])
            inner_layer.append(tup[2])
            retdata.append(inner_layer)

        return retdata
    def clear_curtable(self):
        command = f"DELETE FROM {self.curtable}"
        self.cursor.execute(command)
        
    def delete_curtable(self):
        command = f"DROP TABLE {self.curtable}"
        self.cursor.execute(command)
        
    def get_column(self, column):
        command = f"SELECT {column} FROM {self.curtable}"
        self.cursor.execute(command)
        return self.cursor.fetchall() 
    
    def list_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return self.cursor.fetchall() 
    
    def save(self):
        """ Commits """
        self.connection.commit()
        
    def createTable(self, columns):
        """ Table Name is the value of curtable """
        command = f"CREATE TABLE {self.curtable}(\n"

        for key in columns.keys():
            final_key = key

        for key in columns.keys():
            if columns[key] == "autoinc":
                command += f"{key} INTEGER PRIMARY KEY AUTOINCREMENT"
            elif type(columns[key]) == type(str()):
                command += f"{key} TEXT NOT NULL"
            elif type(columns[key]) == type(int()):
                command += f"{key} INTEGER NOT NULL"
            elif type(columns[key]) == type(list()):
                command += f"{key} LIST"
            elif type(columns[key]) == type(float()):
                command += f"{key} REAL NOT NULL"
            if key != final_key:
                command += ",\n"
                
        command += ")"
        self.cursor.execute(command) 
        
    
    def readTable(self):
        """ Reads Contents Of curtable """
        command = f"SELECT * FROM {self.curtable}"
        self.cursor.execute(command)
        return self.cursor.fetchall() 

    def addValue(self, *args):
        """ Adds Values To curtable """
        values = []
        for arg in args:
            if type(arg) == type(list()):
                values = arg
                break
            values.append(arg)
        
            
        
        command = f"INSERT INTO {self.curtable} VALUES("
        index = -1
        max_index = len(values) - 1
        for arg in values:
            index += 1
            if type(arg) == type(str()):
                command += f"'{arg}'"    
            elif type(arg) == type(int()) or type(arg) == type(float()):
                command += f"{arg}"
            
            if index != max_index:
                command += ","
        
        command += ")" 
        self.cursor.execute(command)

    def query(self, searchQuery, column = "ALL"):
        if column == "ALL":
            command = f"SELECT * FROM {self.curtable} WHERE {searchQuery}"
        else:
            command = f"SELECT {column} FROM {self.curtable} WHERE {searchQuery}"

        self.cursor.execute(command)
        return self.cursor.fetchall() 






