

import matplotlib.pyplot as plt
import numpy as np

# 定义两个点
A = np.array([1, 2])
B = np.array([4, 5])

# 计算曼哈顿距离
manhattan_distance = np.sum(np.abs(A - B))

# 绘制点和路径
plt.figure(figsize=(8, 6))
plt.scatter([A[0], B[0]], [A[1], B[1]], color='red', s=100, label='Points')
plt.plot([A[0], A[0]], [A[1], B[1]], 'g--', linewidth=2, label='Vertical Distance (|y2 - y1|)')
plt.plot([A[0], B[0]], [B[1], B[1]], 'b--', linewidth=2, label='Horizontal Distance (|x2 - x1|)')
plt.plot([A[0], B[0]], [A[1], B[1]], 'k-', alpha=0.3, label='Euclidean Distance')

# 标注距离
#欧氏距离（作为对比，曼哈顿距离是绿色和蓝色距离之和 3 + 3 = 6）。
plt.text((A[0] + B[0])/2, A[1], f'|x2 - x1| = {abs(B[0] - A[0])}', ha='center', va='bottom', color='blue')
plt.text(A[0], (A[1] + B[1])/2, f'|y2 - y1| = {abs(B[1] - A[1])}', ha='right', va='center', color='green')
plt.text((A[0] + B[0])/2, (A[1] + B[1])/2, 
         f'Manhattan Distance = {manhattan_distance}', 
         ha='center', va='center', bbox=dict(facecolor='white', alpha=0.8))

# 设置图形
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Manhattan Distance Visualization')
plt.grid(True)
plt.legend()
plt.axis('equal')
plt.show()