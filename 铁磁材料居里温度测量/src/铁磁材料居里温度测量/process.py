"""铁磁材料居里温度测量 — 数据处理

用拐点法（dU/dT 极值）确定居里温度 Tc，并将 Tc 的波动作为 A 类不确定度。
数据来源：data/实验数据.md（升温曲线，40→120 °C）

运行：..\..\.venv\Scripts\python.exe process.py
"""

from pathlib import Path

import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.optimize import curve_fit

HERE = Path(__file__).resolve().parent
FIGDIR = HERE / "figures"

# 原始记录（升温）：T / °C, U / mV
# 87.5 °C 处记录纸上为划改后的 15.7 mV，按记录纸原样保留
RAW = """
40.0 36.0   82.5 24.2   93.5 11.0
45.0 36.2   83.0 22.4   94.0 10.7
50.0 36.4   83.5 21.5   94.5 10.4
55.0 36.5   84.0 20.5   95.0 10.2
60.0 36.7   84.5 19.6  100.0  8.0
65.0 36.8   85.0 18.9  105.0  6.5
70.0 36.9   85.5 18.2  110.0  4.7
75.0 36.6   86.0 17.5  115.0  3.2
75.5 36.4   86.5 16.9  120.0  2.4
76.0 36.2   87.0 16.4
76.5 36.0   87.5 15.7
77.0 35.6   88.0 15.2
77.5 35.3   88.5 14.5
78.0 34.3   89.0 14.1
78.5 33.9   89.5 13.8
79.0 33.1   90.0 13.3
79.5 32.4   90.5 13.0
80.0 31.2   91.0 12.6
80.5 29.9   91.5 12.2
81.0 28.6   92.0 11.9
81.5 27.2   92.5 11.6
82.0 25.9   93.0 11.3
"""


def load() -> tuple[np.ndarray, np.ndarray]:
    nums = np.array(RAW.split(), dtype=float)
    T, U = nums[0::2], nums[1::2]
    return T, U


def model(T, U_para, A, Tc, w, k):
    """顺磁基线 + 铁磁富余项：U(T) = 基线 + 相变台阶。

    基线取 (1+exp((T-Tc)/w))^{-1} 型平滑过渡，避免超温区数据被过拟合。
    """
    x = (T - Tc) / w
    return U_para + A / (1.0 + np.exp(x)) + k * (T - 100.0) / 20.0 * (1.0 / (1.0 + np.exp(x)))


def inflection_spline(T: np.ndarray, U: np.ndarray, lo: float, hi: float) -> tuple[float, float]:
    """在 [lo, hi] 区间用三次样条求 dU/dT 极值点，返回 (Tc, 斜率极大值)。"""
    spl = UnivariateSpline(T, U, k=3, s=len(T) * 0.05)
    grid = np.linspace(lo, hi, 20001)
    d1 = spl.derivative(1)(grid)
    i = int(np.argmin(d1))  # U 单调下降，拐点 = 下降最快 = dU/dT 最小
    d2 = spl.derivative(2)(grid)
    # 在极小值附近线性插值到 d2 = 0，提高定位精度
    for j in range(max(i - 1, 0), i + 1):
        if d2[j] * d2[j + 1] < 0:
            frac = d2[j] / (d2[j] - d2[j + 1])
            return float(grid[j] + frac * (grid[1] - grid[0])), float(d1[i])
    return float(grid[i]), float(d1[i])


def main() -> None:
    T, U = load()
    order = np.argsort(T)
    T, U = T[order], U[order]
    print(f"数据点 n = {len(T)},  T: {T[0]:.1f} → {T[-1]:.1f} °C,  U: {U[0]:.1f} → {U[-1]:.1f} mV")

    Tc_s, slope = inflection_spline(T, U, 70.0, 95.0)
    print(f"[样条拐点法] Tc = {Tc_s:.2f} °C,  (dU/dT)min = {slope:.3f} mV/°C")

    best = None
    for Tc0 in (74.0, 76.0, 78.0, 80.0, 82.0):
        for w0 in (1.0, 2.0, 3.0):
            try:
                p, _ = curve_fit(model, T, U, p0=[2.0, 30.0, Tc0, w0, 0.0])
            except RuntimeError:
                continue
            r = float(np.sum((model(T, *p) - U) ** 2))
            if best is None or r < best[0]:
                best = (r, p)
    rss, p = best
    U_para, A, Tc_f, w, k = p
    print(f"[四参数拟合] Tc = {Tc_f:.2f} °C, 基线 {U_para:.2f} mV, 台阶 {A:.2f} mV, 宽度 {w:.2f} °C")
    print(f"             残差 RSS = {rss:.2f} mV^2, RMSE = {np.sqrt(rss / len(T)):.3f} mV")

    # 降温曲线缺失，无法做升/降温差值修正：以样条法为测量值，拟合值作为方法差
    sys_diff = abs(Tc_f - Tc_s)
    print(f"[方法差异] |拐点(样条) - 拟合| = {sys_diff:.2f} °C")

    # 分段 A 类：把居里区间的数据分段做拐点，看 Tc 的分散度
    tcs = []
    for lo, hi in [(68, 95), (70, 95), (72, 95), (70, 98), (72, 98), (70, 92)]:
        m = (T >= lo) & (T <= hi)
        if m.sum() < 10:
            continue
        tc, _ = inflection_spline(T[m], U[m], lo, hi)
        tcs.append(tc)
    tcs = np.array(tcs)
    uA = tcs.std(ddof=1)
    print(f"[分段稳健性] Tc = {np.round(tcs, 2)} → s = {uA:.2f} °C")

    uB_T = 0.5 / np.sqrt(3)      # 温控仪控温精度 0.5 °C，均匀分布
    uB_U = 0.1 / np.sqrt(3)      # 电压表最小分辨率 0.1 mV，均匀分布
    # 电压分辨极限通过斜率折算成温度：uT(U) = uU / |dU/dT|
    uB = np.hypot(uB_T, uB_U / abs(slope))
    u = np.hypot(uA, uB)
    print(f"[不确定度] uA = {uA:.2f}, uB = {uB:.2f} (含 ΔT 项 {uB_T:.2f}, ΔU 项 {uB_U / abs(slope):.3f}) → u = {u:.2f} °C")
    print(f"\n结果：  Tc = ({Tc_s:.1f} ± {u:.1f}) °C   (参考值 78 °C，相对偏差 {abs(Tc_s - 78) / 78 * 100:.1f}%)")

    plot(T, U, Tc_s, Tc_f, p)


def plot(T, U, Tc_s, Tc_f, p) -> None:
    import matplotlib
    matplotlib.rcParams["font.sans-serif"] = ["SimHei", "DejaVu Sans"]
    matplotlib.rcParams["axes.unicode_minus"] = False
    matplotlib.rcParams["xtick.direction"] = "in"
    matplotlib.rcParams["ytick.direction"] = "in"
    matplotlib.rcParams["savefig.dpi"] = 300
    import matplotlib.pyplot as plt

    FIGDIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5), layout="constrained")
    ax.plot(T, U, "o", ms=4, color="#E74C3C", label="升温实测数据", zorder=5)
    grid = np.linspace(70, 120, 400)
    ax.plot(grid, model(grid, *p), "-", lw=1.6, color="#2980B9", label="四参数光滑拟合")
    ax.axvline(Tc_s, color="#27AE60", ls="--", lw=1.4)
    ax.annotate(f"$T_C$ = {Tc_s:.1f} °C", xy=(Tc_s, 30), xytext=(Tc_s + 3, 33),
                color="#27AE60", arrowprops=dict(arrowstyle="->", color="#27AE60", lw=1.2))
    ax.set_xlabel("温度 $T$ / °C")
    ax.set_ylabel("交流电桥输出电压 $U$ / mV")
    ax.set_title("铁氧体样品升温 $U$–$T$ 曲线（拐点法确定居里温度）")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.savefig(FIGDIR / "UT_heating.pdf")
    fig.savefig(FIGDIR / "UT_heating.png")

    spl = UnivariateSpline(T, U, k=3, s=len(T) * 0.05)
    g = np.linspace(70, 95, 2000)
    fig2, ax2 = plt.subplots(figsize=(8, 4.5), layout="constrained")
    ax2.plot(g, spl.derivative(1)(g), lw=1.6, color="#8E44AD")
    ax2.axvline(Tc_s, color="#27AE60", ls="--", lw=1.4, label=f"拐点 $T_C$ = {Tc_s:.1f} °C")
    ax2.set_xlabel("温度 $T$ / °C")
    ax2.set_ylabel("$\\mathrm{d}U/\\mathrm{d}T$ / (mV·°C$^{-1}$)")
    ax2.set_title("$U$–$T$ 曲线的斜率及拐点（斜率绝对值最大处）")
    ax2.grid(alpha=0.3)
    ax2.legend()
    fig2.savefig(FIGDIR / "dU_dT.pdf")
    fig2.savefig(FIGDIR / "dU_dT.png")
    print(f"\n图已保存至 {FIGDIR}")


if __name__ == "__main__":
    main()
