import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

# 模拟FRED数据（实际应用时可用fredapi获取真实数据）
def simulate_fred_data():
    dates = pd.date_range(start='1990-01-02', end=datetime.today(), freq='M')
    np.random.seed(42)
    
    # 模拟10年期零息债券收益率（均值5%，波动1%）
    y10 = 5 + np.random.normal(0, 1, len(dates)).cumsum()/100
    y10 = np.clip(y10, 2, 8)  # 限制在2%-8%范围内
    
    # 模拟2年期零息债券收益率（均值3%，波动0.8%）
    y2 = 3 + np.random.normal(0, 0.8, len(dates)).cumsum()/100
    y2 = np.clip(y2, 1, 6)
    
    # 创建DataFrame
    df = pd.DataFrame({
        'DATE': dates,
        '10Y Zero Yield': y10,
        '2Y Zero Yield': y2
    }).set_index('DATE')
    
    # 添加10-2利差
    df['10-2 Spread'] = df['10Y Zero Yield'] - df['2Y Zero Yield']
    
    return df

# 计算2年后生效的8年期远期利率
def calculate_forward_rate(df):
    df['8Y2Y Forward'] = 100 * (
        ((1 + df['10Y Zero Yield']/100)**10 / (1 + df['2Y Zero Yield']/100)**2)**(1/8) - 1
    )
    return df

# 主绘图函数
def plot_forward_rates(df):
    plt.figure(figsize=(14, 8))
    
    # 绘制原始收益率曲线
    plt.plot(df.index, df['10Y Zero Yield'], 'b-', label='10-Year Zero Yield', linewidth=2)
    plt.plot(df.index, df['2Y Zero Yield'], 'g-', label='2-Year Zero Yield', linewidth=2)
    
    # 绘制远期利率
    plt.plot(df.index, df['8Y2Y Forward'], 'r--', label='8Y2Y Forward Rate', linewidth=3)
    
    # 绘制10-2利差
    plt.plot(df.index, df['10-2 Spread'], 'm:', label='10-2 Yield Spread', linewidth=2)
    
    # 添加关键标注
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.title('2-Year vs 10-Year Zero Yields and 8Y2Y Forward Rate (1990-Present)', fontsize=14)
    plt.ylabel('Yield (%)', fontsize=12)
    plt.xlabel('Date', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # 添加公式说明
    plt.annotate('Forward Rate Formula:\n'
                 r'$100 \times \left(\left(\frac{(1+y_{10}/100)^{10}}{(1+y_2/100)^2}\right)^{1/8} - 1\right)$',
                 xy=(datetime(2000,1,1), 6), xytext=(datetime(1995,1,1), 7),
                 bbox=dict(boxstyle='round', fc='white', alpha=0.8),
                 fontsize=12)
    
    plt.tight_layout()
    plt.show()

# 执行流程
df = simulate_fred_data()
df = calculate_forward_rate(df)
plot_forward_rates(df)

# 显示最近5条数据
print("\nRecent Forward Rate Calculations:")
print(df[['10Y Zero Yield', '2Y Zero Yield', '8Y2Y Forward']].tail())
