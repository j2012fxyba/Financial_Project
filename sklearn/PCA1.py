
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

'''
3个产区的 3种葡萄  13种成分 178条数据 
1.Alcohol 
2.Malic acid 
3.Ash 
4.Alcalinity of ash 
5.Magnesium 
6.Total phenols 
7.Flavanoids
8.Nonflavanoid phenols
9.Proanthocyanins
10.Color intensity
11.Hue
12.OD280/OD315 of diluted wines
13.Proline
酒精 苹果酸 灰分 灰分的碱度 镁 总酚 类黄酮 非类黄酮酚 花色苷 色泽强度 色调 稀释葡萄酒的OD280/OD315 脯氨酸
'''




# 确保全局字体设置
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False   #负号处理

# 设置随机种子保证可重复性
np.random.seed(42)

# 定义13种葡萄成分名称（基于真实葡萄成分）
components = [
    '糖度(Brix)', '总酸度(g/L)', 'pH值', 
    '花青素(mg/L)', '总酚(mg/L)', '单宁(mg/L)',
    '酒石酸(g/L)', '苹果酸(g/L)', '柠檬酸(g/L)',
    '钾含量(mg/L)', '总抗氧化能力(ORAC)',
    '挥发性酯类(mg/L)', '类黄酮(mg/L)'
]


# # 为3种来源定义不同的成分特征（均值±标准差）
source_profiles = {
    'A': {  # 产地A：高糖高酚
        '糖度(Brix)': (20, 1.5), '总酸度(g/L)': (5, 0.8), 'pH值': (3.4, 0.1),
        '花青素(mg/L)': (350, 50), '总酚(mg/L)': (2800, 300), '单宁(mg/L)': (1800, 200),
        '酒石酸(g/L)': (3.5, 0.5), '苹果酸(g/L)': (1.2, 0.3), '柠檬酸(g/L)': (0.3, 0.1),
        '钾含量(mg/L)': (1500, 200), '总抗氧化能力(ORAC)': (4500, 500),
        '挥发性酯类(mg/L)': (120, 20), '类黄酮(mg/L)': (800, 100)
    },
    'B': {  # 产地B：中等糖酸比
        '糖度(Brix)': (18, 1.2), '总酸度(g/L)': (6, 0.7), 'pH值': (3.2, 0.1),
        '花青素(mg/L)': (300, 40), '总酚(mg/L)': (2500, 250), '单宁(mg/L)': (1600, 180),
        '酒石酸(g/L)': (4.0, 0.4), '苹果酸(g/L)': (1.5, 0.2), '柠檬酸(g/L)': (0.4, 0.1),
        '钾含量(mg/L)': (1700, 180), '总抗氧化能力(ORAC)': (4000, 400),
        '挥发性酯类(mg/L)': (100, 15), '类黄酮(mg/L)': (700, 80)
    },
    'C': {  # 产地C：低糖高酸
        '糖度(Brix)': (16, 1.0), '总酸度(g/L)': (7, 0.9), 'pH值': (3.0, 0.1),
        '花青素(mg/L)': (250, 30), '总酚(mg/L)': (2200, 200), '单宁(mg/L)': (1400, 150),
        '酒石酸(g/L)': (4.5, 0.6), '苹果酸(g/L)': (2.0, 0.3), '柠檬酸(g/L)': (0.5, 0.1),
        '钾含量(mg/L)': (1900, 150), '总抗氧化能力(ORAC)': (3500, 300),
        '挥发性酯类(mg/L)': (80, 10), '类黄酮(mg/L)': (600, 70)
    }
}

# 生成数据 (178个样本)
n_samples = 178
sources = ['A', 'B', 'C']
source_counts = [60, 58, 60]  # 三个来源的样本数

# 创建数据数组
data = []
labels = []
for source, count in zip(sources, source_counts):
    for _ in range(count):
        sample = []
        for comp in components:
            mean, std = source_profiles[source][comp]
            sample.append(np.random.normal(mean, std))
        data.append(sample)
        labels.append(source)

# 转换为numpy数组
X = np.array(data)  # (178, 13) 特征矩阵
y = np.array(labels) # (178,) 标签

print(X)
print(y)

# 标准化数据
scaler = StandardScaler()
X_std = scaler.fit_transform(X)

print('StandardScaler 以后的值',X_std)

# 假设X_std是已标准化的数据 (178 x 13)
pca = PCA(n_components=None)  # 不降维，计算所有主成分
pca.fit(X_std)

#保存第一次不降维pca信息
pca_components = pca.components_  # 获取主成分
print('不降维pca主成分方向：',pca_components)
#variance=pca.explained_variance_


# 计算累积方差贡献率
cumulative_variance = np.cumsum(pca.explained_variance_ratio_)

# 设定解释率阈值（如90%）
threshold = 0.9
k = np.argmax(cumulative_variance >= threshold)  

print(k) 

#Cumulative Percent Variance，简称CPV，是主成分分析（PCA）中用来衡量主成分解释数据方差的指标。
#CPV表示前k个主成分解释的数据方差占总数据方差的百分比。
print(f"主成分数量k={k}（累积解释方差={cumulative_variance[k-1]:.2%}）")


# 重新用k值降维
pca_k = PCA(n_components=k)
X_pca_k = pca_k.fit_transform(X_std)

# 训练阶段
from joblib import dump
pca = PCA(n_components=9).fit(X_std)
dump(pca, 'pca_model.joblib')


# 查看降维后数据形状
print("降维后数据形状:", X_pca_k.shape)  # (178, 9)

# 保存降维后的数据（供后续分析）
np.save('grape_data_pca.npy', X_pca_k)
np.save('grape_labels.npy', y)  # 保存标签
np.save('variance_ratio.npy',pca.explained_variance_ratio_ )#查看方差贡献率


from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_pca_k, y)  # y为来源标签


# 定义新葡萄的特征范围（假设与训练数据分布相似）

new_data = {
    'A': {  # 产地A：高糖高酚
        '糖度(Brix)': (30, 1.5), '总酸度(g/L)': (9, 0.8), 'pH值': (3.0, 0.1),
        '花青素(mg/L)': (300, 50), '总酚(mg/L)': (2500, 300), '单宁(mg/L)': (2000, 200),
        '酒石酸(g/L)': (3.8, 0.5), '苹果酸(g/L)': (1.5, 0.3), '柠檬酸(g/L)': (0.3, 0.1),
        '钾含量(mg/L)': (1500, 200), '总抗氧化能力(ORAC)': (4500, 500),
        '挥发性酯类(mg/L)': (120, 20), '类黄酮(mg/L)': (800, 100)
    },
    'B': {  # 产地B：中等糖酸比
        '糖度(Brix)': (18, 1.2), '总酸度(g/L)': (6, 0.7), 'pH值': (3.2, 0.1),
        '花青素(mg/L)': (350, 40), '总酚(mg/L)': (2500, 250), '单宁(mg/L)': (1600, 180),
        '酒石酸(g/L)': (3.8, 0.4), '苹果酸(g/L)': (1.7, 0.2), '柠檬酸(g/L)': (0.6, 0.1),
        '钾含量(mg/L)': (1700, 180), '总抗氧化能力(ORAC)': (4000, 400),
        '挥发性酯类(mg/L)': (100, 15), '类黄酮(mg/L)': (700, 80)
    },
     'C': {  # 产地C：低糖高酸
        '糖度(Brix)': (16, 1.0), '总酸度(g/L)': (5, 0.9), 'pH值': (3.0, 0.1),
        '花青素(mg/L)': (230, 30), '总酚(mg/L)': (1800, 200), '单宁(mg/L)': (1400, 150),
        '酒石酸(g/L)': (4.5, 0.6), '苹果酸(g/L)': (18, 0.3), '柠檬酸(g/L)': (0.4, 0.1),
        '钾含量(mg/L)': (1900, 150), '总抗氧化能力(ORAC)': (3500, 300),
        '挥发性酯类(mg/L)': (80, 10), '类黄酮(mg/L)': (600, 70)
    }
}



# 生成测试数据（100个样本）
n_test = [33, 33, 34]  # 每个类型的样本数
X_new = []
y_new_true = []
for i, (type_name, type_params) in enumerate(new_data.items()):
    for _ in range(n_test[i]):
        sample = [np.random.normal(type_params[comp][0], type_params[comp][1]) for comp in components]
        X_new.append(sample)
        y_new_true.append(type_name)

# 比较训练测试数据统计量
print("训练数据均值:", scaler.mean_)
X_new = np.array(X_new)  # (100, 13)
print("测试数据均值:", X_new.mean(axis=0))
y_new_true = np.array(y_new_true)  # (100,)

'''
在机器学习的工作流程中，预处理参数（如均值、标准差、PCA主成分等）应该从训练集中学习得到，
然后应用于测试集，而不是从测试集中重新计算。
这样可以避免数据泄露（data leakage）问题，确保模型评估的准确性
'''

# ===== 测试/应用阶段 =====

# 加载预处理参数
scaler_mean = np.load('scaler_mean.npy')
scaler_scale = np.load('scaler_scale.npy')


#标准化测试集数据，用训练集产生的mean和scale  '''注意：典型的广播（broadcasting）错误'''

scaler_mean=scaler_mean.flatten()
scaler_scale=scaler_scale.flatten()
X_new_std = (X_new - scaler_mean) / scaler_scale



#pca降维
from joblib import load
print('加载之前训练pca模型')
pca = load('pca_model.joblib')  # 直接加载完整对象

print('将测试集数据投影到主成分空间')
X_new_pca = pca.transform(X_new_std)
#预测前先将维度，将测试数据和训练数据对齐，之前训练数据降维了9 
print('测试集降维',X_new_pca.shape[1])



y_new_pred = model.predict(X_new_pca)
y_new_proba = model.predict_proba(X_new_pca)
 

# # 输出结果
results = pd.DataFrame({
    '真实类别': y_new_true,
    '预测类别': y_new_pred,
    'A概率': y_new_proba[:, 0],
    'B概率': y_new_proba[:, 1],
    'C概率': y_new_proba[:, 2]
})
print(results.head(10))


# # 分类报告
from sklearn.metrics import classification_report

print("\n分类报告:")
print(classification_report(y_new_true, y_new_pred))


from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_new_true, y_new_pred)
sns.heatmap(cm, annot=True, fmt='d', xticklabels=model.classes_, yticklabels=model.classes_)
plt.xlabel('预测标签')
plt.ylabel('真实标签')
plt.title('混淆矩阵')
plt.show()




plt.figure(figsize=(8, 4))
plt.plot(range(1, len(cumulative_variance)+1), cumulative_variance, 'bo-')
plt.axhline(y=threshold, color='r', linestyle='--', label=f'阈值 ({threshold:.0%})')
plt.axvline(x=k, color='g', linestyle=':', label=f'k={k}')
plt.xlabel('主成分数量')
plt.ylabel('累积解释方差')
plt.title('PCA累积方差贡献率')
plt.legend()
plt.grid()
plt.show()


# 创建直方图
plt.figure(figsize=(10, 5))

# 绘制直方图（每个主成分的贡献）
bars = plt.bar(range(1, len(cumulative_variance)+1), 
               np.diff(np.insert(cumulative_variance, 0, 0)),  # 计算单个主成分的贡献
               alpha=0.6, color='skyblue', edgecolor='black',
               label='单个主成分贡献率')

# 添加累积贡献率曲线（红色点线）
plt.plot(range(1, len(cumulative_variance)+1), cumulative_variance, 
         'ro--', linewidth=1, markersize=5, label='累积贡献率')

# 添加阈值线和k值标记
plt.axhline(y=threshold, color='r', linestyle='--', linewidth=1, label=f'阈值 ({threshold:.0%})')
plt.axvline(x=k, color='g', linestyle=':', linewidth=2, label=f'k={k}')

# 标记关键点
plt.scatter(k, cumulative_variance[k-1], color='green', zorder=5, s=100)
plt.annotate(f'PC{k}\n{cumulative_variance[k-1]:.1%}', 
             xy=(k, cumulative_variance[k-1]), 
             xytext=(k+0.5, cumulative_variance[k-1]-0.1),
             arrowprops=dict(arrowstyle='->'))

# 图表美化
plt.xlabel('主成分编号 (PC1-PC{})'.format(len(cumulative_variance)), fontsize=10)
plt.ylabel('方差贡献率', fontsize=10)
plt.title('PCA方差贡献分析（直方图+累积曲线）', fontsize=14, pad=20)
plt.xticks(range(1, len(cumulative_variance)+1))
plt.ylim(0, 1.05)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

plt.show()


# 载荷矩阵 (13 x k)
loadings = pca_k.components_.T  # 转置为(13, k)


# 热图可视化
import seaborn as sns
plt.figure(figsize=(10, 6))
sns.heatmap(loadings, annot=True, cmap='coolwarm', 
            xticklabels=[f'PC{i+1}' for i in range(k)],
            yticklabels=components)
plt.title('主成分载荷矩阵')
plt.tight_layout()#自动调整子图参数
plt.show()


plt.scatter(X_pca_k[:, 0], X_pca_k[:, 1], c=pd.factorize(y)[0], cmap='viridis')
plt.xlabel('PC1 (解释方差: {:.1%})'.format(pca_k.explained_variance_ratio_[0]))
plt.ylabel('PC2 (解释方差: {:.1%})'.format(pca_k.explained_variance_ratio_[1]))
plt.colorbar(label='来源')
plt.title('前两主成分可视化（k={}）'.format(k))
plt.show()

