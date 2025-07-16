import numpy as np
import pandas as pd
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


# 确保全局字体设置
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False   #负号处理

# 数据准备
# 模拟1000笔订单的原料使用量（标准化单位）  
np.random.seed(42)
orders = 1000

# 定义原料
ingredients = ['奶茶', '糖', '珍珠', '水果', '冰沙']

# 生成数据：70%经典奶茶，20%果茶，10%随机混合
data = np.zeros((orders, len(ingredients)))

# 经典奶茶订单（V1配方） 将1000 order 取前5组数据 每组数据5个成分值 
data[:700] = [0.8, 0.1, 0.1, 0, 0] + np.random.normal(0, 0.05, (700, 5))
data[700:900] = [0.2, 0, 0, 0.7, 0.1] + np.random.normal(0, 0.05, (200, 5))  # 果茶订单（V2配方）
data[900:] = np.random.uniform(0, 0.3, (100, 5))  # 随机混合订单

# 确保数值合理
data = np.clip(data, 0, 1)

# 创建DataFrame
df = pd.DataFrame(data, columns=ingredients)
print("前5笔订单数据：")
print(df.head().round(2))


# 数据标准化 StandardScaler去均值和方差归一化 计算协方差矩阵，特征分解特征值（λ）和特征向量（V），主成分分析
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

# PCA分析
pca = PCA()
pca.fit(scaled_data)


#解释方差比例表示每个主成分对整体数据差异的贡献度 依次打印每个主成分的解释方差比例
#根据解释方差比例，我们可以选择保留前几个主成分，以尽可能保留数据中的信息，同时减少计算复杂度。
#解释方差比例可以帮助我们确定应该保留多少个主成分。
# 一般来说，我们可以选择解释方差比例累积达到90%或95%的主成分。
print("\n获取特征值和特征向量：")
print("特征值（λ）:", pca.explained_variance_)
print("解释方差比例:", pca.explained_variance_ratio_)


#图示解释方差比例
plt.figure(figsize=(10, 4))
plt.bar(range(1,6), pca.explained_variance_ratio_, alpha=0.6)
#累计解释方差cumsum
#plt.plot(range(1,6), np.cumsum(pca.explained_variance_ratio_), 'bo-', alpha=0.6)
plt.axhline(y=0.9, color='green', linestyle='--', label='90%阈值')
plt.xlabel('单个主成分数量')
plt.ylabel('explained_variance_ratio')
plt.title('奶茶配方PCA分析')
plt.show()

# 绘制累计解释方差图
plt.figure(figsize=(10, 4))
plt.bar(range(1,6), pca.explained_variance_ratio_, alpha=0.6, label='单个方差比例')
plt.plot(range(1,6), np.cumsum(pca.explained_variance_ratio_), 'bo-', alpha=0.6,label='累计方差比例')
plt.axhline(y=0.9, color='r', linestyle='--', label='90%阈值')
plt.xlabel('单个主成分数量')
plt.ylabel('解释方差比例')
plt.title('奶茶配方PCA累计方差分析')
plt.legend()
plt.show()


# 特征向量（配方）
components = pca.components_
print("\n主成分（配方）：")
#目前我们选择保留PC1 PC2 0.53633439+0.22578135=0.76211274
for i, comp in enumerate(components[:2]):  # 只看前两个主成分
    print(f"PC{i+1}:", dict(zip(ingredients, comp.round(2))))

#主成分分析
pca = PCA(n_components=2)
pca.fit(scaled_data)
reduced_data = pca.transform(scaled_data)
# 绘制散点图
plt.figure(figsize=(8, 6))
#右上 >0 混合偏好型  右下PC1>0 PC2<0 经典奶茶偏好型  左下PC1<0 PC2<0 果茶偏好型  左上PC1<0 PC2>0 混合偏好型
plt.scatter(reduced_data[:, 0], reduced_data[:, 1])
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('奶茶配方PCA分析scatter')
plt.show()

# 找出右下象限的经典奶茶党（PC1>1, PC2<-0.5）
classic_lovers = df[(reduced_data[:,0]>1) & (reduced_data[:,1]<-0.5)]
print("经典奶茶党的平均订单：")
print(classic_lovers.mean().round(2))



# 主成分构成热力图
plt.figure(figsize=(8, 4))
plt.imshow(components[:2], cmap='coolwarm', aspect='auto')
plt.yticks([0,1], ['PC1（经典奶茶）','PC2（果茶）'])
plt.xticks(range(5), ingredients)
plt.colorbar(label='配方权重')
plt.title('主成分配方构成')
plt.show()



# 根据PCA结果构建推荐系统
class DrinkRecommender:
    def __init__(self, components):
        self.components = components  # 前两个主成分
        
    def recommend(self, customer_pref, n=3):
        """
        customer_pref: 顾客当前原料偏好（数组，如[0.5,0,0,0.3,0]）
        返回推荐加强/减弱的原料
        """
        # 计算顾客与各配方的相似度
        similarity = self.components.dot(customer_pref)
        
        # 生成推荐
        rec_idx = np.argsort(similarity)[-n:][::-1]  # 取相似度最高的n个
        
        recommendations = []
        for i in rec_idx:
            if similarity[i] > 0:
                action = "增加"
            else:
                action = "减少"
            recommendations.append(f"{action} {ingredients[i]} 的使用")
        
        return recommendations

# 初始化推荐器
recommender = DrinkRecommender(components[:2])

# 测试推荐
test_pref = [0.6, 0.1, 0.1, 0.2, 0]  # 一个喜欢经典奶茶但偶尔加水果的顾客
print("\n推荐结果：")
for rec in recommender.recommend(test_pref):
    print("-", rec)
