import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import pandas as pd



data = pd.read_excel('D:\\tool\\CQF\\pachong\\AMZN.xlsx')
data['Date'] = pd.to_datetime(data['Date'])

# 计算技术指标
data['MA20'] = data['Close'].rolling(20).mean()
data['MA60'] = data['Close'].rolling(60).mean()


# 假设data已经包含必要的列：Date, Open, High, Low, Close, Volume, MA20, MA60
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# 创建图形和网格布局
fig = plt.figure(figsize=(12, 8))
gs = fig.add_gridspec(2, 1, height_ratios=[3, 1])
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])


# 绘制K线图（蜡烛图）
for idx, row in data.iterrows():
    color = 'green' if row['Close'] >= row['Open'] else 'red'
    x = mdates.date2num(idx)
    
    # 绘制上下影线
    ax1.plot([x, x], [row['Low'], row['High']], color=color, linewidth=1)
    
    # 绘制蜡烛实体
    rect_width = 0.8
    rect = Rectangle(
        (x - rect_width/2, min(row['Open'], row['Close'])),
        rect_width,
        abs(row['Close'] - row['Open']),
        facecolor=color,
        edgecolor=color
    )
    ax1.add_patch(rect)

# 确保全局字体设置
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False   #负号处理

# 绘制均线（在同一个ax1上）
ax1.plot(data.index, data['Close'], label='收盘价', color='Purple', linewidth=1)
ax1.plot(data.index, data['MA20'], label='20日均线', color='blue', linestyle='--', alpha=0.8)
ax1.plot(data.index, data['MA60'], label='60日均线', color='orange', linestyle='--', alpha=0.8)

# 设置K线图坐标轴
ax1.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1,4,7,10]))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax1.xaxis.set_minor_locator(mdates.MonthLocator())
ax1.set_title('AMZN K线图与均线组合', fontsize=12)
ax1.set_ylabel('价格 (USD)', fontsize=10)
ax1.legend(loc='upper left')
ax1.grid(True, linestyle=':', alpha=0.5)

# 绘制成交量图
ax2.bar(data.index, data['Volume']/1e6, 
        color=['green' if close>open else 'red' 
               for close,open in zip(data['Close'],data['Open'])],
        width=0.8, label='成交量')
ax2.set_ylabel('成交量(百万)', fontsize=10)
ax2.grid(True, linestyle=':', alpha=0.5)

# 调整布局
plt.setp(ax1.get_xticklabels(), rotation=45)
plt.tight_layout()
plt.show()