import numpy as np
import sklearn.feature_selection
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm


# 原始数据  
#回归估计 α   alpha_adj 
# 特征参数：通胀缺口2.0%、1.8% 失业率6.5、6.3 信贷增长4.2 3.9
#X_raw = np.array([[2.0, 6.5, 4.2], [1.8, 6.3, 3.9]])  # (2, 3)
# alpha_adj = np.array([3.14, 2.98])  # 长度=2 给定了2个 调整α的值  
# 假设的因变量（需与样本数匹配） 维度一致性：确保 X 的样本数（行数）与 y（如 alpha_adj）长度一致。

# # 标准化整个矩阵
scaler = StandardScaler()

import sklearn
sklearn.feature_selection  #特征选择
sklearn.config_context 

'''原来的样本量太小了，报错，模型至少需要 8个样本 '''
'''50个样本，4个特征，包括1个截距项'''
np.random.seed(42)
n_samples = 50  # 至少8个
X_raw = np.random.randn(n_samples, 3) * [0.2, 0.2, 0.2] + [2.0, 6.5, 4.2]  # 围绕原均值偏移
X_scaled = scaler.fit_transform(X_raw) 
print(X_scaled)
# 添加截距项（必需） 线性回归模型通常包含一个截距项
X = sm.add_constant(X_scaled)
#生成因变量alpha_adj   # 添加正态分布随机噪声，均值为0 标准差为0.1
alpha_adj = 1.4 * np.exp(0.35 * X_raw[:, 0]) + np.random.normal(0, 0.1, n_samples)  
print(alpha_adj)
# 拟合OLS模型
model = sm.OLS(alpha_adj, X).fit()  # 输入形状 (2,4) 和 (2,)
print(model.summary())


# 预测新数据
new_data = np.array([[2.1, 6.4, 4.0]])
new_data_scaled = scaler.transform(new_data)  # 使用原scaler
new_data_scaled = np.ascontiguousarray(new_data_scaled, dtype=np.float64)  # 确保数据类型
new_X = sm.add_constant(new_data_scaled, has_constant='add')  # 形状 (1,4)
print(new_X.shape)
print("预测:", model.predict(new_X))
# 添加截距项
#原本这行代码没有生效new_X = sm.add_constant(new_data_scaled)



