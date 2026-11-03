"""
不确定度计算便捷函数

封装 uncertainties 库，提供物理实验中常用的不确定度计算工具。
使用方式：
    from utils.uncertainty import u, u_result, type_a_uncertainty
"""

from uncertainties import ufloat, umath
import numpy as np


def u(value: float, uncertainty: float):
    """
    创建带不确定度的测量值（ufloat 的简写）。

    Parameters
    ----------
    value : float
        测量值。
    uncertainty : float
        不确定度。

    Returns
    -------
    UFloat
        带不确定度的浮点数。

    Examples
    --------
    >>> L = u(25.30, 0.03)  # L = (25.30 ± 0.03) mm
    >>> print(L)
    25.30+/-0.03
    """
    return ufloat(value, uncertainty)


def u_result(x, unit: str = "", precision: int = 2) -> str:
    """
    格式化带不确定度的结果表达式。

    Parameters
    ----------
    x : UFloat
        带不确定度的测量值。
    unit : str
        单位字符串，如 'mm', 'V', 'Ω'。
    precision : int
        不确定度的有效位数，默认 2。

    Returns
    -------
    str
        格式化的结果字符串，如 'L = (25.30 ± 0.03) mm'。

    Examples
    --------
    >>> L = u(25.30, 0.03)
    >>> u_result(L, 'mm')
    '25.30 ± 0.03 mm'
    """
    val = x.nominal_value
    err = x.std_dev

    if err == 0:
        if unit:
            return f"{val:.6f} {unit}"
        return f"{val:.6f}"

    # 根据不确定度确定小数位数
    err_str = f"{err:.{precision}g}"
    # 计算小数位数
    if "." in err_str:
        decimals = len(err_str.split(".")[1])
    else:
        decimals = 0

    val_str = f"{val:.{decimals}f}"

    result = f"{val_str} ± {err_str}"
    if unit:
        result += f" {unit}"
    return result


def type_a_uncertainty(data: np.ndarray) -> tuple[float, float, float]:
    """
    计算 A 类不确定度（统计不确定度）。

    Parameters
    ----------
    data : np.ndarray
        等精度测量数据数组。

    Returns
    -------
    tuple[float, float, float]
        (平均值, 样本标准差, A类不确定度)

    Notes
    -----
    - 平均值: x̄ = (1/n) Σxᵢ
    - 样本标准差: s = √[1/(n-1) Σ(xᵢ - x̄)²]
    - A 类不确定度: uA = s / √n

    Examples
    --------
    >>> data = np.array([25.32, 25.28, 25.30, 25.34, 25.26])
    >>> mean, std, uA = type_a_uncertainty(data)
    >>> print(f"x̄ = {mean:.4f}, s = {std:.4f}, uA = {uA:.4f}")
    """
    n = len(data)
    mean = np.mean(data)
    std = np.std(data, ddof=1)  # 样本标准差 (Bessel 校正)
    uA = std / np.sqrt(n)
    return float(mean), float(std), float(uA)


def type_b_uncertainty(instrument_limit: float, confidence: str = "normal") -> float:
    """
    计算 B 类不确定度（仪器不确定度）。

    Parameters
    ----------
    instrument_limit : float
        仪器的最大允许误差（分度值的一半或精度等级对应的误差限）。
    confidence : str
        置信分布类型：
        - 'normal': 正态分布 (除以 3)
        - 'uniform': 均匀分布 (除以 √3)，默认适用于大多数指针式仪表
        - 'triangular': 三角分布 (除以 √6)

    Returns
    -------
    float
        B 类不确定度。

    Examples
    --------
    >>> # 游标卡尺分度值 0.02mm，误差限 = 0.02/2 = 0.01mm
    >>> uB = type_b_uncertainty(0.01, 'uniform')
    >>> print(f"uB = {uB:.4f} mm")
    """
    divisors = {
        "normal": 3.0,
        "uniform": np.sqrt(3),
        "triangular": np.sqrt(6),
    }
    if confidence not in divisors:
        raise ValueError(f"confidence 必须是 {list(divisors.keys())} 之一")

    return instrument_limit / divisors[confidence]


def combined_uncertainty(uA: float, uB: float) -> float:
    """
    计算合成不确定度。

    Parameters
    ----------
    uA : float
        A 类不确定度。
    uB : float
        B 类不确定度。

    Returns
    -------
    float
        合成标准不确定度 u = √(uA² + uB²)
    """
    return np.sqrt(uA**2 + uB**2)
