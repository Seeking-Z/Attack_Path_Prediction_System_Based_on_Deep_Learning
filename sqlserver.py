"""
建表语句
登录表
CREATE TABLE login
(
    id INT PRIMARY KEY IDENTITY(1,1),
    username NVARCHAR(255),
    password NVARCHAR(255),
    admin int
)

信息表
CREATE TABLE message
(
    id INT PRIMARY KEY IDENTITY(1,1),
    sip NVARCHAR(255),
    dip NVARCHAR(255),
    time DATETIME,
    status NVARCHAR(255),
    image NVARCHAR(MAX)
)
"""

import pyodbc
import settings


class Sqlserver:
    """连接数据库"""

    def __init__(self, server: str, database: str, username: str, password: str, table_name: str) -> None:
        """初始化数据库连接"""
        connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        self.connection = pyodbc.connect(connection_string)
        self.cursor = self.connection.cursor()
        self.table_name = table_name

    def insert_data(self, data):
        """
        插入数据
        table_name: 表名
        data: 插入的数据，应为字典，键是列名，值是要插入的值
        """
        columns = ', '.join(data.keys())
        values = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})"
        values = list(data.values())

        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error during insert_data: {str(e)}")
            return False

    def delete_data(self, condition):
        """
        删除数据
        table_name: 表名
        condition: 删除的条件，应为字符串
        """
        query = f"DELETE FROM {self.table_name} WHERE {condition}"

        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error during delete_data: {str(e)}")
            return False

    def update_data(self, data, condition):
        """
        更新数据
        data: 要更新的数据，应为字典，键是要更新的列名，值是新的值
        condition: 更新的条件，应为字符串
        """
        set_values = ', '.join([f"{column} = ?" for column in data.keys()])
        query = f"UPDATE {self.table_name} SET {set_values} WHERE {condition}"
        values = list(data.values())

        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error during update_data: {str(e)}")
            return False

    def select_data(self, columns, condition=None):
        """
        查询数据
        columns: 要查询的列，可以是字符串或列表
        condition: 查询条件，可选
        """
        if isinstance(columns, str):
            columns = [columns]

        query = f"SELECT {', '.join(columns)} FROM {self.table_name}"
        if condition:
            query += f" WHERE {condition}"

        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error during select_data: {str(e)}")
            return False

    def close(self):
        """关闭数据库连接"""
        self.connection.close()


# settings = settings.Settings()
# db = Sqlserver(settings.sqlserver, settings.database, settings.username, settings.password, "login")
# in_data = {"id": None, "username": "test", "password": "test"}
# db.insert_data(in_data)
# result = db.select_data(["id", "username", "password"])
# db.update_data({"password": "test123"}, "username='admin'")
# db.delete_data("username='admin'")
# print(result)
# print(type(result[0][1]))
# db.close()


