"""
物理实验绘图样式配置

提供中文字体配置与统一的绘图样式，确保生成的图表与 LaTeX 报告风格一致。
使用方式：
    from utils.plotting import setup_physics_plot, save_figure
    setup_physics_plot()
"""

import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path


def setup_physics_plot(
    font_family: str = "SimHei",
    font_size: int = 12,
    use_qt_backend: bool = False,
) -> None:
    """
    配置 matplotlib 中文字体与物理实验绘图样式。

    Parameters
    ----------
    font_family : str
        中文字体名称，默认 'SimHei'（黑体）。
        Windows 系统可选：'SimHei'（黑体）、'KaiTi'（楷体）、'SimSun'（宋体）。
    font_size : int
        全局字体大小，默认 12。
    use_qt_backend : bool
        是否使用 Qt 交互式后端（需安装 PyQt6），默认 False。
    """
    if use_qt_backend:
        matplotlib.use("QtAgg")

    # 中文字体配置
    matplotlib.rcParams["font.sans-serif"] = [font_family, "DejaVu Sans"]
    matplotlib.rcParams["axes.unicode_minus"] = False  # 正确显示负号

    # 全局字体大小
    matplotlib.rcParams["font.size"] = font_size

    # 刻度样式
    matplotlib.rcParams["xtick.direction"] = "in"
    matplotlib.rcParams["ytick.direction"] = "in"
    matplotlib.rcParams["xtick.major.size"] = 5
    matplotlib.rcParams["ytick.major.size"] = 5
    matplotlib.rcParams["xtick.minor.size"] = 3
    matplotlib.rcParams["ytick.minor.size"] = 3

    # 线条样式
    matplotlib.rcParams["axes.linewidth"] = 1.0
    matplotlib.rcParams["lines.linewidth"] = 1.5
    matplotlib.rcParams["lines.markersize"] = 6

    # 图例样式
    matplotlib.rcParams["legend.framealpha"] = 0.8
    matplotlib.rcParams["legend.edgecolor"] = "0.8"

    # 保存质量
    matplotlib.rcParams["savefig.dpi"] = 300
    matplotlib.rcParams["savefig.bbox"] = "tight"
    matplotlib.rcParams["savefig.pad_inches"] = 0.05


def save_figure(
    fig: plt.Figure,
    filename: str,
    output_dir: str | Path = "figures",
    formats: list[str] | None = None,
) -> list[Path]:
    """
    保存图表为指定格式，默认保存 PDF（矢量图，供 LaTeX 引用）和 PNG（预览用）。

    Parameters
    ----------
    fig : plt.Figure
        要保存的 matplotlib Figure 对象。
    filename : str
        文件名（不含扩展名），如 'UI_curve'。
    output_dir : str | Path
        输出目录，默认 'figures'。
    formats : list[str] | None
        输出格式列表，默认 ['pdf', 'png']。

    Returns
    -------
    list[Path]
        保存的文件路径列表。
    """
    if formats is None:
        formats = ["pdf", "png"]

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    saved = []
    for fmt in formats:
        path = output_dir / f"{filename}.{fmt}"
        fig.savefig(path, format=fmt)
        saved.append(path)

    return saved


# 预定义的物理实验配色方案
PHYSICS_COLORS = {
    "red": "#E74C3C",
    "blue": "#2980B9",
    "green": "#27AE60",
    "orange": "#E67E22",
    "purple": "#8E44AD",
    "dark": "#2C3E50",
    "gray": "#7F8C8D",
}

# 实验常用标记样式
MARKER_STYLES = ["o", "s", "^", "D", "v", "p", "h", "*"]
