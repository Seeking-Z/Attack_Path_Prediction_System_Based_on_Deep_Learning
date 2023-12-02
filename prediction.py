import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def add_nodes_and_edges(g, sip, dip, status, setting):
    """添加节点和边进图"""
    g.add_node(sip)

    g.add_node(dip)

    g.add_edge(sip, dip)

    if status == 'Normal':
        if 'status' not in g.nodes[sip]:
            g.nodes[sip]['status'] = 'Normal'
            g.nodes[sip]['percent'] = setting.status['Normal']
        if 'percent' not in g.edges[(sip, dip)]:
            g.edges[(sip, dip)]['percent'] = 0
    else:
        g.nodes[sip]['status'] = 'Down'
        g.nodes[sip]['percent'] = setting.status['Down']
        g.edges[(sip, dip)]['percent'] = 1

    if 'percent' not in g.nodes[dip]:
        g.nodes[dip]['status'] = status
        g.nodes[dip]['percent'] = setting.status[status]

    if g.nodes[dip]['percent'] < setting.status[status]:
        g.nodes[dip]['status'] = status
        g.nodes[dip]['percent'] = setting.status[status]

    if 'connect' in g.nodes[sip]:
        g.nodes[sip]['connect'] += 1
    else:
        g.nodes[sip]['connect'] = 1

    if 'connect' in g.nodes[dip]:
        g.nodes[dip]['connect'] += 1
    else:
        g.nodes[dip]['connect'] = 1


def neighbor_prediction(g, node):
    """对一个节点向相邻节点的攻击概率进行预测"""
    sum_connect = 0

    neighbors = g.edges(node)

    for i, j in neighbors:
        sum_connect += g.nodes[j]['connect']

    for i, j in neighbors:
        percent = g.nodes[j]['connect'] / sum_connect * g.nodes[i]['percent']
        if percent > g.edges[(i, j)]['percent']:
            g.edges[(i, j)]['percent'] = percent


def base64_graph(g):
    """将图绘制并转为base64编码"""
    pos = nx.circular_layout(g)

    # 获取节点和边的属性
    node_labels = nx.get_node_attributes(g, 'percent')
    edge_labels = nx.get_edge_attributes(g, 'percent')

    # 设置换行
    node_labels_wrap = {k: f"{k}\n{v}" for k, v in node_labels.items()}

    # 绘制图形和节点，显示标签换行
    nx.draw(g, pos, with_labels=False)
    nx.draw_networkx_labels(g, pos, labels=node_labels_wrap)

    # 绘制边的标签
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)

    # 转为base64
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    figdata_str = str(figdata_png, "utf-8")

    return figdata_str


def prediction(g, sip, dip, status, setting):
    """对攻击路径进行预测，分为向图添加节点和边，预测，返回图的base64编码三步"""
    add_nodes_and_edges(g, sip, dip, status, setting)

    neighbor_prediction(g, sip)
    neighbor_prediction(g, dip)

    return base64_graph(g)

# data = ['37,udp,other,SF,6048,0,0,0,0,0,0,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0,0,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,172.22.32.1,5353,224.0.0.251,5353,2023-05-22T08:58:42',
#         '0,udp,domain_u,SF,138,179,0,0,0,0,0,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0,0,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,172.22.43.47,44004,172.22.32.1,53,2023-05-22T08:58:31',
#         '6,icmp,eco_i,SF,686,0,0,0,0,0,0,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0,0,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,172.22.43.47,0,110.242.68.66,0,2023-05-22T08:58:38',
#         '6,icmp,ecr_i,SF,686,0,0,0,0,0,0,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0,0,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,110.242.68.66,0,172.22.43.47,0,2023-05-22T08:58:38',
#         '10,udp,domain_u,SF,86,344,0,0,0,1,1,0.00,0.00,0.00,0.00,1.00,0.00,0.00,1,1,1.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,172.22.43.47,42918,172.22.32.1,53,2023-05-22T08:58:42']
# g = nx.Graph()
# setting = settings.Settings()
# for i in data:
#     feature, sip, sport, dip, dport, time = data_processing(i)
#     status = ids.get_label(feature)
#     print(status)
#     print(prediction(g, sip, dip, status, setting))

# html = f'<img src="data:image/png;base64,{figdata_str}"/>'
# print(html)

# try:
#     with open('gdata.pickle', 'rb') as file:
#         g = pickle.load(file)
# except FileNotFoundError:
#     print('未找到储存文件，使用空白实例')
# except:
#     print('未知错误，无法读取实例。使用空白实例')
#
# try:
#     with open('gdata.pickle', 'wb') as file:
#         pickle.dump(g, file)
# except:
#     print('未知错误，无法储存实例。')
