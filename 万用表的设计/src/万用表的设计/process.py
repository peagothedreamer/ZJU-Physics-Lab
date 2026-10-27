"""万用表的设计：校准数据拟合、等级计算与作图。

运行：..\\..\\.venv\\Scripts\\python.exe process.py
输出：Template/figures/ammeter_calibration.pdf, voltmeter_calibration.pdf,
      ohmmeter_curve.pdf
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy.optimize import curve_fit

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / "Template" / "figures"

matplotlib.rcParams.update(
    {
        "font.sans-serif": ["SimHei", "Microsoft YaHei"],
        "axes.unicode_minus": False,
        "font.size": 11,
        "axes.linewidth": 0.8,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.top": True,
        "ytick.right": True,
        "figure.dpi": 150,
    }
)

# ---------------------------------------------------------------- 数据
# 5 mA 电流表：改装表示值 Ix / mA，标准表示值 I0 / mA
Ix = np.array([1.00, 2.00, 3.00, 4.00, 5.00])
I0 = np.array([1.02, 2.08, 3.04, 4.06, 5.00])
dI = I0 - Ix

# 5 V 电压表：改装表示值 Ux / V，标准表示值 U0 / V
Ux = np.array([1.00, 2.00, 3.00, 4.00, 5.00])
U0 = np.array([1.03, 1.98, 3.08, 4.05, 5.00])
dU = U0 - Ux

# 欧姆表：待测电阻 Rx / Ω，电流计读数 I / mA
Rx = np.array([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000], dtype=float)
I = np.array([1.00, 0.76, 0.62, 0.51, 0.44, 0.39, 0.34, 0.30, 0.28, 0.26, 0.24, 0.13, 0.09])

CLASSES = np.array([0.1, 0.2, 0.5, 1.0, 1.5, 2.5, 5.0])


def grade(gamma_percent):
    """按引用误差百分数向上取标准准确度等级。"""
    return CLASSES[np.argmax(CLASSES >= gamma_percent)]


def fit_line(x, y):
    p, cov = np.polyfit(x, y, 1, cov=True)
    yfit = np.polyval(p, x)
    ss_res = np.sum((y - yfit) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    return p, np.sqrt(np.diag(cov)), 1 - ss_res / ss_tot, yfit


def report_calibration(name, x, y, full_scale, unit):
    d = y - x
    p, perr, r2, yfit = fit_line(x, y)
    gamma = np.max(np.abs(d)) / full_scale * 100
    rel = np.abs(d) / y * 100
    print(f"\n=== {name} ===")
    print(f"示值误差 Δ = {np.round(d, 3)} {unit}")
    print(f"最大绝对误差 {np.max(np.abs(d)):.3f} {unit}, 最大相对误差 {np.max(rel):.2f}% @ {x[np.argmax(rel)]:.2f} {unit}")
    print(f"拟合: y = ({p[0]:.5f} ± {perr[0]:.5f}) x + ({p[1]:.5f} ± {perr[1]:.5f}), R² = {r2:.6f}")
    print(f"引用误差 γ = {gamma:.2f}%  →  {grade(gamma)} 级")
    print(f"平均误差 {d.mean():.4f} {unit}, 标准差 {d.std(ddof=1):.4f} {unit}, "
          f"u_A = {d.std(ddof=1)/np.sqrt(len(d)):.4f} {unit}")
    return d, p, perr, r2, gamma


report_calibration("5 mA 电流表", Ix, I0, 5.0, "mA")
report_calibration("5 V 电压表", Ux, U0, 5.0, "V")


# ---------------------------------------------------------------- 欧姆表
def ohm_model(r, ig, r0):
    return ig * r0 / (r0 + r)


popt, pcov = curve_fit(ohm_model, Rx, I, p0=[1.0, 300.0])
perr = np.sqrt(np.diag(pcov))
Ig, R0 = popt
Ipred = ohm_model(Rx, *popt)
resid = I - Ipred
ss_res = np.sum(resid**2)
ss_tot = np.sum((I - I.mean()) ** 2)
r2 = 1 - ss_res / ss_tot

# 线性化 1/I = 1/Ig + Rx/(Ig R0)
p_lin = np.polyfit(Rx, 1 / I, 1)
Ig_lin = 1 / p_lin[1]
R0_lin = p_lin[1] / p_lin[0]
r2_lin = 1 - np.sum((1 / I - np.polyval(p_lin, Rx)) ** 2) / np.sum((1 / I - (1 / I).mean()) ** 2)

# 半偏位置（线性插值）
half = Ig / 2
idx = np.searchsorted(-I, -half)  # I 递减
r_lo, r_hi = Rx[idx - 1], Rx[idx]
i_lo, i_hi = I[idx - 1], I[idx]
r_half = r_lo + (half - i_lo) * (r_hi - r_lo) / (i_hi - i_lo)

print("\n=== 欧姆表 ===")
print(f"拟合 I = Ig·R0/(R0+Rx): Ig = {Ig:.4f} ± {perr[0]:.4f} mA, "
      f"R0 = {R0:.2f} ± {perr[1]:.2f} Ω, R² = {r2:.5f}")
print(f"线性化: Ig = {Ig_lin:.4f} mA, R0 = {R0_lin:.2f} Ω, R² = {r2_lin:.5f}")
print(f"半偏插值: R_中 = {r_half:.1f} Ω (I = {half:.3f} mA)")
print(f"拟合残差最大绝对值 {np.max(np.abs(resid)):.3f} mA, 最大相对偏差 {np.max(np.abs(resid/I))*100:.2f}%")
for r in [0, 100, 300, 1000, 3000]:
    sens = -Ig * R0 / (R0 + r) ** 2
    print(f"  Rx={r:>5.0f} Ω: dI/dRx = {sens*1e3:.3f} μA/Ω, I = {ohm_model(r, *popt):.3f} mA")

# ---------------------------------------------------------------- 作图
def style(ax):
    ax.minorticks_on()
    ax.tick_params(which="minor", length=2.5, width=0.6)
    ax.grid(True, which="major", alpha=0.25, linewidth=0.6)
    ax.grid(False, which="minor")


# 电流表
fig, ax = plt.subplots(figsize=(4.6, 3.6))
ax.plot(Ix, I0, "o", ms=5, mfc="white", mew=1.2, color="#1f4e79", label="实验数据")
xx = np.linspace(0.8, 5.2, 100)
ax.plot(xx, np.polyval(np.polyfit(Ix, I0, 1), xx), "-", lw=1.2, color="#c0504d", label="拟合直线")
ax.plot(xx, xx, "--", lw=0.9, color="0.45", label="$I_0=I_x$")
ax.set_xlabel("改装电流表示值 $I_x$ / mA")
ax.set_ylabel("标准电流表示值 $I_0$ / mA")
ax.set_xlim(0.8, 5.2)
ax.set_ylim(0.8, 5.2)
ax.legend(frameon=False, loc="upper left", fontsize=9)
style(ax)
fig.tight_layout()
fig.savefig(FIG / "ammeter_calibration.pdf")
fig.savefig(FIG / "ammeter_calibration.png", dpi=300)
plt.close(fig)

# 电压表
fig, ax = plt.subplots(figsize=(4.6, 3.6))
ax.plot(Ux, U0, "o", ms=5, mfc="white", mew=1.2, color="#1f4e79", label="实验数据")
ax.plot(xx, np.polyval(np.polyfit(Ux, U0, 1), xx), "-", lw=1.2, color="#c0504d", label="拟合直线")
ax.plot(xx, xx, "--", lw=0.9, color="0.45", label="$U_0=U_x$")
ax.set_xlabel("改装电压表示值 $U_x$ / V")
ax.set_ylabel("标准电压表示值 $U_0$ / V")
ax.set_xlim(0.8, 5.2)
ax.set_ylim(0.8, 5.2)
ax.legend(frameon=False, loc="upper left", fontsize=9)
style(ax)
fig.tight_layout()
fig.savefig(FIG / "voltmeter_calibration.pdf")
fig.savefig(FIG / "voltmeter_calibration.png", dpi=300)
plt.close(fig)

# 欧姆表
fig, ax = plt.subplots(figsize=(5.4, 3.8))
ax.plot(Rx, I, "o", ms=5, mfc="white", mew=1.2, color="#1f4e79", label="实验数据")
rr = np.linspace(0, 3000, 400)
ax.plot(rr, ohm_model(rr, *popt), "-", lw=1.1, color="#c0504d", label="拟合曲线")
ax.axhline(half, ls=":", lw=0.9, color="0.45")
ax.axvline(R0, ls=":", lw=0.9, color="0.45")
ax.annotate(
    f"中值电阻 $R_0={R0:.0f}\\ \\Omega$\n$I_g/2={half:.2f}\\ \\mathrm{{mA}}$",
    xy=(R0, half),
    xytext=(R0 + 260, half + 0.16),
    fontsize=9,
    arrowprops=dict(arrowstyle="-", lw=0.8, color="0.35"),
)
ax.set_xlabel("待测电阻 $R_x$ / Ω")
ax.set_ylabel("电流计读数 $I$ / mA")
ax.set_xlim(0, 3050)
ax.set_ylim(0, 1.08)
ax.legend(frameon=False, loc="upper right", fontsize=9)
style(ax)
fig.tight_layout()
fig.savefig(FIG / "ohmmeter_curve.pdf")
fig.savefig(FIG / "ohmmeter_curve.png", dpi=300)
plt.close(fig)

print("\n图已保存至", FIG)
