import pickle
import networkx as nx
import matplotlib.pyplot as plt
import subprocess
import datetime
import ids
import settings
import sqlserver
import prediction


def data_processing(data):
    """数据处理，返回特征值数组/源ip/源端口/目的ip/目的端口/时间"""
    data = data.split(',')
    feature = data[:-5]
    sip = data[-5]
    sport = data[-4]
    dip = data[-3]
    dport = data[-2]
    time = datetime.datetime.strptime(data[-1], "%Y-%m-%dT%H:%M:%S")

    return feature, sip, sport, dip, dport, time


def attack_path_prediction():
    """路径预测子线程函数"""
    # 执行命令
    process = subprocess.Popen(['./model_and_extractor/kdd99extractor', '-e'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 初始化
    setting = settings.Settings()
    login_sqlserver = sqlserver.Sqlserver(setting.sqlserver, setting.database, setting.sql_username,
                                          setting.sql_password,
                                          setting.message_table)
    columns = setting.message_table_columns
    g = nx.Graph()

    # 实时读取命令输出,并将数据进行处理预测后存入数据库
    while True:
        try:
            with open('gdata.pickle', 'rb') as file:
                g = pickle.load(file)
        except FileNotFoundError:
            print('未找到储存文件，使用空白实例')
        except:
            print('未知错误，无法读取实例。使用空白实例')

        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            data = output.decode().strip()
            feature, sip, sport, dip, dport, time = data_processing(data)  # 接收数据并转换为需要的形式
            status = ids.get_label(feature)  # 获取入侵检测返回的状态

            if status is 'Normal':
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
    print(f"致命错误，路径预测子线程已停止。子线程退出代码:{process.poll()}。程序已停止。")

    exit(1)

    # attack_path_prediction()

    # G = nx.Graph()
    # G.add_edge(1, 2, weight=4)  # 添加一条带有权重属性的边
    # G.add_edge(2, 3, weight=2)  # 添加另一条带有权重属性的边
    #
    # # 获取边属性
    # edge_weight = G[1][2]['weight']
    # print("Weight of edge (1, 2):", edge_weight)
    #
    # # 修改边属性
    # G[1][2]['weight'] = 7  # 修改边的权重
    #
    # # 绘制图形
    # plt.figure(figsize=(7.5, 7.5))
    # nx.draw(G, with_labels=True)
    # plt.show()
