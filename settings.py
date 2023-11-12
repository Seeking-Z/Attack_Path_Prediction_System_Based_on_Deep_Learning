class Settings:
    """系统设置"""

    def __init__(self):
        """数据库连接设置"""
        self.sqlserver = '127.0.0.1'
        self.database = '基于深度学习的攻击路径预测系统'
        self.username = 'SA'
        self.password = '12@plokmnPLOKMN'

        self.login_and_user_table = 'login'
        self.login_and_user_table_columns = ['id', 'username', 'password', 'admin']
