


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

import pandas as pd

from sklearn import cluster, covariance, manifold

#https://www.nasdaq.com/

'''通过亲和传播聚类（Affinity Propagation）对股票收益率数据进行相关性分组。
计算每日收益率（价格变化的百分比）
构建收益率的相关性矩阵,用亲和传播算法根据相关性自动分组 '''

#读取Excel所有Sheet到字典
stock_data = pd.read_excel('D:\\tool\\CQF\\pachong\\zhenghe.xlsx', sheet_name=None, index_col='Date')
print(stock_data.keys())

symbol_dict = {
    #'TOT': 'Total',
    'APPL': 'APPL',
    'AMZN': 'AMZN',
    'Tesla': 'Tesla',
    'AIG': 'AIG',
    'DELL':'DELL',
    'IBM':'IBM',
    'Cisco':'Cisco',
    'DuPont':'DuPont',
    'General Dynamics':'General Dynamics',
    'CocaCola':'CocaCola',
    'Microsoft':'Microsoft',
    'JPMorgan':'JPMorgan',
    'Blackstone':'Blackstone',
    'General Electric':'General Electric',
    'TXN':'TXN',
    'CSCO':'CSCO',
    'INTC':'INTC',
    'Sony':'Sony',
    'Pfizer':'Pfizer'
    }

symbols, names = np.array(sorted(symbol_dict.items())).T

#定义一个 quotes 价格列表

quotes = []
for ticker, df in stock_data.items():
    # 统一列名大小写（确保字段可访问）
    df = df.rename(columns={
        'Date':'Date',
        'Close':'Close',
        'Volume':'Volume',
        'Open': 'Open',
        'Low':'Low',
        'High':'High',   

    })
    quotes.append(df)  #将 标准化以后的字段 列表 追加到 quotes[]里
#提取价格矩阵
close_prices = np.vstack([q['Close'] for q in quotes])
open_prices = np.vstack([q['Open'] for q in quotes])


# 验证结果
print("股票代码:", list(stock_data.keys()))
print("开盘价矩阵示例:\n", open_prices[:4, :5])  # 前2只股票的前5个交易日
print("收盘价矩阵示例:\n", close_prices[:4, :5])

#对每只股票的 (close - open) 序列进行标准化（减去均值、除以标准差），消除不同股票价格量纲的影响。
'''使用的 close price - open price 并非直接计算相关性，
而是通过以下步骤构建 协方差矩阵 和 相关性网络，目的是分析股票之间的 日内价格变动模式的相似性'''
variation = close_prices - open_prices

edge_model = covariance.GraphicalLassoCV()   #稀疏逆协方差估计

# standardize the time series: using correlations rather than covariance

X = variation.copy().T   ## 转置数据矩阵（资产×时间序列）
X /= X.std(axis=0)     # 标准化每个资产的时间序列
edge_model.fit(X)    #拟合数据
print("标准化后的特征矩阵 X (n_features x n_samples):\n", X)
#资产聚类 （根据相关性分组） 亲和传播聚类算法（Affinity Propagation），根据相似性对样本进行分组
# 输入协方差矩阵（反映资产联动性）
#总共分成了 11组 
_, labels = cluster.affinity_propagation(edge_model.covariance_,
                                         random_state=0)
print(labels.max())
n_labels = labels.max()


for i in range(n_labels + 1):
    print('Cluster %i: %s' % ((i + 1), ', '.join(names[labels == i])))

# 将高维相关性映射到2D平面 #流形降维 模型LLE   
#第一次 X.T：适配 sklearn 的输入格式（样本×特征
#n_components 降维后的维度，如果后续需要聚类或分类，2维特征已足够
#对于 n 个样本，n_neighbors 必须满足 1 < n_neighbors < n - 1
#eigen_solver='dense' 特征求解器
#临近样本的数量调整为3，目前只有 8家公司，原始代码是 6

node_position_model = manifold.LocallyLinearEmbedding(
   
    n_components=2, eigen_solver='dense', n_neighbors=3)   
#二次转置 #将原始样本X 转置为X.T
#第二次 .T：适配 matplotlib 的绘图格式（维度×数据点） 以便 scatter绘图
embedding = node_position_model.fit_transform(X.T).T  
# Visualization
plt.figure(1, facecolor='w', figsize=(10, 8))
plt.clf()
ax = plt.axes([0., 0., 1., 1.])
plt.axis('off')

# Display a graph of the partial correlations
partial_correlations = edge_model.precision_.copy()
#节点大小 d = 1 / sqrt(precision_.diagonal())，波动率越大节点越小。
d = 1 / np.sqrt(np.diag(partial_correlations))
partial_correlations *= d
partial_correlations *= d[:, np.newaxis]
#仅显示显著偏相关系数（阈值0.02）
non_zero = (np.abs(np.triu(partial_correlations, k=1)) > 0.02)


# Plot the nodes using the coordinates of our embedding
#大小与精度矩阵对角线倒数相关（反映资产波动）
plt.scatter(embedding[0], embedding[1], s=100 * d ** 2, c=labels,
            cmap=plt.cm.nipy_spectral)

# Plot the edges
start_idx, end_idx = np.where(non_zero)
# a sequence of (*line0*, *line1*, *line2*), where::
#            linen = (x0, y0), (x1, y1), ... (xm, ym)
segments = [[embedding[:, start], embedding[:, stop]]
            for start, stop in zip(start_idx, end_idx)]
values = np.abs(partial_correlations[non_zero])
#用于绘制网络中资产之间的相关性边，并通过颜色和宽度直观展示相关性强弱
#红色系适合表示强度（如相关性），_r 反转后使高值更醒目
lc = LineCollection(segments,  #线段坐标
                    zorder=0, cmap=plt.cm.hot_r,  #颜色映射（红-黑渐变，反向）
                    norm=plt.Normalize(0, .7 * values.max()))
lc.set_array(values)
lc.set_linewidths(15 * values)
ax.add_collection(lc)

# Add a label to each node. The challenge here is that we want to
# position the labels to avoid overlap with other labels
for index, (name, label, (x, y)) in enumerate(
        zip(names, labels, embedding.T)):

    dx = x - embedding[0]
    dx[index] = 1
    dy = y - embedding[1]
    dy[index] = 1
    this_dx = dx[np.argmin(np.abs(dy))]
    this_dy = dy[np.argmin(np.abs(dx))]
    if this_dx > 0:
        horizontalalignment = 'left'
        x = x + .002
    else:
        horizontalalignment = 'right'
        x = x - .002
    if this_dy > 0:
        verticalalignment = 'bottom'
        y = y + .002
    else:
        verticalalignment = 'top'
        y = y - .002
    plt.text(x, y, name, size=10,
             horizontalalignment=horizontalalignment,
             verticalalignment=verticalalignment,
             bbox=dict(facecolor='w',
                       edgecolor=plt.cm.nipy_spectral(label / float(n_labels)),
                       alpha=.6))

plt.xlim(embedding[0].min() - .15 * embedding[0].ptp(),
         embedding[0].max() + .10 * embedding[0].ptp(),)
plt.ylim(embedding[1].min() - .03 * embedding[1].ptp(),
         embedding[1].max() + .03 * embedding[1].ptp())

plt.show()


