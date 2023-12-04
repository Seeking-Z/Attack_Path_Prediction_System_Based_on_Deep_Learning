import pickle

import matplotlib.pyplot as plt
import networkx as nx


def base64_graph(g):
    """将图绘制并转为base64编码"""
    pos = nx.spring_layout(g)

    # 获取节点和边的属性
    node_labels = nx.get_node_attributes(g, 'percent')
    edge_labels = nx.get_edge_attributes(g, 'percent')

    # 设置换行
    node_labels_wrap = {k: f"{k}\n{round(v * 100, 2)}" for k, v in node_labels.items()}
    for i in node_labels_wrap:
        print(i)

    plt.figure(figsize=(8, 6))

    # 绘制图形和节点，显示标签换行
    nx.draw(g, pos, with_labels=False)
    nx.draw_networkx_labels(g, pos, labels=node_labels_wrap)

    # 绘制边的标签
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)

    plt.show()


with open('gdata.pickle', 'rb') as file:
    g = pickle.load(file)
base64_graph(g)
