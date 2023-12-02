import datetime
from flask import Blueprint, request
import pickle
import networkx as nx
import ids
import prediction
import settings
import sqlserver

prediction_blueprint = Blueprint('prediction', __name__)


def data_processing(data):
    """数据处理，返回特征值数组/源ip/源端口/目的ip/目的端口/时间"""
    feature = data[:-5]
    sip = data[-5]
    sport = data[-4]
    dip = data[-3]
    dport = data[-2]
    time = datetime.datetime.strptime(data[-1], "%Y-%m-%dT%H:%M:%S")

    return feature, sip, sport, dip, dport, time


def check_data(data):
    """检查是否符合标准"""
    if len(data) != 33:
        return False
    if len(data[-1]) != 19:
        return False
    return True


@prediction_blueprint.route('/api/prediction', methods=['POST'])
def prediction_process():
    """攻击路径预测接口"""
    data = request.form['data']
    data = data.split(',')
    if not check_data(data):
        return ''
    feature, sip, sport, dip, dport, time = data_processing(data)

    # 初始化
    setting = settings.Settings()
    login_sqlserver = sqlserver.Sqlserver(setting.sqlserver, setting.database, setting.sql_username,
                                          setting.sql_password,
                                          setting.message_table)
    columns = setting.message_table_columns
    g = nx.Graph()

    # 预测,并将数据进行处理预测后存入数据库

    try:
        with open('gdata.pickle', 'rb') as file:
            g = pickle.load(file)
    except FileNotFoundError:
        print('未找到储存文件，使用空白实例')
    except:
        print('未知错误，无法读取实例。使用空白实例')

    status = ids.get_label(feature)  # 获取入侵检测返回的状态

    if status == 'Normal':
        prediction.prediction(g, sip, dip, status, setting)  # 只传入数据
    else:
        image = prediction.prediction(g, sip, dip, status, setting)  # 返回攻击路径预测的图片

        in_data = {
            columns[1]: sip,
            columns[2]: sport,
            columns[3]: dip,
            columns[4]: dport,
            columns[5]: time,
            columns[6]: status,
            columns[7]: image
        }
        login_sqlserver.insert_data(in_data)

    try:
        with open('gdata.pickle', 'wb') as file:
            pickle.dump(g, file)
    except:
        print('未知错误，无法储存实例。')

    login_sqlserver.close()

    return '', 204
