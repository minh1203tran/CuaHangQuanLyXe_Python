import pyodbc

class MSSQLConnection:
    def __init__(self, driver='SQL Server', server=r'.\DUCMINH',database='QUANLYCUAHANGXE', username='sa', password='minhtran123'):
        self.driver = driver
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = None

    def connect(self):
        try:
            connection_string = f"""Driver={{{self.driver}}};
                                    SERVER={self.server};
                                    DATABASE={self.database};
                                    UID={self.username};
                                    PWD={self.password};
                                """
            self.connection = pyodbc.connect(connection_string)
            return True
        except pyodbc.Error as e:
            print(f"Lỗi kết nối: {e}")
            return False

    def cursor(self):
        if self.connection is None:
            self.connect()
        return self.connection.cursor()

    def commit(self):
        if self.connection:
            self.connection.commit()

    def query(self, sql, params=None):
        try:
            cursor = self.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)

            if sql.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            else:
                self.commit()
                return True
        except pyodbc.Error as e:
            print(f"Lỗi query: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()


# Singleton pattern
class Database:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = MSSQLConnection()
            cls._instance.connect()
        return cls._instance
