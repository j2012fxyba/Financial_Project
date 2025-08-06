
import numpy as np
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm

# 随机生成数据（设定种子保证可复现）
np.random.seed(42)
n_samples = 100

# 自变量
debt_ratio = np.random.uniform(0.1, 0.8, n_samples)          # 资产负债率 (0.1~0.8)
revenue_growth = np.random.uniform(-0.1, 0.3, n_samples)      # 营收增长率 (-10%~30%)
management_ratio = np.random.uniform(0.05, 0.2, n_samples)    # 管理费用率 (5%~20%)

# 因变量：ROA = 0.5 - 0.3*资产负债率 + 0.4*营收增长率 - 0.2*管理费用率 + 噪声
roa = 0.5 - 0.3 * debt_ratio + 0.4 * revenue_growth - 0.2 * management_ratio + np.random.normal(0, 0.05, n_samples)

# 构建DataFrame
df = pd.DataFrame({
    'ROA': roa,
    'Debt_Ratio': debt_ratio,
    'Revenue_Growth': revenue_growth,
    'Management_Ratio': management_ratio
})

# 提取自变量并添加截距项
X = df[['Debt_Ratio', 'Revenue_Growth', 'Management_Ratio']]
X = sm.add_constant(X)  # 添加截距项

# 计算VIF
vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

print(vif_data)

# 定义因变量和自变量
y = df['ROA']
X = df[['Debt_Ratio', 'Revenue_Growth', 'Management_Ratio']]
X = sm.add_constant(X)  # 添加截距项

# 拟合模型
model = sm.OLS(y, X).fit()
print(model.summary())
