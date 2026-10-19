"""
数据处理脚本：用霍尔法测直流圆线圈与亥姆霍兹线圈磁场
生成 B-X 曲线图及理论对比，计算相对误差
"""
import numpy as np
import matplotlib
import matplotlib.font_manager as fm
import os
# --- 中文字体配置 ---
# matplotlib 3.11 的 rcParams 字体查找存在 bug，中文会渲染为同一字符的重复。
# 解决方案：使用 FontProperties(fname=字体文件路径) 显式指定字体。
_CN_FONT_PATH = r'C:\Windows\Fonts\simhei.ttf'
_cn_font = fm.FontProperties(fname=_CN_FONT_PATH)
# 仅用于 axes.unicode_minus（负号渲染）
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
from pathlib import Path

# 输出目录
FIG_DIR = Path(r'c:\Users\peago\Desktop\PHYLAB\Hall_method\Template\figures')
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 物理常数与实验参数
# ============================================================
mu0 = 4 * np.pi * 1e-7       # 真空磁导率 T·m/A
N = 400                       # 线圈匝数
I_exc = 0.400                 # 励磁电流 A
R = 0.100                     # 线圈半径 m

# ============================================================
# 1. 测量地磁场
# ============================================================
B_earth = 0.028  # mT (28 µT)

# ============================================================
# 2. 单线圈轴向磁场分布
# ============================================================
# 实验数据（B正: 正向电流, B反: 反向电流, B平均: 平均值）
X_axial = np.array([-5.00, -4.00, -3.00, -2.00, -1.00, 0.00, 1.00, 2.00, 3.00, 4.00, 5.00])
B_fwd_axial = np.array([0.720, 0.804, 0.882, 0.942, 0.988, 1.006, 0.990, 0.946, 0.884, 0.808, 0.724])
B_rev_axial = np.array([0.720, 0.806, 0.884, 0.944, 0.988, 1.002, 0.988, 0.946, 0.884, 0.804, 0.720])
B_avg_axial = (B_fwd_axial + B_rev_axial) / 2

# 理论值: B = μ₀NIR² / [2(R² + x²)^(3/2)]
def B_single_coil(x_cm, N=400, I=0.400, R=0.100):
    """单线圈轴线上磁感应强度（x_cm 为厘米）"""
    x = x_cm * 1e-2  # 转换为米
    B = mu0 * N * I * R**2 / (2 * (R**2 + x**2)**1.5)
    return B * 1e3  # 转换为 mT

B_theory_axial = B_single_coil(X_axial)
rel_err_axial = (B_avg_axial - B_theory_axial) / B_theory_axial * 100

print("=" * 70)
print("1. 单线圈轴向磁场分布")
print("=" * 70)
print(f"{'X(cm)':>8} {'B正(mT)':>10} {'B反(mT)':>10} {'B平均(mT)':>10} {'B理论(mT)':>10} {'相对误差(%)':>12}")
for i in range(len(X_axial)):
    print(f"{X_axial[i]:>8.2f} {B_fwd_axial[i]:>10.3f} {B_rev_axial[i]:>10.3f} {B_avg_axial[i]:>10.3f} {B_theory_axial[i]:>10.3f} {rel_err_axial[i]:>12.1f}")

# ============================================================
# 3. 单线圈径向磁场分布
# ============================================================
Y_radial = np.array([-5.00, -4.00, -3.00, -2.00, -1.00, 0.00, 1.00, 2.00, 3.00, 4.00, 5.00])
B_fwd_radial = np.array([1.240, 1.138, 1.078, 1.036, 1.012, 1.006, 1.016, 1.042, 1.084, 1.148, 1.256])
B_rev_radial = np.array([1.236, 1.132, 1.068, 1.028, 1.006, 1.000, 1.006, 1.028, 1.076, 1.140, 1.244])
B_avg_radial = (B_fwd_radial + B_rev_radial) / 2

print("\n" + "=" * 70)
print("2. 单线圈径向磁场分布")
print("=" * 70)
print(f"{'Y(cm)':>8} {'B正(mT)':>10} {'B反(mT)':>10} {'B平均(mT)':>10}")
for i in range(len(Y_radial)):
    print(f"{Y_radial[i]:>8.2f} {B_fwd_radial[i]:>10.3f} {B_rev_radial[i]:>10.3f} {B_avg_radial[i]:>10.3f}")

# ============================================================
# 4. 亥姆霍兹线圈轴向磁场分布
# ============================================================
X_helm = np.array([
    -12.00, -11.00, -10.00, -9.00, -8.00, -7.00, -6.00, -5.00, -4.00, -3.00, -2.00, -1.00,
     0.00,  1.00,   2.00,  3.00,  4.00,  5.00,  6.00,  7.00,  8.00,  9.00, 10.00, 11.00, 12.00
])
B_fwd_helm = np.array([
    0.682, 0.782, 0.886, 1.006, 1.116, 1.222, 1.308, 1.374, 1.422, 1.446, 1.460, 1.462,
    1.464, 1.462, 1.458, 1.448, 1.418, 1.372, 1.308, 1.218, 1.122, 1.004, 0.898, 0.788, 0.690
])
B_rev_helm = np.array([
    0.670, 0.776, 0.884, 1.002, 1.110, 1.218, 1.302, 1.372, 1.420, 1.440, 1.458, 1.460,
    1.464, 1.458, 1.454, 1.440, 1.412, 1.364, 1.302, 1.216, 1.116, 1.000, 0.890, 0.776, 0.680
])
B_avg_helm = (B_fwd_helm + B_rev_helm) / 2

# 理论值: 亥姆霍兹线圈 B(x) = B_coil1(x) + B_coil2(x)
# 两线圈分别位于 x = ±R/2 处
def B_helmholtz(x_cm, N=400, I=0.400, R=0.100):
    """亥姆霍兹线圈轴线上磁感应强度"""
    x = x_cm * 1e-2  # 转换为米
    d = R / 2  # 每个线圈到中心的距离
    B1 = mu0 * N * I * R**2 / (2 * (R**2 + (x + d)**2)**1.5)
    B2 = mu0 * N * I * R**2 / (2 * (R**2 + (x - d)**2)**1.5)
    return (B1 + B2) * 1e3  # 转换为 mT

B_theory_helm = B_helmholtz(X_helm)
rel_err_helm = (B_avg_helm - B_theory_helm) / B_theory_helm * 100

print("\n" + "=" * 70)
print("3. 亥姆霍兹线圈轴向磁场分布")
print("=" * 70)
print(f"{'X(cm)':>8} {'B正(mT)':>10} {'B反(mT)':>10} {'B平均(mT)':>10} {'B理论(mT)':>10} {'相对误差(%)':>12}")
for i in range(len(X_helm)):
    print(f"{X_helm[i]:>8.2f} {B_fwd_helm[i]:>10.3f} {B_rev_helm[i]:>10.3f} {B_avg_helm[i]:>10.3f} {B_theory_helm[i]:>10.3f} {rel_err_helm[i]:>12.1f}")

# 亥姆霍兹线圈中心理论值
B0_helm_theory = B_helmholtz(0)
# 均匀区域 (-3cm 到 +3cm) 的平均实验值
mask_uniform = np.abs(X_helm) <= 3
B_avg_uniform = np.mean(B_avg_helm[mask_uniform])
print(f"\n亥姆霍兹线圈中心理论值 B0 = {B0_helm_theory:.3f} mT")
print(f"均匀区域(|X|<=3cm)实验平均值 B = {B_avg_uniform:.3f} mT")
print(f"均匀区域与理论值误差 = {(B_avg_uniform - B0_helm_theory)/B0_helm_theory*100:.1f}%")

# ============================================================
# 绘图（使用 FontProperties 显式指定中文字体）
# ============================================================
fp = _cn_font  # 中文字体 FontProperties 对象

plt.style.use('seaborn-v0_8-whitegrid')

# --- 图1: 单线圈轴向 B-X 曲线 ---
fig1, ax1 = plt.subplots(figsize=(8, 5))
X_fine = np.linspace(-5, 5, 200)
B_theory_fine = B_single_coil(X_fine)

ax1.scatter(X_axial, B_avg_axial, color='red', s=50, zorder=5, label='实验值')
ax1.plot(X_fine, B_theory_fine, 'b-', linewidth=1.5, label='理论曲线')
ax1.set_xlabel('轴向距离 $X$ / cm', fontproperties=fp, fontsize=12)
ax1.set_ylabel('磁感应强度 $B$ / mT', fontproperties=fp, fontsize=12)
ax1.set_title('载流圆线圈轴向磁场分布', fontproperties=fp, fontsize=14)
ax1.legend(prop=fp, fontsize=11)
ax1.set_xlim(-5.5, 5.5)
fig1.tight_layout()
fig1.savefig(FIG_DIR / 'single_coil_axial.pdf', dpi=300)
fig1.savefig(FIG_DIR / 'single_coil_axial.png', dpi=150)
print("\n图1已保存: single_coil_axial.pdf")

# --- 图2: 单线圈径向 B-Y 曲线 ---
fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.scatter(Y_radial, B_avg_radial, color='red', s=50, zorder=5, label='实验值')
# 径向没有简单解析式，仅画实验点并连线
ax2.plot(Y_radial, B_avg_radial, 'r--', alpha=0.5, linewidth=1)
ax2.set_xlabel('径向距离 $Y$ / cm', fontproperties=fp, fontsize=12)
ax2.set_ylabel('磁感应强度 $B$ / mT', fontproperties=fp, fontsize=12)
ax2.set_title('载流圆线圈径向磁场分布', fontproperties=fp, fontsize=14)
ax2.legend(prop=fp, fontsize=11)
ax2.set_xlim(-5.5, 5.5)
fig2.tight_layout()
fig2.savefig(FIG_DIR / 'single_coil_radial.pdf', dpi=300)
fig2.savefig(FIG_DIR / 'single_coil_radial.png', dpi=150)
print("图2已保存: single_coil_radial.pdf")

# --- 图3: 亥姆霍兹线圈 B-X 曲线 ---
fig3, ax3 = plt.subplots(figsize=(10, 5.5))
X_helm_fine = np.linspace(-12, 12, 400)
B_helm_fine = B_helmholtz(X_helm_fine)

ax3.scatter(X_helm, B_avg_helm, color='red', s=40, zorder=5, label='实验值')
ax3.plot(X_helm_fine, B_helm_fine, 'b-', linewidth=1.5, label='理论曲线')
# 标注两线圈位置
ax3.axvline(x=-5, color='gray', linestyle=':', alpha=0.7, label='线圈位置')
ax3.axvline(x=5, color='gray', linestyle=':', alpha=0.7)
ax3.set_xlabel('轴向距离 $X$ / cm', fontproperties=fp, fontsize=12)
ax3.set_ylabel('磁感应强度 $B$ / mT', fontproperties=fp, fontsize=12)
ax3.set_title('亥姆霍兹线圈轴向磁场分布', fontproperties=fp, fontsize=14)
ax3.legend(prop=fp, fontsize=11)
ax3.set_xlim(-13, 13)
fig3.tight_layout()
fig3.savefig(FIG_DIR / 'helmholtz_coil.pdf', dpi=300)
fig3.savefig(FIG_DIR / 'helmholtz_coil.png', dpi=150)
print("图3已保存: helmholtz_coil.pdf")

# --- 图4: 三图合并（用于报告） ---
fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))

# 子图1: 单线圈轴向
ax = axes[0]
ax.scatter(X_axial, B_avg_axial, color='red', s=30, zorder=5, label='实验值')
ax.plot(X_fine, B_theory_fine, 'b-', linewidth=1.2, label='理论曲线')
ax.set_xlabel('$X$ / cm', fontproperties=fp, fontsize=11)
ax.set_ylabel('$B$ / mT', fontproperties=fp, fontsize=11)
ax.set_title('(a) 单线圈轴向', fontproperties=fp, fontsize=12)
ax.legend(prop=fp, fontsize=9)

# 子图2: 单线圈径向
ax = axes[1]
ax.scatter(Y_radial, B_avg_radial, color='red', s=30, zorder=5, label='实验值')
ax.plot(Y_radial, B_avg_radial, 'r--', alpha=0.5, linewidth=1)
ax.set_xlabel('$Y$ / cm', fontproperties=fp, fontsize=11)
ax.set_ylabel('$B$ / mT', fontproperties=fp, fontsize=11)
ax.set_title('(b) 单线圈径向', fontproperties=fp, fontsize=12)
ax.legend(prop=fp, fontsize=9)

# 子图3: 亥姆霍兹线圈
ax = axes[2]
ax.scatter(X_helm, B_avg_helm, color='red', s=25, zorder=5, label='实验值')
ax.plot(X_helm_fine, B_helm_fine, 'b-', linewidth=1.2, label='理论曲线')
ax.axvline(x=-5, color='gray', linestyle=':', alpha=0.5)
ax.axvline(x=5, color='gray', linestyle=':', alpha=0.5)
ax.set_xlabel('$X$ / cm', fontproperties=fp, fontsize=11)
ax.set_ylabel('$B$ / mT', fontproperties=fp, fontsize=11)
ax.set_title('(c) 亥姆霍兹线圈轴向', fontproperties=fp, fontsize=12)
ax.legend(prop=fp, fontsize=9)

fig.tight_layout()
fig.savefig(FIG_DIR / 'B_X_curves_combined.pdf', dpi=300)
fig.savefig(FIG_DIR / 'B_X_curves_combined.png', dpi=150)
print("图4(合并)已保存: B_X_curves_combined.pdf")

# ============================================================
# 误差统计
# ============================================================
print("\n" + "=" * 70)
print("误差统计汇总")
print("=" * 70)
print(f"单线圈轴向 平均相对误差: {np.mean(np.abs(rel_err_axial)):.1f}%")
print(f"单线圈轴向 最大相对误差: {np.max(np.abs(rel_err_axial)):.1f}% (X={X_axial[np.argmax(np.abs(rel_err_axial))]:.1f} cm)")
print(f"亥姆霍兹线圈 平均相对误差: {np.mean(np.abs(rel_err_helm)):.1f}%")
print(f"亥姆霍兹线圈 最大相对误差: {np.max(np.abs(rel_err_helm)):.1f}% (X={X_helm[np.argmax(np.abs(rel_err_helm))]:.1f} cm)")

# 单线圈中心B值
B0_single_theory = B_single_coil(0)
B0_single_exp = B_avg_axial[5]  # X=0处
print(f"\n单线圈中心 理论值: {B0_single_theory:.3f} mT, 实验值: {B0_single_exp:.3f} mT, 误差: {(B0_single_exp-B0_single_theory)/B0_single_theory*100:.1f}%")
print(f"亥姆霍兹线圈中心 理论值: {B0_helm_theory:.3f} mT, 实验值: {B_avg_helm[12]:.3f} mT, 误差: {(B_avg_helm[12]-B0_helm_theory)/B0_helm_theory*100:.1f}%")

print("\n数据处理完成！")
