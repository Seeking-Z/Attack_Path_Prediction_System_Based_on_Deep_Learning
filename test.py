import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_edge(1, 2, weight=4)  # 添加一条带有权重属性的边
G.add_edge(2, 3, weight=2)  # 添加另一条带有权重属性的边

# 获取边属性
edge_weight = G[1][2]['weight']
print("Weight of edge (1, 2):", edge_weight)

# 修改边属性
G[1][2]['weight'] = 7  # 修改边的权重

# 绘制图形
plt.figure(figsize=(7.5, 7.5))
nx.draw(G, with_labels=True)
plt.show()