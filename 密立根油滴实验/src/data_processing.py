"""
密立根油滴实验数据处理脚本
"""
import numpy as np
import sys
import os

# 设置输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.append('.')
from utils.uncertainty import type_a_uncertainty

# 实验常数
d = 5.00e-3  # 极板间距，单位：m
l = 1.5e-3  # 下落距离，单位：m (1.5mm，测量距离)
rho = 981  # 油的密度，单位：kg/m³
eta = 1.83e-5  # 空气粘滞系数，单位：Pa·s
g = 9.794  # 杭州地区重力加速度，单位：m/s²
b = 6.17e-6  # 修正常数，单位：Pa·m
p = 1.01e5  # 大气压强，单位：Pa

# 实验数据（从原始数据表中提取）
data = [
    {'V': 60, 't': 7.38, 'q': 0.846e-17},
    {'V': 62, 't': 7.33, 'q': 0.827e-17},
    {'V': 68, 't': 5.53, 'q': 1.16e-17},
    {'V': 142, 't': 3.31, 'q': 1.22e-17},
    {'V': 87, 't': 1.35, 'q': 7.84e-17},
    {'V': 96, 't': 6.20, 'q': 0.691e-17},
    {'V': 171, 't': 4.93, 'q': 0.552e-17},
    {'V': 265, 't': 11.6, 'q': 0.0951e-17},
    {'V': 128, 't': 2.63, 'q': 1.93e-17},
    {'V': 267, 't': 2.50, 'q': 1.00e-17},
]

def calculate_charge(V, t):
    """
    计算油滴电荷量

    参数:
        V: 平衡电压 (V)
        t: 下落时间 (s)

    返回:
        q: 电荷量 (C)
        r: 油滴半径 (m)
    """
    v = l / t  # 下落速度

    # 未修正的油滴半径
    r_uncorrected = np.sqrt(9 * eta * v / (2 * rho * g))

    # 修正后的粘滞系数
    eta_corrected = eta / (1 + b / (p * r_uncorrected))

    # 修正后的油滴半径
    r = np.sqrt(9 * eta_corrected * v / (2 * rho * g))

    # 油滴质量
    m = (4/3) * np.pi * r**3 * rho

    # 电荷量
    q = m * g * d / V

    return q, r

print("=" * 80)
print("密立根油滴实验数据处理")
print("=" * 80)

# 计算每颗油滴的电荷量（使用实验数据.md中的实测值）
charges = []
print("\n序号\t平衡电压V(V)\t下落时间t(s)\t电荷量q(×10⁻¹⁹C)\t电荷倍数n")
print("-" * 80)

for i, d_point in enumerate(data, 1):
    V = d_point['V']
    t = d_point['t']
    q = d_point['q']  # 直接使用实验数据.md中的测量值
    charges.append(q)

    # 估算电荷倍数（相对于1.6e-19C）
    n = round(q / 1.6e-19)

    print(f"{i}\t{V}\t\t{t:.2f}\t\t{q/1e-19:.3f}\t\t\t{n}")

charges = np.array(charges)

# 公约数法计算基本电荷
print("\n" + "=" * 80)
print("基本电荷计算（公约数法）")
print("=" * 80)

# 方法1：直接除以估计倍数
e_values = []
for i, q in enumerate(charges, 1):
    n = round(q / 1.6e-19)
    if n > 0:
        e_est = q / n
        e_values.append(e_est)
        print(f"油滴{i}: q = {q/1e-19:.3f}×10⁻¹⁹C, n ≈ {n}, e ≈ {e_est/1e-19:.4f}×10⁻¹⁹C")

e_values = np.array(e_values)
e_mean = np.mean(e_values)
e_std = np.std(e_values, ddof=1)

print("\n" + "-" * 80)
print(f"基本电荷平均值: e = {e_mean/1e-19:.4f}×10⁻¹⁹ C")
print(f"标准偏差: σ = {e_std/1e-19:.4f}×10⁻¹⁹ C")

# 不确定度分析
_, _, u_a = type_a_uncertainty(e_values)
print(f"A类不确定度: u_A = {u_a/1e-19:.4f}×10⁻¹⁹ C")

# 与标准值比较
e_standard = 1.602e-19  # 标准电子电荷量
relative_error = abs(e_mean - e_standard) / e_standard * 100
print(f"\n标准电子电荷量: e₀ = 1.602×10⁻¹⁹ C")
print(f"相对误差: E_r = {relative_error:.2f}%")

print("\n" + "=" * 80)
print(f"最终结果: e = ({e_mean/1e-19:.3f} ± {u_a/1e-19:.3f})×10⁻¹⁹ C")
print("=" * 80)

# 生成LaTeX表格数据
print("\n\nLaTeX表格数据：")
print("\\begin{table}[H]")
print("    \\centering")
print("    \\caption{密立根油滴实验测量数据与计算结果}")
print("    \\begin{tabular}{cccccc}")
print("        \\toprule")
print("        序号 & 平衡电压 $V$/V & 下落时间 $t$/s & 电荷量 $q$/(×10$^{-19}$C) & 电荷倍数 $n$ & 基本电荷 $e$/(×10$^{-19}$C) \\\\")
print("        \\midrule")

for i, (d_point, q) in enumerate(zip(data, charges), 1):
    V = d_point['V']
    t = d_point['t']
    n = round(q / 1.6e-19)
    if n > 0:
        e_i = q / n
        print(f"        {i} & {V} & {t:.2f} & {q/1e-19:.2f} & {n} & {e_i/1e-19:.3f} \\\\")

print("        \\midrule")
print(f"        \\multicolumn{{5}}{{c}}{{平均值}} & {e_mean/1e-19:.3f} \\\\")
print("        \\bottomrule")
print("    \\end{tabular}")
print("    \\label{tab:millikan_data}")
print("\\end{table}")
