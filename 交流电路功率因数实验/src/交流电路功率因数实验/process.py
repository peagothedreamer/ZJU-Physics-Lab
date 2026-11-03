"""交流电路功率因数实验：cosφ 计算、最佳电容拟合与作图。

运行：
    f:/desktop/PHYLAB/.venv/Scripts/python.exe src/交流电路功率因数实验/process.py

输出：
    Template/figures/cosphi_vs_C.pdf
    Template/figures/current_vs_C.pdf
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / "Template" / "figures"

matplotlib.rcParams.update(
    {
        "font.sans-serif": ["SimHei", "Microsoft YaHei"],
        "axes.unicode_minus": False,
        "font.size": 10,
        "axes.linewidth": 0.8,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.top": True,
        "ytick.right": True,
        "legend.frameon": False,
        "figure.dpi": 150,
    }
)

# C / μF, I / mA, U / V, P / W
# 45 Hz 的 2.645 μF 按原始记录修正（数据表误记为 2.695 μF）。
# 55 Hz 的 3.242 μF 一组在原始记录中作废，重测为 3.517 μF，故不计入。
DATA = {
    45: (
        np.array([0, 0.931, 1.714, 2.645, 3.412, 4.343, 5.089, 6.020, 6.925]),
        np.array([371.4, 314.5, 272.1, 228.5, 196.4, 170.2, 161.4, 169.9, 194.6]),
        np.array([219.4, 219.6, 219.8, 220.0, 220.3, 220.5, 220.6, 220.6, 220.1]),
        np.array([29.7, 30.3, 30.6, 30.8, 31.1, 31.3, 31.7, 31.5, 31.4]),
    ),
    50: (
        np.array([0, 0.931, 1.714, 2.645, 3.412, 4.343, 5.089, 6.020, 6.925]),
        np.array([297.7, 240.6, 196.7, 152.5, 130.1, 129.3, 151.6, 194.6, 247.1]),
        np.array([219.0, 219.4, 219.4, 220.1, 219.7, 219.6, 219.3, 219.0, 219.2]),
        np.array([24.8, 24.9, 24.9, 25.0, 25.2, 25.0, 25.2, 25.1, 25.2]),
    ),
    55: (
        np.array([0, 0.803, 1.773, 3.517, 4.320, 5.153, 5.956]),
        np.array([250.9, 189.1, 134.3, 106.9, 146.6, 193.8, 253.6]),
        np.array([218.4, 218.7, 218.5, 217.5, 217.7, 217.6, 217.6]),
        np.array([19.6, 20.1, 20.2, 20.3, 20.5, 20.3, 20.5]),
    ),
}

STYLE = {
    45: ("#2980B9", "o"),
    50: ("#E74C3C", "s"),
    55: ("#27AE60", "^"),
}


def cosphi(I_mA, U, P):
    return P / (U * I_mA * 1e-3)


def quadratic_vertex(C, y):
    """过最优点及相邻两点作抛物线，返回顶点横坐标。"""
    k = int(np.argmax(y))
    lo, hi = max(k - 1, 0), min(k + 1, len(C) - 1)
    p = np.polyfit(C[lo : hi + 1], y[lo : hi + 1], 2)
    return -p[1] / (2 * p[0])


def b_type(resolution):
    """均匀分布假设下的 B 类不确定度。"""
    return resolution / np.sqrt(3)


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    summary = {}

    for f, (C, I, U, P) in DATA.items():
        c = cosphi(I, U, P)
        k = int(np.argmax(c))
        c_opt = quadratic_vertex(C, c)
        phi0 = np.arccos(c[0])
        c_theory = P[0] * np.tan(phi0) / (2 * np.pi * f * U[0] ** 2) * 1e6

        # cosφ 的 B 类不确定度：按 U 0.1 V、I 0.1 mA、P 0.1 W 的分辨力估计
        u_c = c[k] * np.sqrt(
            (b_type(0.1) / P[k]) ** 2
            + (b_type(0.1) / U[k]) ** 2
            + (b_type(0.1) / I[k]) ** 2
        )

        summary[f] = dict(c=c, k=k, c_opt=c_opt, c_theory=c_theory, u_c=u_c)

        print(f"\n=== f = {f} Hz ===")
        for ci, ii, ui, pi, si in zip(C, I, U, P, c):
            print(f"{ci:6.3f} & {ii:6.1f} & {ui:6.1f} & {pi:5.1f} & {si:.4f} \\\\")
        print(
            f"cosφ_max = {c[k]:.4f} @ {C[k]:.3f} μF; "
            f"抛物线顶点 {c_opt:.3f} μF; "
            f"理论值 {c_theory:.3f} μF; "
            f"相对偏差 {(c_opt - c_theory) / c_theory * 100:+.1f}%"
        )
        print(f"cosφ = {c[k]:.4f} ± {u_c:.4f}")

    # ---------------------------------------------------------- cosφ–C
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    for f, (C, I, U, P) in DATA.items():
        c = cosphi(I, U, P)
        color, marker = STYLE[f]
        ax.plot(C, c, color=color, marker=marker, ms=4.5, lw=1.2, label=f"{f} Hz")
        k = summary[f]["k"]
        ax.plot(C[k], c[k], marker="*", ms=11, color=color, mec="k", mew=0.4, zorder=5)
    ax.set_xlabel("$C$ / μF")
    ax.set_ylabel(r"$\cos\varphi$")
    ax.set_xlim(0, 7.3)
    ax.set_ylim(0.30, 0.95)
    ax.grid(alpha=0.25)
    ax.legend(title="频率", loc="lower right")
    fig.tight_layout()
    fig.savefig(FIG / "cosphi_vs_C.pdf")
    fig.savefig(FIG / "cosphi_vs_C.png")
    plt.close(fig)

    # ---------------------------------------------------------- I–C
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    for f, (C, I, U, P) in DATA.items():
        color, marker = STYLE[f]
        ax.plot(C, I, color=color, marker=marker, ms=4.5, lw=1.2, label=f"{f} Hz")
    ax.set_xlabel("$C$ / μF")
    ax.set_ylabel("$I$ / mA")
    ax.set_xlim(0, 7.3)
    ax.grid(alpha=0.25)
    ax.legend(title="频率", loc="upper right")
    fig.tight_layout()
    fig.savefig(FIG / "current_vs_C.pdf")
    fig.savefig(FIG / "current_vs_C.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
