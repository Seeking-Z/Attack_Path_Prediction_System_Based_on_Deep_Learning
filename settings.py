"""
Normal: 正常记录

DOS: 拒绝服务攻击

Probing: 监视和其他探测活动

R2L: 来自远程机器的非法访问

U2R: 普通用户对本地超级用户特权的非法访问
"""


class Settings:
    """系统设置"""

    def __init__(self):
        # 数据库连接设置
        self.sqlserver = '127.0.0.1'
        self.database = '基于深度学习的攻击路径预测系统'
        self.sql_username = 'SA'
        self.sql_password = '12@plokmnPLOKMN'

        self.login_and_user_table = 'login'
        self.login_and_user_table_columns = ['id', 'username', 'password', 'admin']

        self.message_table = 'message'
        self.message_table_columns = ['id', 'sip', 'sport', 'dip', 'dport', 'time', 'status', 'image']

        # 获取到的流量数据发送到的主机
        self.url = '127.0.0.1:5000'

        # 每种攻击的被入侵概率
        self.status = {
            'Normal': 0,
            'DOS': 0.1,
            'Probing': 0.05,
            'R2L': 0.5,
            'U2R': 0.8,
            'Down': 1  # 被攻陷
        }
