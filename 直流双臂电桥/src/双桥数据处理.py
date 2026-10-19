"""直流双臂电桥 — 数据处理与 R-t 曲线绘图

数据来源：data/实验数据.xlsx（与 data/images/实验数据.jpg 手写原始记录一致）
输出：Template/figures/Rt_curve.pdf（供 LaTeX 引用）
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

matplotlib.rcParams["font.sans-serif"] = ["SimHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False

S3 = np.sqrt(3.0)

# ---------- 1. 电阻率 ----------
R = 6.52e-4      # Ω，QJ44 电桥读数，精度等级 0.2%
d = 4.04e-3      # m，游标卡尺 0.02 mm
L = 30.00e-2     # m，米尺 0.5 mm
rho = R * np.pi * d**2 / (4 * L)

uR = 0.002 * R / S3                       # 电桥 0.2% 误差限按均匀分布
ud = 0.02e-3 / S3                         # 卡尺分度值 0.02 mm
uL = 0.5e-3 / S3                          # 米尺分度值 0.5 mm

rel_R, rel_d, rel_L = uR / R, 2 * ud / d, uL / L
rel_rho = np.sqrt(rel_R**2 + rel_d**2 + rel_L**2)
u_rho = rho * rel_rho

print(f"rho = {rho:.4e} Ω·m")
print(f"u(R)={uR:.3e}  u(d)={ud:.3e} m  u(L)={uL:.3e} m")
print(f"相对分量: R {rel_R*100:.3f}%  d {rel_d*100:.3f}%  L {rel_L*100:.3f}%")
print(f"rel_rho = {rel_rho*100:.3f}%   u(rho) = {u_rho:.3e} Ω·m")

# ---------- 2. 电阻温度系数 ----------
t = np.array([24.3, 29.3, 34.3, 39.3, 44.3, 49.3, 54.3, 59.3, 64.3, 69.3])  # °C
Rt = np.array([4.815, 4.908, 5.007, 5.102, 5.190,
               5.288, 5.359, 5.471, 5.566, 5.660]) * 1e-3              # Ω

# 方法一：分组逐差  alpha_i = (R_{i+5}-R_i) / (R_i t_{i+5} - R_{i+5} t_i)
alphas = np.array([
    (Rt[i + 5] - Rt[i]) / (Rt[i] * t[i + 5] - Rt[i + 5] * t[i]) for i in range(5)
])
a_mean = alphas.mean()
print("\nalpha_i =", np.array2string(alphas * 1e3, precision=2, suppress_small=True), "×10^-3 /°C")
print(f"alpha_mean = {a_mean:.4e} /°C")

# 方法二：最小二乘线性拟合 R = R0 (1 + alpha t) = b + a t
A = np.vstack([t, np.ones_like(t)]).T
a_fit, b_fit = np.linalg.lstsq(A, Rt, rcond=None)[0]
alpha_fit = a_fit / b_fit
resid = Rt - (a_fit * t + b_fit)
print(f"fit: R = ({a_fit*1e3:.5f} t + {b_fit*1e3:.5f})×10^-3 Ω")
print(f"alpha_fit = {alpha_fit:.4e} /°C,  max|resid| = {np.abs(resid).max():.2e} Ω")

# 与理论值比较（铜 alpha = 4.33e-3 /°C）
alpha_ref = 4.33e-3
for name, val in (("逐差法", a_mean), ("图解法", alpha_fit)):
    print(f"{name} 相对误差 = {abs(val - alpha_ref)/alpha_ref*100:.2f}%")

# ---------- 3. R-t 图 ----------
fig, ax = plt.subplots(figsize=(7, 4.6))
t_fit = np.linspace(t.min() - 2, t.max() + 2, 100)
ax.plot(t_fit, (a_fit * t_fit + b_fit) * 1e3, "-", color="#2980B9", lw=1.6,
        label=f"拟合 $R_t=({a_fit*1e3:.5f}t+{b_fit*1e3:.5f})\\times10^{{-3}}\\ \\Omega$")
ax.plot(t, Rt * 1e3, "o", ms=5, color="#E74C3C", zorder=5, label="实验数据")
ax.set_xlabel("温度 $t$ / $^\\circ$C")
ax.set_ylabel("电阻 $R_t$ / $10^{-3}\\ \\Omega$")
ax.set_title("铜导体电阻随温度的变化")
ax.grid(True, alpha=0.3)
ax.legend(loc="upper left", fontsize=10)
fig.tight_layout()
fig.savefig("Template/figures/Rt_curve.pdf")
print("\nsaved Template/figures/Rt_curve.pdf")
