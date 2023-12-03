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
    sport NVARCHAR(6),
    dip NVARCHAR(255),
    dport NVARCHAR(6),
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

    def delete_data(self, column, condition):
        """
        删除数据
        table_name: 表名
        column: 列名
        condition: 删除的条件，应为字符串
        """
        query = f"DELETE FROM {self.table_name} WHERE {column}=?"

        try:
            self.cursor.execute(query, (condition,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error during delete_data: {str(e)}")
            return False

    def update_data(self, data, column, condition):
        """
        更新数据
        data: 要更新的数据，应为字典，键是要更新的列名，值是新的值
        condition: 更新的条件，应为字符串
        """
        set_values = ', '.join([f"{col} = ?" for col in data.keys()])
        query = f"UPDATE {self.table_name} SET {set_values} WHERE {column}=?"
        values = list(data.values())

        try:
            self.cursor.execute(query, values + [condition,])
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error during update_data: {str(e)}")
            return False

    def select_data(self, columns, condition=None):
        """
        查询数据
        columns: 要查询的列，应为列表或字符串
        condition: 查询条件，可选。列表，第一个为列，第二个为值
        """

        if isinstance(columns, str):
            columns = [columns]

        query = f"SELECT {', '.join(columns)} FROM {self.table_name}"
        values = None
        if condition:
            query += " WHERE " + condition[0] + '=?'
            values = [condition[1]]

        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error during select_data: {str(e)}")
            return False

    def close(self):
        """关闭数据库连接"""
        self.connection.close()


settings = settings.Settings()
db = Sqlserver(settings.sqlserver, settings.database, settings.sql_username, settings.sql_password, "login")
#   初始账号密码  admin zadmin2023
# in_data = {"username": "admin",
#            "password": "scrypt:32768:8"
#                        ":1$CwZM7K9pzo4ecW6i$2584b1fba5092c65a70a25db6d8befc5bbb2656d3ef24ad3fd4c264a155a01b560ca4e92c375efc8d3be7f4cfb54cff50247bee8f218c394cdbe40204905eb8d",
#            "admin": 1}
# db.insert_data(in_data)
# result = db.select_data(["id", "username", "password"], ['id', 19])
# print(result)
# db.update_data({"password": "test123"}, "id",18)
# db.delete_data("username",'admin')
# print(result)
# print(type(result[0][1]))
# db.close()
