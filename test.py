import networkx as nx

# 创建一个简单的图
G = nx.Graph()
G.add_edges_from([(1, '2'), (1, 3), (2, 4), (3, 4)])

# 指定一个当前节点
current_node = 1

# 找到当前节点的所有相邻节点
neighbors = G.edges(current_node, data=True)

for i in neighbors:
    print(i)
