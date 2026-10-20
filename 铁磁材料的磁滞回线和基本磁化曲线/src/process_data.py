# -*- coding: utf-8 -*-
"""铁磁材料的磁滞回线和基本磁化曲线 —— 数据处理与绘图。

样品 1（环形铁氧体）：N1 = N2 = 150, L = 0.130 m, S = 1.24e-4 m^2
电路：R1 = 2.5 ohm, R2 = 10 kohm, C = 3 uF, f = 130 Hz

H = N1 * Ux / (R1 * L)
B = R2 * C * Uy / (N2 * S)
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams["font.sans-serif"] = ["SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "Template" / "figures"
FIG.mkdir(exist_ok=True)

# ---------------- 参数 ----------------
N1 = N2 = 150.0
L = 0.130          # m
S = 1.24e-4        # m^2
R1 = 2.5           # ohm
R2 = 10e3          # ohm
C = 3e-6           # F
F = 130.0          # Hz

kH = N1 / (R1 * L)          # A/m per V
kB = R2 * C / (N2 * S)      # T per V

# ---------------- 基本磁化曲线 ----------------
U = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
Ux = np.array([47.58, 95.52, 143.1, 192.6, 284.1, 702.6]) * 1e-3   # V
Uy = np.array([39.35, 79.64, 120.2, 159.2, 199.8, 237.4]) * 1e-3   # V

H = kH * Ux
B = kB * Uy
mu = B / H
mur = mu / (4 * np.pi * 1e-7)

# ---------------- 饱和磁滞回线（V = 3.00 V） ----------------
# 原始记录按测量顺序编号 1..48；同一 H 处有上、下两条支路。
loop_raw = [
    (702.6, 237.4), (650.0, 234.2), (600.0, 231.1), (550.0, 228.0),
    (500.0, 225.4), (500.0, 218.6), (450.0, 223.3), (450.0, 210.8),
    (400.0, 220.2), (400.0, 196.7), (350.0, 217.0), (350.0, 174.9),
    (300.0, 210.8), (300.0, 115.5), (250.0, 204.5), (250.0, 6.161),
    (246.8, 0.000), (200.0, 200.0), (200.0, -53.12), (150.0, 192.1),
    (150.0, -92.18), (100.0, 182.8), (100.0, -123.4), (50.00, 173.4),
    (50.00, -142.1), (0.000, 162.5), (0.000, -159.3), (-50.00, 143.7),
    (-50.00, -173.4), (-100.0, 123.4), (-100.0, -184.3), (-150.0, 95.31),
    (-150.0, -195.5), (-200.0, 54.68), (-200.0, -203.4), (-246.8, 0.000),
    (-246.8, -209.6), (-300.0, -106.2), (-300.0, -214.3), (-350.0, -171.8),
    (-350.0, -219.0), (-400.0, -196.8), (-400.0, -222.1), (-450.0, -210.9),
    (-450.0, -226.8), (-500.0, -218.7), (-500.0, -229.9), (-684.3, -235.9),
]
ux_raw = np.array([p[0] for p in loop_raw])
uy_raw = np.array([p[1] for p in loop_raw])

# 按原始编号（0-based）划分上下支路
upper_idx = [0, 1, 2, 3, 4, 6, 8, 10, 12, 14, 17, 19, 21, 23, 25, 27, 29,
             31, 33, 35, 37, 39, 41, 43, 45, 47]
lower_idx = [47, 46, 44, 42, 40, 38, 36, 34, 32, 30, 28, 26, 24, 22, 20, 18,
             16, 15, 13, 11, 9, 7, 5, 3, 2, 1, 0]

ux_loop = np.concatenate([ux_raw[upper_idx], ux_raw[lower_idx]]) * 1e-3
uy_loop = np.concatenate([uy_raw[upper_idx], uy_raw[lower_idx]]) * 1e-3
H_loop = kH * ux_loop
B_loop = kB * uy_loop

# ---------------- 特征量 ----------------
Hc_pos = kH * (246.8e-3)          # B = 0, 上行支路
Hc_neg = kH * (-246.8e-3)         # B = 0, 下行支路
Hc = (abs(Hc_pos) + abs(Hc_neg)) / 2

Br_pos = kB * (162.5e-3)          # H = 0, 下行支路
Br_neg = kB * (-159.3e-3)         # H = 0, 上行支路
Br = (abs(Br_pos) + abs(Br_neg)) / 2

Bm = (kB * 237.4e-3 + abs(kB * -235.9e-3)) / 2
Bm_pos = kB * 237.4e-3
Bm_neg = abs(kB * -235.9e-3)

# 多边形面积（闭合回线）
area = 0.5 * abs(np.dot(H_loop, np.roll(B_loop, -1)) -
                 np.dot(B_loop, np.roll(H_loop, -1)))

# ---------------- 不确定度 ----------------
dUx = dUy = 0.5e-3                 # V，光标读数（约半格）
dR1 = 0.01 * R1                    # 1%
dR2 = 0.01 * R2                    # 1%
dC = 0.05 * C                      # 5%
dL = 0.5e-3                        # m
dS = 0.01 * S                      # 1%

rel_Hc = np.sqrt((dUx / 246.8e-3) ** 2 + (dR1 / R1) ** 2 + (dL / L) ** 2)
rel_Br = np.sqrt((dUy / 162.5e-3) ** 2 + (dR2 / R2) ** 2 +
                 (dC / C) ** 2 + (dS / S) ** 2)
rel_Bm = np.sqrt((dUy / 237.4e-3) ** 2 + (dR2 / R2) ** 2 +
                 (dC / C) ** 2 + (dS / S) ** 2)
u_Hc = rel_Hc * Hc
u_Br = rel_Br * Br
u_Bm = rel_Bm * Bm
u_area = np.sqrt(rel_Hc ** 2 + rel_Br ** 2) * area

# ---------------- 输出 ----------------
print("kH = %.4f A/m per V, kB = %.6f T per V" % (kH, kB))
print("\n基本磁化曲线")
print("U/V\tUx/mV\tUy/mV\tH/(A/m)\tB/mT\tmu/(1e-3 H/m)\tkappar")
for row in zip(U, Ux * 1e3, Uy * 1e3, H, B * 1e3, mu * 1e3, mur):
    print("%.1f\t%.2f\t%.2f\t%.2f\t%.2f\t%.3f\t%.0f" % row)

print("\n特征量")
print("Hc  = %.2f +/- %.2f A/m (%.2f%%)" % (Hc, u_Hc, rel_Hc * 100))
print("Br  = %.2f +/- %.2f mT (%.2f%%)" % (Br * 1e3, u_Br * 1e3, rel_Br * 100))
print("Bm  = %.2f +/- %.2f mT (%.2f%%)" % (Bm * 1e3, u_Bm * 1e3, rel_Bm * 100))
print("Bm+ = %.2f mT, Bm- = %.2f mT" % (Bm_pos * 1e3, Bm_neg * 1e3))
print("area = %.2f +/- %.2f J/m^3" % (area, u_area))

print("\n回线表（原始编号顺序）")
for i, (a, b) in enumerate(zip(ux_raw, uy_raw), 1):
    print("%d\t%.1f\t%.2f\t%.2f\t%.2f" %
          (i, a, b, kH * a * 1e-3, kB * b * 1e-3 * 1e3))

# ---------------- 图 1：基本磁化曲线 + mu-H ----------------
fig, ax1 = plt.subplots(figsize=(6.4, 4.0), constrained_layout=True)
ax1.plot(H, B * 1e3, "o-", color="#1f4e79", lw=1.4, ms=4,
         label="B–H")
ax1.set_xlabel("H / (A·m$^{-1}$)")
ax1.set_ylabel("B / mT", color="#1f4e79")
ax1.tick_params(axis="y", colors="#1f4e79")
ax1.grid(alpha=0.3)

ax2 = ax1.twinx()
ax2.plot(H, mur, "s--", color="#c0392b", lw=1.2, ms=4, label="μr–H")
ax2.set_ylabel("相对磁导率 μ$_r$", color="#c0392b")
ax2.tick_params(axis="y", colors="#c0392b")

lines = ax1.get_lines() + ax2.get_lines()
ax1.legend(lines, [l.get_label() for l in lines], loc="center right")
fig.savefig(FIG / "basic_curve.pdf")
plt.close(fig)

# ---------------- 图 2：饱和磁滞回线 ----------------
fig, ax = plt.subplots(figsize=(5.4, 4.4), constrained_layout=True)
ax.plot(H_loop, B_loop * 1e3, "-", color="#1f4e79", lw=1.4, label="B–H 回线")
ax.plot(H_loop, B_loop * 1e3, "o", color="#1f4e79", ms=2.2, alpha=0.7)
ax.axhline(0, color="gray", lw=0.6)
ax.axvline(0, color="gray", lw=0.6)
ax.plot([0, 0], [Br * 1e3, -Br * 1e3], "o", color="#c0392b", ms=5, label="B$_r$")
ax.plot([Hc, -Hc], [0, 0], "s", color="#27ae60", ms=5, label="H$_c$")
ax.set_xlabel("H / (A·m$^{-1}$)")
ax.set_ylabel("B / mT")
ax.set_title("饱和磁滞回线（U = 3.00 V）")
ax.grid(alpha=0.3)
ax.legend(loc="lower right")
fig.savefig(FIG / "hysteresis_loop.pdf")
plt.close(fig)

print("\nfigures ->", FIG)
