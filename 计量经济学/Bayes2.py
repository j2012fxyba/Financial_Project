import shap
import numpy as np

from sklearn.naive_bayes import GaussianNB #提供了多种朴素贝叶斯分类器的实现 GaussianNB假设特征服从高斯分布（连续数据）


# 加载金融数据
# data = pd.read_csv('financial_data.csv')
# X = data.drop('target', axis=1)
# y = data['target']

# 模拟数据
X_train = np.random.randn(1000, 3)  # 特征
y_train = np.random.choice([0, 1], size=1000, p=[0.92, 0.08])  # 标签

# 训练朴素贝叶斯模型
model = GaussianNB()
model.fit(X_train, y_train)

# 创建SHAP解释器
explainer = shap.Explainer(model.predict_proba, X_train)

# 要解释的新样本
sample = np.array([[1.5, 0.8, 1.0]])

# 计算SHAP值
shap_values = explainer(sample)

# 1. 打印基础值和预测概率
print("=== 基础值与预测概率 ===")
print(f"基础值（模型平均输出）: {shap_values.base_values[0][1]:.4f}")
print(f"实际预测概率: {model.predict_proba(sample)[0][1]:.4f}\n")

# 2. 打印每个特征的贡献值
print("=== 特征贡献分解 ===")
feature_names = X_train.columns if hasattr(X_train, 'columns') else [f"Feature_{i}" for i in range(X_train.shape[1])]

for i in range(len(feature_names)):
    print(f"{feature_names[i]}: {shap_values.values[0][i][1]:.4f}")

# 3. 计算累积效应
print("\n=== 累积效应验证 ===")
cumulative_effect = shap_values.base_values[0][1] + shap_values.values[0,:,1].sum()
print(f"基础值 + 总特征贡献: {cumulative_effect:.4f}")
print(f"模型直接输出的概率: {model.predict_proba(sample)[0][1]:.4f}")

# 4. 输出逐步累积概率
print("\n=== 逐步累积概率 ===")
current_value = shap_values.base_values[0][1]
print(f"起始值: {current_value:.4f}")

# 按贡献绝对值排序
sorted_idx = np.argsort(-np.abs(shap_values.values[0,:,1]))

for i in sorted_idx:
    current_value += shap_values.values[0][i][1]
    print(f"+ {feature_names[i]} ({shap_values.values[0][i][1]:+.4f}) → {current_value:.4f}")

# 可视化
shap.plots.waterfall(shap_values[0, :, 1])

# 添加阈值分析和业务解释
THRESHOLD = 0.5
final_prob = model.predict_proba(sample)[0][1]

print("\n=== 业务解释 ===")
print(f"最终违约概率: {final_prob:.2%}")
print(f"决策阈值: {THRESHOLD:.0%}")
print("主要风险驱动因素:")
for i in sorted_idx[:2]:  # 只显示前两大因素
    print(f"- {feature_names[i]}: 贡献值 {shap_values.values[0][i][1]:+.3f}")
    