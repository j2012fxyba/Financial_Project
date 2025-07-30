import matplotlib.pyplot as plt
import numpy as np


# 确保全局字体设置
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False   #负号处理

# 设置参数
P_D = 0.1  # 缺陷品基础概率
P_G = 1 - P_D  # 良品概率
alpha = 0.95  # 真阳性率（缺陷品被正确检测）
beta = 0.05    # 假阳性率（良品被误检）

# 计算联合概率
P_Tp_D = alpha * P_D  # 缺陷品且被检出
P_Tp_G = beta * P_G   # 良品但被误检

# 全概率
P_Tp = P_Tp_D + P_Tp_G

# 创建画布
fig, ax = plt.subplots(figsize=(10, 10))

# 外层圆（全概率）
size = 0.3
outer_labels = [f'检测为缺陷\n总概率: {P_Tp:.1%}', 
                f'检测为良品\n{1-P_Tp:.1%}']
outer_colors = ['#ff9999','#66b3ff']
ax.pie([P_Tp, 1-P_Tp], radius=1, colors=outer_colors,
       labels=outer_labels, labeldistance=0.8,
       wedgeprops=dict(width=size, edgecolor='w'))

# 中层圆（联合概率）
mid_labels = [
    f'缺陷品且被检出\n{P_Tp_D:.1%}\n(条件概率 α={alpha})',
    f'良品但被误检\n{P_Tp_G:.1%}\n(条件概率 β={beta})',
    ''
]
mid_colors = ['#ff6666', '#ffcc99', '#66b3ff']
ax.pie([P_Tp_D, P_Tp_G, 1-P_Tp], radius=1-size, colors=mid_colors,
       labels=mid_labels, labeldistance=0.7,
       wedgeprops=dict(width=size, edgecolor='w'))

# 内层圆（基础概率）
inner_labels = [
    f'实际缺陷品\n{P_D:.1%}',
    f'实际良品\n{P_G:.1%}'
]
inner_colors = ['#ff3333', '#99ff99']
ax.pie([P_D, P_G], radius=1-2*size, colors=inner_colors,
       labels=inner_labels, labeldistance=0.4,
       wedgeprops=dict(width=size, edgecolor='w'))

# 添加标题和说明
plt.title('概率关系分解图\n'
          '条件概率 → 联合概率 → 全概率', pad=20, fontsize=14)
plt.text(0, -1.5, 
         f"全概率公式: P(T⁺) = α·P(D) + β·P(G) = {alpha}×{P_D} + {beta}×{P_G} = {P_Tp:.3f}",
         ha='center', fontsize=12)

plt.tight_layout()
plt.show()





# 设定参数
P_B = 0.4      # 事件B的概率
P_A_given_B = 0.7  # 条件概率 P(A|B)

# 计算联合概率 P(A∩B) = P(A|B) * P(B)
P_A_and_B = P_A_given_B * P_B

# 绘制饼图
labels = [
    f'P(A∩B) = {P_A_and_B:.2f}',  # 联合概率
    f'P(B但非A) = {P_B - P_A_and_B:.2f}',  # B发生但A不发生
    '其他事件 (非B)'  # 其他情况
]
sizes = [P_A_and_B, P_B - P_A_and_B, 1 - P_B]
colors = ['#ff9999', '#66b3ff', '#99ff99']
explode = (0.1, 0, 0)  # 突出显示联合概率部分

plt.figure(figsize=(8, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', startangle=90, shadow=True)
plt.title('联合概率 vs. 条件概率\n'
          f'P(A|B) = {P_A_given_B:.1f} (条件概率)', pad=20)
plt.legend([f'P(B) = {P_B:.2f}'], loc='upper right')
plt.show()





# 创建图形
fig, ax = plt.subplots(figsize=(8, 6))

# 绘制两个圆表示集合A和B
circle_A = plt.Circle((0.4, 0.5), 0.3, color='red', alpha=0.3, label='A')
circle_B = plt.Circle((0.6, 0.5), 0.3, color='blue', alpha=0.3, label='B')
ax.add_patch(circle_A)
ax.add_patch(circle_B)

# 标注各部分概率
P_A = 0.5      # P(A)
P_B = 0.4      # P(B)
P_A_and_B = 0.2  # P(A∩B)

# 手动计算各区域概率
P_A_only = P_A - P_A_and_B  # 仅A发生
P_B_only = P_B - P_A_and_B  # 仅B发生
P_neither = 1 - (P_A + P_B - P_A_and_B)  # 两者都不发生
labels = [
    f'P(A∩B) = {P_A_and_B:.2f}',  # 联合概率
    f'P_A = {P_A_only:.2f}'
    f'P_B = {P_B_only:.2f}',  # B发生但A不发生
    '其他事件 (非B)'  # 其他情况
]
# 标注概率值
ax.text(0.25, 0.5, f'P(A only)\n{P_A_only:.2f}', ha='center', va='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
ax.text(0.75, 0.5, f'P(B only)\n{P_B_only:.2f}', ha='center', va='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
ax.text(0.5, 0.5, f'P(A∩B)\n{P_A_and_B:.2f}', ha='center', va='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
ax.text(0.5, 0.1, f'两者都不发生\n{P_neither:.2f}', ha='center', va='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

# 添加图示（显示A和B的总概率）
legend_labels = [f'P(A)={P_A}', f'P(B)={P_B}']
plt.legend([circle_A, circle_B],legend_labels,loc='upper right')


# 设置坐标轴和标题
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.axis('off')  # 隐藏坐标轴
plt.title("Joint Probability P(A∩B) Visualization", fontsize=12, pad=20)
plt.show()



# 设置参数
P_D = 0.05     # 缺陷品基础概率
P_G = 1 - P_D  # 良品概率
alpha = 0.9    # 真阳性率（缺陷品被检出概率）
beta = 0.03     # 假阳性率（良品被误检概率）

# 计算全概率
P_Tp_D = alpha * P_D  #0.05*0.9=0.045  # 缺陷且被检出
P_Tp_G = beta * P_G  #0.95*0.03   # 良品但被误检
P_Tp = P_Tp_D + P_Tp_G  # 全概率（被检出总概率）
print(P_Tp_D)
print(P_Tp_G)

# 创建画布
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制分层条形图
categories = ['实际分布', '检测结果']
width = 0.35
x = np.arange(len(categories))

# 实际分布层  f'(P(A)={P_A})'
ax.bar(x - width/2, [P_D, 0], width, label=f'缺陷品P(D)={P_D}', color="#99ff9e")
ax.bar(x - width/2, [P_G, 0], width, bottom=[P_D, 0], label=f'良品P(G)={P_G}', color="#ff6666")

# 检测结果层（全概率分解）
ax.bar(x + width/2, [0, P_Tp_D], width, color="#cd19ac", 
       #真阳性=0.05*0.9=0.045
       
       label=f'真阳性(αP(D)={alpha}×{P_D}={P_Tp_D:.4f})')
        #假阳性 0.03*0.95=0.285
ax.bar(x + width/2, [0, P_Tp_G], width, bottom=[0, P_Tp_D], color="#ff99a7",
       label=f'假阳性(βP(G)={beta}×{P_G}={P_Tp_G:.4f})')

# 标注全概率公式
formula_text = f'全概率公式:\nP(Total) = αP(D) + βP(G)\n= {alpha}×{P_D} + {beta}×{P_G}\n= {P_Tp:.4f}'
ax.text(1.5, 0.5, formula_text, ha='left', va='center', fontsize=12,
        bbox=dict(facecolor='white', alpha=0.8))

# 添加标注线
ax.annotate('', xy=(1, P_Tp), xytext=(0.2, P_D),
            arrowprops=dict(arrowstyle='->', linestyle='dashed'))
ax.annotate('', xy=(1, P_Tp_G), xytext=(0.2, P_G),
            arrowprops=dict(arrowstyle='->', linestyle='dashed'))

# 设置图形属性
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.set_ylabel('概率')
ax.set_title('全概率分解图（质量检测场景）', pad=20)
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()





# 设置参数
scenarios = ['S1', 'S2', 'S3', 'S4', 'S5']  # 不同情景
P_S = np.array([0.2, 0.3, 0.25, 0.15, 0.1])  # 各情景发生概率
P_A_given_S = np.array([0.8, 0.6, 0.4, 0.2, 0.1])  # 各情景下A发生的条件概率

# 计算联合概率
P_A_and_S = P_S * P_A_given_S
P_A_total = np.sum(P_A_and_S)  # 全概率

# 创建画布
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制各情景下的概率（堆叠直方图）
base_bars = ax.bar(scenarios, P_S, width=0.6, 
                  color='lightblue', edgecolor='grey',
                  label='情景概率 P(S)')

# 在各情景柱上叠加A发生的概率（部分填充）
overlay_bars = []
for i, (s, p_s, p_a_given_s) in enumerate(zip(scenarios, P_S, P_A_given_S)):
    bar = ax.bar(s, p_s*p_a_given_s, width=0.6, 
                color='salmon', edgecolor='red', alpha=0.8,
                label='联合概率 P(A∩S)' if i == 0 else "")
    overlay_bars.append(bar)

# 添加累计全概率柱（最右侧）
total_bar = ax.bar('Total', P_A_total, width=0.6, 
                  color='darkred', edgecolor='black',
                  label=f'全概率 P(A)={P_A_total:.2f}')

# 添加标注
for i, s in enumerate(scenarios):
    ax.text(i, P_S[i] + 0.02, f'P(S{i+1})={P_S[i]:.2f}', 
           ha='center', va='bottom', fontsize=9)
    ax.text(i, P_A_and_S[i]/2, f'P(A|S{i+1})={P_A_given_S[i]:.2f}', 
           ha='center', va='center', color='white', weight='bold', fontsize=9)

ax.text(len(scenarios), P_A_total/2, f'Σ={P_A_total:.2f}', 
       ha='center', va='center', color='white', weight='bold', fontsize=10)

# 美化图形
ax.set_ylim(0, max(P_S)*1.2)
ax.set_title('全概率分解可视化\n$P(A) = \sum P(A|S_i)P(S_i)$', pad=20, fontsize=12)
ax.set_ylabel('概率值', fontsize=10)
ax.tick_params(axis='both', which='major', labelsize=9)

# 将图例移动到左上角并优化显示
handles = [base_bars, overlay_bars[0], total_bar]
labels = ['情景概率 P(S)', '联合概率 P(A∩S)', f'全概率 P(A)={P_A_total:.2f}']
ax.legend(handles, labels, loc='upper left', 
         bbox_to_anchor=(0.02, 0.98), framealpha=1)

ax.grid(axis='y', linestyle=':', alpha=0.5)

plt.tight_layout()
plt.show()



import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# 设置参数
scenarios = ['生产\n线A', '生产\n线B', '外包\n商C', '实验\n批次D']  # 带换行的情景名称
P_S = np.array([0.35, 0.4, 0.2, 0.05])  # 各情景发生概率
P_A_given_S = np.array([0.02, 0.08, 0.15, 0.3])  # 各情景下的缺陷率

# 计算概率
P_A_and_S = P_S * P_A_given_S  # 联合概率
P_A_total = np.sum(P_A_and_S)  # 全概率
P_S_cumsum = np.cumsum(P_S)  # 累积概率

# 创建专业级图表
plt.style.use('seaborn-v0_8-pastel')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), 
                          gridspec_kw={'height_ratios': [3, 1]})

# ========== 主图：概率分解 ==========
# 绘制基础概率（透明底色）
base_bars = ax1.bar(scenarios, P_A_given_S, width=0.7,
                   color='lightgray', edgecolor='grey', alpha=0.3,
                   label='来源分布 P(S)')

    
# 绘制联合概率（彩色叠加）
colors = plt.cm.OrRd(np.linspace(0.4, 0.8, len(scenarios)))
for i, (s, h) in enumerate(zip(scenarios, P_A_and_S)):
    print(s, h)
    ax1.bar(s, h, width=0.7, color=colors[i], edgecolor='white',
            label=f'P(缺陷|{s.strip()})={P_A_given_S[i]:.0%}')


# 添加全概率线
ax1.axhline(P_A_total, color='darkred', linestyle='--', 
           label=f'总缺陷率: {P_A_total:.2%}')
ax1.annotate(f'{P_A_total:.2%}', xy=(3.5, P_A_total), 
            xytext=(5,5), textcoords='offset points',
            color='darkred', weight='bold')

# ========== 底部：累积概率 ==========
ax2.bar(scenarios, P_S, width=0.7, color='lightblue', 
       edgecolor='white', label='来源占比')
ax2.plot(scenarios, P_S_cumsum, 'o-', color='navy', 
        label='累积分布')
ax2.axhline(1.0, color='gray', linestyle=':')

# 在每个柱子上方标注 P(S)=x.xx
for bar, prob in zip(base_bars, P_S):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width() / 2, height + 0.01,  # x, y 坐标
            f'P(S)={prob:.2f}',  # 文本内容，保留2位小数
            ha='center', va='bottom', fontsize=10)  # 水平居中，垂直底部对齐

# ========== 高级美化 ==========
# 主图设置
ax1.set_ylim(0, max(P_S)*1.3)
ax1.set_title('产品质量缺陷全概率分析', pad=20, fontsize=14, weight='bold')
ax1.set_ylabel('概率分布', labelpad=10)
ax1.grid(axis='y', linestyle=':', alpha=0.7)

# 底部图设置
ax2.set_ylim(0, 1.1)
ax2.set_ylabel('累积概率', labelpad=10)
ax2.grid(axis='y', linestyle=':', alpha=0.5)

# 统一美化
for ax in (ax1, ax2):
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(axis='both', which='major', labelsize=9)

# 专业图例设计
legend_elements = [
    Patch(facecolor='lightgray', edgecolor='grey', label=r'$P(S)$（情景缺陷率）'),

    *[Patch(facecolor=colors[i], #label=f'{scenarios[i].strip()}: {P_A_given_S[i]:.0%}') 
      label=f'{scenarios[i].strip()}: {P_A_given_S[i]:.0%}')
      for i in range(len(scenarios))],
    plt.Line2D([0], [0], color='darkred', linestyle='--', 
              #label=f'总缺陷率 {P_A_total:.2%}'
              label=fr'P(S)_total={P_A_total:.4f}')  # 全概率公式)
]
ax1.legend(handles=legend_elements, loc='upper right', 
          bbox_to_anchor=(1, 1), frameon=True, framealpha=1)

plt.tight_layout(pad=2)
plt.show()
