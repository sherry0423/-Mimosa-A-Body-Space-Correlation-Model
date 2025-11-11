import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 数据
x = np.array([4.5, 4, 7, 6.5, 4, 0, 2])
y = np.array([1, 0.260740741, 0, 0.677248677, 0.637037037, 0.835555556, 0.548148148])

# 定义带约束的线性回归目标函数
def objective(params):
    a, b = params  # a为斜率，b为截距
    y_pred = a * x + b
    return np.sum((y_pred - y) ** 2)  # 均方误差

# 约束条件：斜率必须为负
constraints = {'type': 'ineq', 'fun': lambda params: -params[0]}  # -a > 0 等价于 a < 0

# 初始猜测值
initial_guess = [-0.1, 1]  # 初始斜率为负，截距为正

# 使用优化方法求解
result = minimize(objective, initial_guess, constraints=constraints)

# 提取最优参数
a_opt, b_opt = result.x

# 计算拟合优度（R²）
y_pred = a_opt * x + b_opt
r2 = 1 - np.sum((y - y_pred) ** 2) / np.sum((y - np.mean(y)) ** 2)

# 打印结果
print(f"最优线性函数：专注度 = {b_opt:.4f} - {abs(a_opt):.4f} × 变化次数")
print(f"斜率 a = {a_opt:.4f}（约束为负）")
print(f"截距 b = {b_opt:.4f}")
print(f"R² = {r2:.4f}")

# 可视化结果
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='blue', label='实际数据')
plt.plot(x, y_pred, color='red', linestyle='--',
         label=f'拟合直线: y = {b_opt:.4f} - {abs(a_opt):.4f}x')
plt.xlabel('平均变化次数')
plt.ylabel('专注度')
plt.title('带约束的线性回归拟合结果')
plt.legend()
plt.grid(True)
plt.show()