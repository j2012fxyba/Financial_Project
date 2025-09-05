

import numpy as np

A = np.array([[1, 2, 3],
              [4, 5, 6]])

B = np.array([[5, 6, 7]])
print('打印出B的转置')
print(B.T)
'''
[5]    第一行1*5+2*6+3*7=32
[6]    第二行 4*5+5*6+6*7=92 
[7]     输出A@B.T =[[38,[92]]
'''
B_T = B.T  # 或者 B.T    1*5 +2*6 +3*7=38

result = A @ B_T
print(result)


'''行列转换'''

# 机器学习中常见：样本按行排列 vs 按列排列
X_rows = np.array([[1, 2, 3],    # 每个样本一行
                   [4, 5, 6]])   # 2个样本，3个特征

X_cols = X_rows.T                # 转置后：每个特征一列
# [[1, 4],
#  [2, 5], 
#  [3, 6]]  3个特征，2个样本
print(X_cols)

'''内积运算'''

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# 内积的两种等价计算：
dot1 = np.dot(a, b)           # 直接内积
dot2 = a @ b.T                # 通过转置用矩阵乘法
# 都是：1×4 + 2×5 + 3×6 = 32
print(dot1, dot2)


'''协方差矩阵计算'''

# 协方差矩阵：衡量特征之间的线性相关程度

# 计算特征的协方差矩阵
X = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])     # 3个样本，3个特征

X_centered = X - X.mean(axis=0)  # 中心化
cov_matrix = (X_centered.T @ X_centered) / (X.shape[0] - 1)
print(cov_matrix)


'''线性方程求解'''

# 机器学习中常见：最小二乘法
# 求解线性方程组：A×X = B
A = np.array([[1, 2, 3], [4, 5, 6]])
B = np.array([7, 8])

# 直接求解：X = A⁻¹×B
# X = np.linalg.inv(A) @ B
# print(X)  # [ 1. -1.  1.]
# # 但如果 A 不可逆，则无法直接求解
# # 可以使用 np.linalg.lstsq(A, B) 来求解最小二乘解
# X = np.linalg.lstsq(A, B, rcond=None)[0]
# print(X)  # [ 1. -1.  1.]
# rcond=None 表示不考虑数值稳定性
# 如果 A 可逆，则结果与直接求解相同
# 如果 A 不可逆，则结果是最小二乘解
# np.linalg.lstsq 返回一个元组，第一个元素是最小二乘解


'''图像处理'''

# 图像本质是矩阵，转置相当于90度旋转  K=1时 可以省略
image = np.array([[1,3,2],
                  [-3,2,1],
                  [4,1,2]])

print('源矩阵\n',image)
print('左右翻转\n',np.fliplr(image))  # 左右翻转  
print('上下翻转\n',np.flipud(image) ) # 上下翻转  

print('顺时针旋转 90°\n',np.fliplr(image.T))  
print('逆时针旋转90°\n',np.flipud(image.T))  





import numpy as np
#在线性代数中，我们通常用大写字母表示矩阵，小写字母表示向量/标量
#利用逆矩阵可解方程组，标准形式是Ax=b ,x 是未知向量  b是常量 A是矩阵系数
# 计算X=np.linalg.inv(A)*b



A=np.array([[1,3,6],[2,5,8],[3,9,11]])
print(A)
#如果A可逆,则 Z=A⁻¹ 
Z=np.linalg.inv(A)

C=A*Z 
print(C)

#对于方程组 Ax=b,其中A是一个矩阵，b是一个向量，x是一个未知向量，
# 我们可以使用矩阵的逆来求解X。具体来说，X = a^-1 * b，其中a^-1是矩阵a的逆矩阵。

AX=b
A=np.array([[1,3,6],[2,5,8],[3,9,11]])
b = np.array([[3], [6], [7]])  # 方法1
print('A的逆矩阵是\n')
Z=np.linalg.inv(A)
print(Z)
x=Z*b
print("解向量 x（满足 A x = b）:\n", x)


A=np.array([[1,3,6],
            [2,5,8],
            [3,6,8]
            ])
#计算A的特征值
eigenvalues, eigenvectors = np.linalg.eig(A)
#计算A的特征向量
print('A的特征向量是\n',eigenvectors)
#计算A的特征值
print('A的特征值是\n',eigenvalues)

# 验证：对于每个特征值λ和对应的特征向量v，应该满足 A·v = λ·v
for i in range(len(eigenvalues)):
    λ = eigenvalues[i]
    v = eigenvectors[:, i]  # 第i列是第i个特征向量
    print(f"验证 A·v{i} = λ{i}·v{i}:")
    print("A·v =", A @ v)
    print("λ·v =", λ * v)
    print("误差:", np.linalg.norm(A @ v - λ * v))
    print()


import numpy as np

# 解方程组：
# 2x + y = 5
# x - y = 1
A = np.array([[2, 1],
              [1, -1]])
b = np.array([5, 1])

# 使用逆矩阵求解
A_inv = np.linalg.inv(A)
x = A_inv @ b  # x = [2, 1]
print("解:", x)  # 输出: [2. 1.]