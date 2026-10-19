"""居里温度估计方法的稳健性对比

目的：区分「数据本身的信息量」与「估计方法引入的偏差」，
判断哪些误差可以通过数据处理减小，哪些不能。

运行：..\..\..\.venv\Scripts\python.exe compare_methods.py
"""

import re
from pathlib import Path

import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter

HERE = Path(__file__).resolve().parent


def load() -> tuple[np.ndarray, np.ndarray]:
    raw = re.search(r'RAW = """(.*?)"""', (HERE / "process.py").read_text(encoding="utf-8"), re.S).group(1)
    nums = np.array(raw.split(), dtype=float)
    T, U = nums[0::2], nums[1::2]
    o = np.argsort(T)
    return T[o], U[o]


def spline_inflection(T, U, s, lo=70.0, hi=95.0, n=20001):
    spl = UnivariateSpline(T, U, k=3, s=s)
    g = np.linspace(lo, hi, n)
    d1, d2 = spl.derivative(1)(g), spl.derivative(2)(g)
    i = int(np.argmin(d1))
    for j in range(max(i - 1, 0), min(i + 1, n - 1)):
        if d2[j] * d2[j + 1] < 0:
            f = d2[j] / (d2[j] - d2[j + 1])
            return float(g[j] + f * (g[1] - g[0])), float(d1[i])
    return float(g[i]), float(d1[i])


def uniform(T, U, step=0.1):
    g = np.arange(T[0], T[-1] + step / 2, step)
    return g, UnivariateSpline(T, U, k=3, s=len(T) * 0.05)(g)


def savgol_peak(T, U, win, poly=3, lo=70.0, hi=95.0):
    g, u = uniform(T, U)
    w = win if win % 2 else win + 1
    d1 = savgol_filter(u, w, poly, deriv=1, delta=g[1] - g[0])
    m = (g >= lo) & (g <= hi)
    i = int(np.argmin(np.where(m, d1, np.inf)))
    return float(g[i]), float(d1[i])


def critical_fit(T, U, lo=65.0, hi=98.0):
    """临界律 U = U0 + A(1-T/Tc)^beta（T<Tc）并在 T>Tc 接线性基线。"""
    m = (T >= lo) & (T <= hi)
    t, u = T[m], U[m]

    def f(x, U0, A, Tc, beta, k):
        r = 1.0 - x / Tc
        # 平滑过渡，避免 max() 不可导
        soft = 0.5 * (1.0 - np.tanh(r * 40.0))
        return U0 + A * np.abs(np.clip(r, 0, None)) ** beta * soft + k * (x - Tc) * (1 - soft)

    best = None
    for Tc0 in (79.0, 81.0, 83.0, 85.0):
        for b0 in (0.3, 0.5):
            try:
                p, _ = curve_fit(f, t, u, p0=[6.0, 30.0, Tc0, b0, -0.1],
                                 bounds=([-20, 0, 60, 0.05, -1], [40, 80, 100, 1.5, 1]),
                                 maxfev=40000)
            except RuntimeError:
                continue
            r = float(np.sum((f(t, *p) - u) ** 2))
            if best is None or r < best[0]:
                best = (r, p)
    if best is None:
        return None
    rss, p = best
    return dict(Tc=p[2], U0=p[0], A=p[1], beta=p[3], k=p[4], rmse=float(np.sqrt(rss / len(t))))


def windowed_logistic(T, U, lo, hi):
    m = (T >= lo) & (T <= hi)
    t, u = T[m], U[m]

    def f(x, U0, A, Tc, w, k):
        z = (x - Tc) / w
        g = 1.0 / (1.0 + np.exp(z))
        return U0 + A * g + k * (x - 100.0) / 20.0 * g

    best = None
    for Tc0 in (78.0, 80.0, 82.0, 84.0):
        for w0 in (1.5, 2.5, 4.0):
            try:
                p, _ = curve_fit(f, t, u, p0=[5.0, 32.0, Tc0, w0, 0.0], maxfev=40000)
            except RuntimeError:
                continue
            r = float(np.sum((f(t, *p) - u) ** 2))
            if best is None or r < best[0]:
                best = (r, p)
    rss, p = best
    return dict(Tc=p[2], U0=p[0], A=p[1], w=p[3], rmse=float(np.sqrt(rss / len(t))))


def main() -> None:
    T, U = load()
    n = len(T)
    print(f"数据 {n} 点，T ∈ [{T[0]:.1f}, {T[-1]:.1f}] °C，电压量化步长 0.1 mV\n")

    print("【1】样条平滑参数对拐点位置的影响（s = 平滑权重, s=0 为严格插值）")
    print(f"{'s':>8} {'Tc/°C':>8} {'|dU/dT|max':>11}")
    for s in [0.0, 0.5, 1.0, 2.0, 5.0, n * 0.05, n * 0.2, n * 0.5]:
        tc, d = spline_inflection(T, U, s)
        print(f"{s:>8.1f} {tc:>8.2f} {abs(d):>11.3f}")

    print("\n【2】Savitzky–Golay 导数峰值（先插值到 0.1 °C 均匀网格）")
    print(f"{'窗宽':>6} {'Tc/°C':>8} {'|dU/dT|max':>11}")
    tcs = []
    for w in [5, 7, 9, 11, 13, 17]:
        tc, d = savgol_peak(T, U, w)
        tcs.append(tc)
        print(f"{w:>6} {tc:>8.2f} {abs(d):>11.3f}")
    print(f"   → 窗宽引起的方法散布 s = {np.std(tcs, ddof=1):.2f} °C")

    print("\n【3】原始差分（不做任何平滑）——检查数据本身最陡处")
    dU = np.diff(U) / np.diff(T)
    mid = 0.5 * (T[1:] + T[:-1])
    m = (mid >= 70) & (mid <= 95)
    idx = np.argsort(-np.abs(dU[m]))[:6]
    for i in sorted(idx):
        print(f"   T ≈ {mid[m][i]:>5.2f} °C   dU/dT = {dU[m][i]:>7.3f} mV/°C")

    print("\n【4】四参数 logistic 拟合：区间选择的影响")
    print(f"{'区间/°C':>14} {'Tc/°C':>8} {'U0/mV':>7} {'w/°C':>6} {'RMSE':>7}")
    res = []
    for lo, hi in [(60, 120), (70, 120), (70, 110), (70, 100), (65, 120), (72, 120), (70, 95)]:
        r = windowed_logistic(T, U, lo, hi)
        res.append(r["Tc"])
        print(f"{f'{lo}–{hi}':>14} {r['Tc']:>8.2f} {r['U0']:>7.2f} {r['w']:>6.2f} {r['rmse']:>7.3f}")
    print(f"   → 区间引起的方法散布 s = {np.std(res, ddof=1):.2f} °C")

    print("\n【5】临界律拟合 U = U0 + A(1-T/Tc)^β（物理上更贴近相变）")
    for lo, hi in [(70, 120), (65, 120), (70, 100)]:
        r = critical_fit(T, U, lo, hi)
        if r:
            print(f"   {lo}–{hi} °C: Tc = {r['Tc']:.2f} °C, β = {r['beta']:.3f}, "
                  f"U0 = {r['U0']:.2f} mV, RMSE = {r['rmse']:.3f} mV")

    print("\n【6】不确定度分解（以样条拐点法 s=n*0.05 为基准）")
    tc0, slope = spline_inflection(T, U, n * 0.05)
    uA_method = float(np.std([spline_inflection(T, U, s)[0]
                              for s in [n * 0.02, n * 0.05, n * 0.1, n * 0.2]], ddof=1))
    uB_T = 0.5 / np.sqrt(3)          # 温控仪控温精度 0.5 °C
    uB_U = (0.1 / np.sqrt(12)) / abs(slope)   # 量化误差 0.1 mV，均匀分布
    print(f"   基准 Tc          = {tc0:.2f} °C")
    print(f"   方法散布 u_method= {uA_method:.2f} °C   ← 可借选法/取平均压缩")
    print(f"   测温 B 类 u_B,T  = {uB_T:.2f} °C   ← 仪器指标，不可压缩")
    print(f"   量化 B 类 u_B,U  = {uB_U:.3f} °C  ← 已可忽略")
    print(f"   量化极限 dT = 0.1/|dU/dT|   = {0.1 / abs(slope):.3f} °C/字")


if __name__ == "__main__":
    main()
