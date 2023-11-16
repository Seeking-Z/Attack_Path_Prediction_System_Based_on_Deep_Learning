import pyodbc
from datetime import datetime
import sqlserver
import settings

# 连接数据库
settings = settings.Settings()
test_sql = sqlserver.Sqlserver(settings.sqlserver, settings.database, settings.sql_username, settings.sql_password, settings.message_table)


# 示例插入时间数据
# current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间精确到秒
# data = {
#     'sip': '127.0.0.1',
#     'dip': '127.0.0.1',
#     'time': current_time,
#     'status': 'normal'
# }
# test_sql.insert_data(data)

data = test_sql.select_data(['id', 'sip', 'dip', 'time', 'status'])
print(data)

# 关闭连接
test_sql.close()
