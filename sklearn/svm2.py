import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# 确保全局字体设置
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False   #负号处理


# 设置随机种子
np.random.seed(42)

# 生成数据：确保线性可分且原点附近有清晰分界
n_samples = 20
X = np.random.randn(n_samples, 2) * 1.5
y = np.where(X[:, 1] > -X[:, 0], 1, -1)  # 分类边界设为 y = -x

# 设置超平面参数（从原点出发，法向量指向右上方）
w = np.array([1, 1])  # 法向量方向
w = w / np.linalg.norm(w)  # 单位化
b = 0  # 超平面通过原点

# 计算边界线（从原点延伸）
x_plot = np.linspace(-3, 3, 100)
y_hyper = (-w[0] * x_plot - b) / w[1]  # 超平面 y = -x
y_margin_pos = (1 - w[0] * x_plot - b) / w[1]  # 上间隔边界
y_margin_neg = (-1 - w[0] * x_plot - b) / w[1]  # 下间隔边界

# 绘制图形
plt.figure(figsize=(10, 8))

# 1. 绘制数据点和支持向量
support_vectors = []
for i in range(n_samples):
    dist = abs(w[0]*X[i,0] + w[1]*X[i,1] + b)
    if dist <= 1.01:  # 支持向量
        support_vectors.append(i)
        plt.scatter(X[i,0], X[i,1], c='gold', s=200, marker='*', 
                   edgecolor='k', label='支持向量' if len(support_vectors)==1 else "")
    else:
        plt.scatter(X[i,0], X[i,1], c='skyblue' if y[i]==1 else 'lightcoral', s=80)

# 2. 绘制从原点出发的边界线
plt.plot(x_plot, y_hyper, 'k-', linewidth=3, label='超平面 $w·x + b = 0$')
plt.plot(x_plot, y_margin_pos, 'g--', label='$w·x + b = +1$')
plt.plot(x_plot, y_margin_neg, 'g--', label='$w·x + b = -1$')

# 3. 填充间隔区域（甬道）
plt.fill_between(x_plot, y_margin_neg, y_margin_pos, color='gray', alpha=0.1)

# 4. 强调原点与坐标轴
plt.axhline(0, color='black', linewidth=0.5, linestyle=':')
plt.axvline(0, color='black', linewidth=0.5, linestyle=':')
plt.scatter(0, 0, c='k', s=60, label='原点 (0,0)')

# 5. 标注法向量方向
plt.quiver(0, 0, w[0], w[1], angles='xy', scale_units='xy', scale=1,
           color='red', width=0.015, label='法向量 $w$')

# 6. 标注间隔宽度
arrow_x = 1.5  # 选择标注位置
arrow = FancyArrowPatch(
    (arrow_x, (-w[0]*arrow_x -b +1)/w[1]),
    (arrow_x, (-w[0]*arrow_x -b -1)/w[1]),
    arrowstyle='<->', color='red', mutation_scale=20
)
plt.gca().add_patch(arrow)
plt.text(arrow_x+0.1, (-w[0]*arrow_x -b)/w[1], 
         f'间隔宽度=2/‖w‖={2/np.linalg.norm(w):.2f}',
         color='red', va='center')

plt.axis('equal')
plt.xlim(-2.5, 2.5)
plt.ylim(-2.5, 2.5)
plt.xlabel('$x_1$')
plt.ylabel('$x_2$')
plt.title('从原点出发的SVM超平面与间隔', pad=20)
plt.legend(loc='upper right')
plt.grid(alpha=0.2)
plt.show()



