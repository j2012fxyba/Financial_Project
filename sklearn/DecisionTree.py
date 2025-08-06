import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import plot_tree



# 确保全局字体设置
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False   #负号处理

data = {
    '色泽': ['青绿', '乌黑', '浅白', '乌黑', '浅白', '青绿', '乌黑', '乌黑', '青绿', '浅白'],
    '根蒂': ['卷缩', '卷缩', '硬挺', '稍卷', '稍卷', '卷缩', '稍卷', '卷缩', '硬挺', '硬挺'],
    '敲声': ['浊响', '沉闷', '清脆', '浊响', '浊响', '浊响', '沉闷', '浊响', '清脆', '沉闷'],
    '纹理': ['清晰', '清晰', '模糊', '稍糊', '清晰', '稍糊', '稍糊', '清晰', '模糊', '模糊'],
    '脐部': ['凹陷', '凹陷', '平坦', '凹陷', '稍凹', '稍凹', '稍凹', '凹陷', '平坦', '稍凹'],
    '触感': ['硬滑', '硬滑', '硬滑', '硬滑', '软粘', '软粘', '硬滑', '硬滑', '软粘', '硬滑'],
    '好瓜': [1, 1, 0, 1, 0, 1, 0, 1, 0, 0] 
}
df = pd.DataFrame(data)

# 数据编码
df_encoded = df.copy()
le = LabelEncoder()
for col in df.columns[:-1]:
    df_encoded[col] = le.fit_transform(df[col])

# 构建决策树（限制深度模拟手动选择）
clf = DecisionTreeClassifier(
    criterion='entropy',
    max_depth=2,  # 限制深度以匹配纹理→脐部的分裂
    random_state=42
)
clf.fit(df_encoded[['纹理', '脐部', '触感']], df_encoded['好瓜'])

# 绘制树图
plt.figure(figsize=(15, 8))
plot_tree(clf,
          feature_names=['纹理', '脐部', '触感'],
          class_names=['坏瓜', '好瓜'],
          filled=True,
          rounded=True,
          proportion=True,
          impurity=True,
          fontsize=10)
plt.title("决策树分裂过程（以纹理为根节点）\n(节点显示: 特征[熵] → 样本分布)", pad=20)
plt.show()



# 标签编码并保存编码器
le_dict = {}  # 初始化字典存储编码器
for col in df.columns[:-1]:  # 对每个特征列编码（除最后一列标签）
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])  # 训练并转换
    le_dict[col] = le  # 保存编码器到字典

# 训练模型
clf = DecisionTreeClassifier(criterion='entropy', max_depth=3)
clf.fit(df.iloc[:, :-1], df['好瓜'])



# 使用之前保存的LabelEncoder编码新样本
# 新样本
new_melon = {
    '色泽': '乌黑', 
    '根蒂': '稍卷',
    '敲声': '浊响',
    '纹理': '清晰',
    '脐部': '稍凹',
    '触感': '软粘'
}

# 使用le_dict编码新样本
new_encoded = []
for col in df.columns[:-1]:
    le = le_dict[col]  # 取出对应特征的编码器
    new_encoded.append(le.transform([new_melon[col]])[0])  # 编码

# 预测
pred = clf.predict([new_encoded])[0]
print(f"新样本: {new_melon}")
print(f"编码后的新样本: {new_encoded}")
print(pred)




# 设置图像大小
plt.figure(figsize=(18, 10))

# 绘制决策树
plot_tree(clf, 
          feature_names=df.columns[:-1], 
          class_names=['坏瓜', '好瓜'],
          filled=True,
          rounded=True,
          proportion=True,
          fontsize=10)

# 标注新样本路径
plt.annotate('新样本路径',
             xy=(0.6, 0.5), 
             xytext=(0.1, 0.3),
             arrowprops=dict(arrowstyle="->", color='red', linewidth=2),
             fontsize=12, color='red',
             bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8))

plt.title("新西瓜样本的决策路径\n(红色箭头标注预测路径)", pad=20,fontsize=14)
plt.show()
