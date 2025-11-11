import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 数据（专注度和面部变化次数）
x = np.array([0, 8, 2, 7, 1, 6, 2, 0, 2, 2, 3, 1, 2, 7, 0, 2, 1, 0, 27, 2, 0, 11, 2, 11, 4, 12, 1, 0, 29, 18, 8, 12, 3, 0])
y = np.array([0.82962963, 1.185185185, 0.296296296, 0.088888889, 0.562962963, 0.8, 0.651851852, 0.059259259, 0.148148148, 0.77037037, 0.977777778, -0.088888889, 0.82962963, 0.474074074, 1.214814815, 0.533333333, 0.622222222, 1.037037037, 1.096296296, -0.237037037, 0.02962963, 0.207407407, 0.474074074, 0.592592593, 1.185185185, -0.385185185, 0.237037037, 0.385185185, 1.244444444, 1.007407407, 0.859259259, 0.592592593, 0.385185185, 0.711111111])

# 定义二次函数拟合的目标函数
def quadratic_objective(params):
    a, b, c = params  # a为二次项系数，b为一次项系数，c为常数项
    y_pred = a * x**2 + b * x + c
    return np.sum((y_pred - y) ** 2)  # 均方误差

# 初始猜测值（基于可能的倒U型关系）
initial_guess = [-0.01, 0.1, 1]  # 初始参数：[a, b, c]

# 使用优化方法求解
result = minimize(quadratic_objective, initial_guess)

# 提取最优参数
a_opt, b_opt, c_opt = result.x

# 计算拟合优度（R²）
y_pred = a_opt * x**2 + b_opt * x + c_opt
r2 = 1 - np.sum((y - y_pred) ** 2) / np.sum((y - np.mean(y)) ** 2)

# 找到抛物线的顶点（极值点）
vertex_x = -b_opt / (2 * a_opt)  # 顶点的x坐标
vertex_y = a_opt * vertex_x**2 + b_opt * vertex_x + c_opt  # 顶点的y坐标

# 打印结果
print(f"最优二次函数：专注度 = {a_opt:.6f} × 次数² + {b_opt:.6f} × 次数 + {c_opt:.6f}")
print(f"抛物线顶点：次数 = {vertex_x:.2f}，专注度 = {vertex_y:.4f}")
print(f"R² = {r2:.4f}")

# 可视化结果
plt.figure(figsize=(12, 8))
plt.scatter(x, y, color='blue', label='实际数据')

# 绘制二次函数曲线
x_plot = np.linspace(min(x)-2, max(x)+2, 500)
y_plot = a_opt * x_plot**2 + b_opt * x_plot + c_opt
plt.plot(x_plot, y_plot, color='red', linestyle='-',
         label=f'拟合二次函数: y = {a_opt:.6f}x² + {b_opt:.6f}x + {c_opt:.6f}')

# 标记顶点
plt.scatter([vertex_x], [vertex_y], color='green', s=100, marker='*',
            label=f'顶点: ({vertex_x:.2f}, {vertex_y:.4f})')

plt.xlabel('姿态变化次数')
plt.ylabel('专注度')
plt.title('二次函数拟合结果：专注度 vs 姿态变化次数')
plt.legend()
plt.grid(True)
plt.show()