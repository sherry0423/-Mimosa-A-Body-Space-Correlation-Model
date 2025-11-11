import numpy as np
from scipy.interpolate import CubicSpline
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

# 设置中文显示
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# 原始数据
O = np.array([0, 12.5, 25, 37.5, 50, 62.5, 75, 87.5, 100])
S = np.array([55.55556, 100, 90.37037, 26.074074, 0, 67.7249, 63.7037, 83.55556, 54.81481])


def polynomial_fit(x, y, degree):
    """
    多项式拟合函数，返回拟合系数、R²和RMSE
    """
    coeffs = np.polyfit(x, y, degree)
    p = np.poly1d(coeffs)
    y_pred = p(x)
    r2 = r2_score(y, y_pred)
    rmse = np.sqrt(np.mean((y - y_pred) ** 2))
    return coeffs, r2, rmse, p


def cubic_spline_fit(x, y):
    """
    三次样条插值拟合函数，返回插值对象、R²和RMSE
    """
    cs = CubicSpline(x, y)
    y_pred = cs(x)
    r2 = r2_score(y, y_pred)
    rmse = np.sqrt(np.mean((y - y_pred) ** 2))
    return cs, r2, rmse


def print_polynomial(coeffs, degree):
    """
    格式化输出多项式表达式
    """
    terms = []
    for i, c in enumerate(coeffs):
        power = degree - i
        if power == 0:
            terms.append(f"{c:.6f}")
        elif power == 1:
            terms.append(f"{c:.6f}O")
        else:
            terms.append(f"{c:.6f}O^{power}")
    return " + ".join(terms)


def main():
    # 执行多项式拟合（2-5次）
    print("=" * 50)
    print("多项式拟合结果：")
    print("=" * 50)

    for degree in range(2, 6):
        coeffs, r2, rmse, p = polynomial_fit(O, S, degree)
        print(f"{degree}次多项式:")
        print(f"  拟合公式: S(O) = {print_polynomial(coeffs, degree)}")
        print(f"  R² = {r2:.6f}")
        print(f"  RMSE = {rmse:.6f}")
        print("-" * 50)

    # 执行三次样条插值
    print("\n三次样条插值结果:")
    cs, r2, rmse = cubic_spline_fit(O, S)
    print(f"  R² = {r2:.6f}")
    print(f"  RMSE = {rmse:.6f}")

    # 绘制拟合结果对比图
    plt.figure(figsize=(12, 8))
    plt.scatter(O, S, color='red', label='原始数据')

    # 绘制各多项式拟合曲线
    O_fine = np.linspace(0, 100, 500)
    colors = ['blue', 'green', 'purple', 'orange']

    for i, degree in enumerate(range(2, 6)):
        _, _, _, p = polynomial_fit(O, S, degree)
        plt.plot(O_fine, p(O_fine), color=colors[i],
                 label=f'{degree}次多项式 (R²={r2_score(S, p(O)):.4f})')

    # 绘制三次样条曲线
    plt.plot(O_fine, cs(O_fine), color='black', linestyle='--',
             label=f'三次样条 (R²={r2_score(S, cs(O)):.4f})')

    plt.xlabel('开敞度 (%)')
    plt.ylabel('平均得分')
    plt.title('开敞度与平均得分的拟合模型对比')
    plt.legend()
    plt.grid(True)
    plt.savefig('fitting_comparison.png', dpi=300)
    plt.show()

    # 输出专注度计算公式
    print("\n专注度计算公式:")
    print("F(O) = ((S(O) - 79) / 33.75)³")

    # 计算关键点的专注度
    print("\n关键点的专注度计算:")
    key_points = [12.5, 25, 50, 87.5]
    for o in key_points:
        s = cs(o)
        f = ((s - 79) / 33.75) ** 3
        print(f"O={o}%, S={s:.4f}, F={f:.4f}")


if __name__ == "__main__":
    main()