from flask_login import UserMixin
from werkzeug.security import check_password_hash

import sqlserver
import settings


class User(UserMixin):
    """用户类"""

    def __init__(self, username):
        """初始化用户类"""
        setting = settings.Settings()
        self.login_sqlserver = sqlserver.Sqlserver(setting.sqlserver, setting.database, setting.sql_username,
                                                   setting.sql_password,
                                                   setting.login_and_user_table)
        self.id = None
        self.username = username

        self.select_columns = setting.login_and_user_table_columns

    def verify_username(self):
        """验证用户是否存在，不存在返回False，存在则将返回id存入类的属性并返回True"""
        data = self.login_sqlserver.select_data(self.select_columns[0],
                                                [self.select_columns[1], self.username])
        if not data:
            return False
        self.id = data[0][0]
        return True

    def verify_password(self, password):
        """验证密码是否正确，正确返回True，错误返回False"""
        data = self.login_sqlserver.select_data(self.select_columns[2],
                                                [self.select_columns[0], self.id])

        if check_password_hash(data[0][0], password):
            return True
        else:
            return False

    def is_admin(self):
        """验证是否是管理员"""
        data = self.login_sqlserver.select_data(self.select_columns[3],
                                                [self.select_columns[0], self.id])
        if data[0][0]:
            return True
        else:
            return False

    def get_id(self):
        """获取用户id"""
        return self.id

    @staticmethod
    def get(user_id):
        """获取指定id的用户实例"""
        setting = settings.Settings()
        login_sqlserver = sqlserver.Sqlserver(setting.sqlserver, setting.database, setting.sql_username,
                                              setting.sql_password,
                                              setting.login_and_user_table)
        select_columns = setting.login_and_user_table_columns
        data = login_sqlserver.select_data(select_columns[1],
                                           [select_columns[0], user_id])
        user = User(data[0][0])
        user.verify_username()
        return user

    def logout_process(self):
        self.login_sqlserver.close()

