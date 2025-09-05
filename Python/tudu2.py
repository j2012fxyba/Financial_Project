import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch


# Set up the figure
plt.figure(figsize=(10, 6))
plt.title("Bond Price-Yield Relationship with Convexity", fontsize=14)
plt.xlabel("Yield to Maturity (YTM)", fontsize=12)
plt.ylabel("Bond Price", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

# Define yield range
y = np.linspace(0.01, 0.15, 100)

# Bond price function with convexity
def bond_price(y, convexity, macaulay_duration=10, initial_y=0.05, initial_p=100):
    # 计算修正久期（更准确）
    modified_duration = macaulay_duration / (1 + initial_y)

    # Linear approximation (duration only)
    linear_p = initial_p * (1 - modified_duration*(y - initial_y))

    # With convexity adjustment
    convex_p = linear_p + 0.5 * convexity * initial_p * (y - initial_y)**2

    return linear_p, convex_p

# Calculate prices for different convexities
linear_p, convex_p_low = bond_price(y, convexity=50)  # Less convex
_, convex_p_high = bond_price(y, convexity=150)       # More convex

# Plot the curves
plt.plot(y, linear_p, 'b--', label='Linear approximation (Duration only)')
plt.plot(y, convex_p_low, 'g-', label='Less convex bond (Convexity=50)')
plt.plot(y, convex_p_high, 'r-', label='More convex bond (Convexity=150)')

# Mark the initial point
initial_y = 0.05
plt.scatter([initial_y], [100], color='black', zorder=5)
plt.text(initial_y, 102, 'Initial Price (YTM=5%)', ha='center')

# Add tangent line annotation
plt.annotate('Tangent Line (Duration)', xy=(0.08, 70), xytext=(0.1, 80),
             arrowprops=dict(arrowstyle='->'), fontsize=10)

# Highlight convexity differences
plt.fill_between(y, convex_p_low, convex_p_high, where=(y >= initial_y), 
                 color='red', alpha=0.1, label='Convexity advantage')
plt.fill_between(y, convex_p_low, convex_p_high, where=(y <= initial_y), 
                 color='green', alpha=0.1)

# Add arrows showing price difference at higher yields
arrow_y = 0.12
price_diff = bond_price(arrow_y, 150)[1] - bond_price(arrow_y, 50)[1]
plt.annotate('', xy=(arrow_y, bond_price(arrow_y, 50)[1]), 
             xytext=(arrow_y, bond_price(arrow_y, 150)[1]),
             arrowprops=dict(arrowstyle='<->', color='purple'))
plt.text(arrow_y, (bond_price(arrow_y, 50)[1] + bond_price(arrow_y, 150)[1])/2,
         f'Price difference:\n{price_diff:.1f}', ha='left', va='center')

plt.legend(loc='upper right')
plt.ylim(40, 140)
plt.tight_layout()
plt.show()





y = np.linspace(0.01, 0.15, 100)
# 案例1：短期公司债
convex_short = 30
_, price_short = bond_price(y, convexity=convex_short)
print(price_short)
# 案例2：长期国债
convex_long = 120
_, price_long = bond_price(y, convexity=convex_long)
print(price_long)

def calculate_convexity(cashflows, ytm):
    # 基于现金流和到期收益率计算凸性
    t = np.arange(1, len(cashflows)+1)
    pv = cashflows / (1 + ytm)**t
    convexity = np.sum(t * (t + 1) * pv) / (np.sum(pv) * (1 + ytm)**2)
    return convexity

# 示例：5年期债券，年息5%
cashflows = np.array([5, 5, 5, 5, 105])  # 利息+本金
ytm = 0.05
real_convexity = calculate_convexity(cashflows, ytm)  # 约24.5








# 债券参数（可自由调整）
face_value = 1000       # 面值
coupon_rates = [0.04, 0.06]  # 折价债券4% vs 溢价债券6%
y0 = 0.05               # 当前收益率5%
years = 10              # 延长期限至10年以增强凸度效果


def calculate_metrics(y, face_value, coupon_rate, years):
    P0 = bond_price(y, face_value, coupon_rate, years)
    delta_y = 0.0001  # 使用相同的微小变动值
    
    # 修正久期
    P_plus = float(bond_price(y + delta_y, face_value, coupon_rate, years))
    P_minus = float(bond_price(y - delta_y, face_value, coupon_rate, years))
    md = (P_minus - P_plus) / (2 * P0 * delta_y)
    
    # 凸度（使用更大的变动值计算）
    delta_y_conv = 0.01  # 凸度需要更大的变动值
    P_plus_conv = float(bond_price(y + delta_y_conv, face_value, coupon_rate, years))
    P_minus_conv = float(bond_price(y - delta_y_conv, face_value, coupon_rate, years))
    conv = (P_plus_conv + P_minus_conv - 2 * P0) / (P0 * delta_y_conv**2)
    
    return P0, md, conv 





# 债券定价函数
def bond_price(y, face_value, coupon_rate, years):
    """计算债券价格（确保返回float）"""
    coupon_payment = face_value * coupon_rate
    price = sum(coupon_payment / (1 + y)**t for t in range(1, years + 1))
    price += face_value / (1 + y)**years
    return float(price)

# 指标计算函数
def calculate_metrics(y, face_value, coupon_rate, years):
    """计算P0、修正久期和凸度"""
    P0 = bond_price(y, face_value, coupon_rate, years)
    
    # 修正久期（使用微小变动）
    delta_y = 0.0001
    P_plus = bond_price(y + delta_y, face_value, coupon_rate, years)
    P_minus = bond_price(y - delta_y, face_value, coupon_rate, years)
    md = (P_minus - P_plus) / (2 * P0 * delta_y)
    
    # 凸度（使用较大变动）
    delta_y_conv = 0.01
    P_plus_conv = bond_price(y + delta_y_conv, face_value, coupon_rate, years)
    P_minus_conv = bond_price(y - delta_y_conv, face_value, coupon_rate, years)
    conv = (P_plus_conv + P_minus_conv - 2 * P0) / (P0 * delta_y_conv**2)
    
    return P0, md, conv

# 主程序
face_value = 1000
coupon_rates = [0.04, 0.06]  # 折价债券/溢价债券
y0 = 0.05
years = 10

plt.figure(figsize=(14, 8))

for i, coupon_rate in enumerate(coupon_rates):
    # 生成收益率曲线
    y_values = np.linspace(0.01, 0.15, 100)
    prices = [bond_price(y, face_value, coupon_rate, years) for y in y_values]
    
    # 必须先计算指标再使用！
    P0, md, conv = calculate_metrics(y0, face_value, coupon_rate, years)
    linear_approx = P0 * (1 - md * (y_values - y0))
    convexity_approx = linear_approx + 0.5 * conv * (y_values - y0)**2
    
    # 绘图
    color = ['blue', 'orange'][i]
    ls = ['-', '--'][i]
    plt.plot(y_values, prices, color=color, label=f'Coupon {coupon_rate*100}%', linestyle=ls)
    plt.plot(y_values, linear_approx, color=color, linestyle=':', label=f'Duration approx (MD={md:.2f})')
    plt.plot(y_values, convexity_approx, color=color, linestyle='-.', label=f'With convexity (C={conv:.1f})')

# 图表装饰
plt.axhline(face_value, color='gray', linestyle='--')
plt.title("Bond Price-Yield Relationship with Convexity Effect")
plt.xlabel("Yield")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.show()