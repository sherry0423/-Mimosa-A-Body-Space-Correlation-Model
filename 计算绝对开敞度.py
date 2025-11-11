import numpy as np


def find_O_from_F(F_target):
    # 构造多项式系数（常数项减去 F_target）
    coeffs = [
        -0.000038,
        0.007576,
        -0.463138,
        8.205234,
        56.921186 - F_target
    ]
    # 求解多项式的所有根
    roots = np.roots(coeffs)
    # 提取实数部分
    real_roots = roots[np.isreal(roots)].real
    return real_roots


# 主程序：交互式输入F值
while True:
    try:
        # 获取用户输入
        user_input = input("请输入F值（输入q退出）：")

        # 检查是否退出
        if user_input.lower() == 'q':
            break

        # 将输入转换为浮点数
        F_value = float(user_input)

        # 计算对应的O值
        O_solutions = find_O_from_F(F_value)

        # 输出结果
        if len(O_solutions) > 0:
            print(f"当 F = {F_value} 时，可能的O值有：{O_solutions}")
        else:
            print(f"当 F = {F_value} 时，没有找到实数解。")

    except ValueError:
        print("输入无效，请输入一个数字或q退出。")
    except Exception as e:
        print(f"发生错误：{e}")

print("程序已退出。")