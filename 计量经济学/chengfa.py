import matplotlib.pyplot as plt
import networkx as nx
#from matplotlib.patches import FancyArrowPatch

# 创建决策树图
plt.figure(figsize=(15, 10))
G = nx.DiGraph()

# 添加节点（带决策层级）
nodes = {
    "Start": (0, 0),
    "Economic\nClimate": (1, 1),
    "Sector\nAnalysis": (1, -1),
    "Bull Market": (2, 1.5),
    "Bear Market": (2, 0.5),
    "Tech Sector": (2, -0.5),
    "Energy Sector": (2, -1.5),
    "Growth Stocks": (3, 2),
    "Value Stocks": (3, 1),
    "Defensive": (3, 0),
    "AI Companies": (3, -0.7),
    "Clean Energy": (3, -1.3),
    "Final Decision": (4, 0)
}

# 添加节点和连接边
G.add_nodes_from(nodes.keys())
for node, pos in nodes.items():
    G.add_node(node, pos=pos)

'''
权重（weight）：表示条件概率 
P(子节点∣父节点)需满足 ∑=1  ∑ρ=1（归一化）。

联合概率：路径上所有权重的乘积，例如：P(最终决策∣经济气候，科技行业)=0.6×0.4×0.9=0.216
'''
edges = [
    ("Start", "Economic\nClimate", {"weight": 0.6}),  # 条件概率权重 
    ("Start", "Sector\nAnalysis", {"weight": 0.4}),
    ("Economic\nClimate", "Bull Market", {"weight": 0.7}), # 条件概率P(子节点∣父节点) P(Bull|Economic)
    
     ("Economic\nClimate", "Bear Market", {"weight": 0.2}), #GDP>3%
    ("Sector\nAnalysis", "Tech Sector", {"weight": 0.5}),
    ("Sector\nAnalysis", "Energy Sector", {"weight": 0.5}),
    ("Bull Market", "Growth Stocks", {"weight": 0.8, "prob": 0.6*0.7*0.8}),  # 添加联合概率  P(Growth|Bull)×P(Bull|Economic)×P(Economic)=0.6×0.7×0.8=0.336
    ("Bull Market", "Value Stocks", {"weight": 0.2, "prob": 0.6*0.7*0.2}),    #P(Value|Bull)×P(Bull|Economic)×P(Economic)=0.6×0.7×0.2=0.084
    ("Bear Market", "Value Stocks", {"weight": 0.4, "prob": 0.6*0.3*0.4}),   # P(Value|Bear)×P(Bear|Economic)×P(Economic)=0.6×0.3×0.4=0.072
    ("Bear Market", "Defensive", {"weight": 0.6, "prob": 0.6*0.3*0.6}),    # P(Defensive|Bear)×P(Bear|Economic)×P(Economic)=0.6×0.3×0.6=0.108
    ("Tech Sector", "AI Companies", {"weight": 0.9, "prob": 0.4*0.5*0.9}), # P(AI|Tech)×P(Tech|Sector)×P(Sector)=0.4×0.5×0.9=0.18
    ("Tech Sector", "Clean Energy", {"weight": 0.1, "prob": 0.4*0.5*0.1}),  # P(Clean|Tech)×P(Tech|Sector)×P(Sector)=0.4×0.5×0.1=0.02
    ("Energy Sector", "Clean Energy", {"weight": 0.8, "prob": 0.4*0.5*0.8}),# P(Clean|Energy)×P(Energy|Sector)×P(Sector)=0.4×0.5×0.8=0.16
    ("Energy Sector", "AI Companies", {"weight": 0.2, "prob": 0.4*0.5*0.2}),# P(AI|Energy)×P(Energy|Sector)×P(Sector)=0.4×0.5×0.2=0.04
    ("Growth Stocks", "Final Decision"),
    ("Value Stocks", "Final Decision"),
    ("Defensive", "Final Decision"),
    ("AI Companies", "Final Decision"),
    ("Clean Energy", "Final Decision")
]
print(edges)
G.add_edges_from(edges)

# 绘制树形结构
pos = nx.get_node_attributes(G, 'pos')
nx.draw_networkx_nodes(G, pos, node_size=5000, node_color='lightblue', alpha=0.9)
nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')

# 绘制带权重的边
edge_labels = {}
for u, v, d in G.edges(data=True):
    print(f"{u} -> {v}: {d}")
    if 'prob' in d:
        edge_labels[(u, v)] = f"{d['weight']:.1f}\nP={d['prob']:.3f}"
    elif 'weight' in d:
        edge_labels[(u, v)] = f"{d['weight']:.1f}"

nx.draw_networkx_edges(G, pos, width=2, edge_color='gray', arrows=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)



plt.title("Investment Decision Process Using Multiplication Rule")

# 添加文字说明
plt.text(4.2, 0, "-Final Decision:\n- Stock Selection\n- Position Sizing",
         bbox=dict(facecolor='lightgreen', alpha=0.7,boxstyle='round,pad=0.8', edgecolor='darkgreen'))

# 添加图例
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', label='Decision Node',
               markerfacecolor='lightblue', markersize=15),
    plt.Line2D([0], [0], color='gray', lw=2, label='Transition Probability'),
    plt.Line2D([0], [0], marker='$P$', color='w', label='Joint Probability',
               markerfacecolor='black', markersize=15)
]
plt.legend(handles=legend_elements, loc='upper left')

plt.box(False)
plt.tight_layout()
plt.show()

total_prob = 0.336 + 0.156 + 0.108 + 0.220 + 0.180  # = 1.0
print(f"Total Probability: {total_prob:.3f}")
allocation = {
    "Growth Stocks": 0.336 / total_prob * 100,  # ≈33.6%
    "AI Companies": 0.220 / total_prob * 100,   # ≈22.0%
    "Clean Energy": 0.180 / total_prob * 100,   # ≈18.0%
    "Value Stocks": 0.156 / total_prob * 100,   # ≈15.6%
    "Defensive": 0.108 / total_prob * 100       # ≈10.8%
}



sum_allocation = sum(allocation.values())             # 输出 100.0
print(f"Sum of Probabilities: {total_prob:.3f}")

labels = allocation.keys()
sizes = allocation.values()

plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.axis('equal')  # 正圆形
plt.title('Portfolio Allocation Based on Joint Probability')
plt.show()