# src/ — 物理实验数据处理 Python 环境

本目录用于存放物理实验课程中数据处理、绘图、拟合等 Python 脚本。

---

## 🐍 Python 虚拟环境

- **Python 版本**: `3.13`（系统安装，位于 `C:\Users\peago\AppData\Local\Programs\Python\Python313`）
- **虚拟环境**: **项目父目录**下 `../.venv/`（与 `Phy_lab` 同级，使用 `venv` 模块，**不使用 conda**）
- **依赖定义文件**: `requirements.txt`（位于本目录下）

---

## 📦 所需 Python 模块

以下为大物实验课数据处理常用的 Python 模块：

| 模块 | 用途 |
| --- | --- |
| **numpy** | 数值计算、数组运算、统计量计算 |
| **scipy** | 科学计算（曲线拟合 `curve_fit`、插值、积分等） |
| **matplotlib** | 绘图（B-x 曲线、磁滞回线、拟合直线等） |
| **PyQt6** | matplotlib 的 Qt 后端（交互式绘图窗口） |
| **pandas** | 表格数据读写与处理 |
| **openpyxl** | 读写 Excel 文件（`.xlsx`） |
| **pillow** | 图片处理（裁剪原始数据扫描件等） |
| **sympy** | 符号计算（公式推导、不确定度表达式化简） |
| **uncertainties** | 不确定度传递与误差计算 |
| **lmfit** | 高级曲线拟合（比 scipy 更灵活的参数约束） |

---

## 🔧 手动环境创建（面向人类用户）

### 方式一：使用 `requirements.txt` 一键安装（推荐）

```powershell
# 1. 在项目父目录创建虚拟环境
python -m venv ..\.venv

# 2. 激活虚拟环境（PowerShell）
..\.venv\Scripts\Activate.ps1

# 3. 安装所有依赖
pip install -r src\requirements.txt
```

> **CMD 用户**：激活命令为 `..\.venv\Scripts\activate.bat`
> **Git Bash 用户**：激活命令为 `source ../.venv/Scripts/activate`

### 方式二：手动逐个安装

```powershell
# 1. 创建并激活虚拟环境（同上）
python -m venv ..\.venv
..\.venv\Scripts\Activate.ps1

# 2. 安装所有包
pip install numpy scipy matplotlib pandas pillow PyQt6 sympy openpyxl uncertainties lmfit
```

### 常用环境管理命令

```powershell
..\.venv\Scripts\Activate.ps1  # 激活虚拟环境
deactivate                     # 退出虚拟环境

# 如需重建环境
rm -r ..\.venv                 # 删除旧环境
python -m venv ..\.venv        # 重新创建
..\.venv\Scripts\Activate.ps1
pip install -r src\requirements.txt
```

---

## 🤖 AI Agent 工作流指引

> **本节面向 Claude / Codex / Gemini 等 AI 编程助手。**
> 当你需要运行 `src/` 目录下的 Python 脚本时，请严格按照以下流程操作。

### 步骤 0：先确认用户要用的 Python 解释器（必须）

在执行任何 `python` 之前，先向用户确认使用哪一种方式运行脚本：

- **推荐**：使用本项目的 venv 环境（项目根目录 `.venv`）
- **可选**：使用用户已有的其他 venv/解释器路径（给出 `python` 的绝对路径）

确认后，用一个变量在后续步骤中统一表示"Python 运行命令"：

```powershell
# 例 1：项目推荐 venv 环境（推荐）
PYTHON_RUN='.venv\Scripts\python.exe'

# 例 2：用户自定义解释器路径
# PYTHON_RUN='<ABSOLUTE_PATH_TO_PYTHON>'
```

> 若用户不确定或未提供信息：默认先询问是否使用项目 venv；只有用户明确同意后才继续。

### 总体流程图

```
开始
 │
 ▼
[步骤 0] 询问并确认 Python 解释器 / venv
 │
 ▼
[步骤 1] 检测项目 venv 是否存在
 │
 ├── 不存在 → 询问用户"未检测到 .venv，是否为您创建？"
 │             ├── 用户确认 → 跳到 [步骤 3]
 │             └── 用户拒绝 → 停止
 │
 ▼
[步骤 2] 检测 venv 中依赖是否齐全
 │
 ├── 缺失依赖 → 询问用户"是否为您安装缺失的依赖？"
 │             ├── 用户确认 → 安装缺失依赖
 │             └── 用户拒绝 → 告知风险后继续
 │
 ▼
[步骤 3] 验证关键模块是否可用
 │
 ├── 缺少模块 → 询问用户"发现缺失模块 xxx，是否安装？"
 │             ├── 用户确认 → 安装缺失模块
 │             └── 用户拒绝 → 告知风险后继续
 │
 ▼
[步骤 4] 运行 Python 脚本
 │
 ▼
[步骤 5] 检查输出与结果
```

---

### 步骤 1：检测项目 venv 是否存在

运行以下命令：

```powershell
test -d .venv && echo "VENV_EXISTS" || echo "VENV_NOT_FOUND"
```

- **`VENV_EXISTS`**：继续步骤 2。
- **`VENV_NOT_FOUND`**：
  - 向用户询问：> "❌ 未检测到项目虚拟环境 `.venv`。是否为您创建？（创建过程可能需要几分钟）"
  - 用户确认 → 进入步骤 3
  - 用户拒绝 → **停止执行**

---

### 步骤 2：检测 venv 依赖是否齐全

```powershell
.venv\Scripts\pip.exe list
```

检查输出中是否包含所需的包。如果缺失较多，建议直接重新安装全部依赖：

```powershell
.venv\Scripts\pip.exe install -r src\requirements.txt
```

---

### 步骤 3：创建 venv 并安装依赖

```powershell
# 1. 创建虚拟环境
python -m venv .venv

# 2. 安装依赖
.venv\Scripts\pip.exe install -r src\requirements.txt
```

创建完成后，向用户报告：
> ✅ 虚拟环境创建完成！已安装以下模块：numpy, scipy, matplotlib, pandas, pillow, PyQt6, sympy, openpyxl, uncertainties, lmfit。

---

### 步骤 4：验证关键模块可用性

运行以下验证命令：

```powershell
.venv\Scripts\python.exe -c "
modules = {
    'numpy': 'numpy',
    'scipy': 'scipy',
    'matplotlib': 'matplotlib',
    'pandas': 'pandas',
    'sympy': 'sympy',
    'openpyxl': 'openpyxl',
    'uncertainties': 'uncertainties',
    'lmfit': 'lmfit',
    'PIL': 'pillow',
}
missing = []
for mod, pkg in modules.items():
    try:
        __import__(mod)
    except ImportError:
        missing.append(pkg)
if missing:
    print('MISSING:' + ','.join(missing))
else:
    print('ALL_OK')
"
```

- **输出 `ALL_OK`**：所有模块就绪，进入步骤 5。
- **输出 `MISSING:xxx,yyy`**：向用户报告缺失的模块并询问：
  > ⚠️ 以下模块缺失：`xxx`, `yyy`。是否为您安装？

  用户确认后安装：
  ```powershell
  .venv\Scripts\pip.exe install xxx yyy
  ```

---

### 步骤 5：运行 Python 脚本

使用"步骤 0"中确认的 `PYTHON_RUN` 来执行脚本：

```powershell
$PYTHON_RUN <脚本的绝对路径>
```

> **⚠️ 重要**：运行脚本时始终使用 `.venv\Scripts\python.exe` 或绝对路径，不要依赖 `python` 全局命令（可能指向不同版本）。

---

### 步骤 6：检查输出与结果

运行结束后：

1. **检查退出码**：
   - 退出码 `0` = 成功
   - 非零退出码 = 出错，需分析 stderr 输出
2. **如果生成了图片文件**：告知用户保存路径，并询问是否需要在 LaTeX 报告中引用
3. **如果运行出错**：
   - 分析报错信息
   - 向用户展示错误原因和修复建议
   - 询问用户：`"是否需要我帮您修复这个问题？"`

---

## ⚠️ Agent 注意事项

1. **绝对路径**：运行脚本和保存文件时都用绝对路径，避免工作目录不一致导致的路径问题。
2. **中文绘图字体**：如果脚本生成含中文的图表，需在脚本开头配置 matplotlib 字体：
   ```python
   import matplotlib
   matplotlib.rcParams['font.sans-serif'] = ['SimHei']
   matplotlib.rcParams['axes.unicode_minus'] = False
   ```
3. **图片输出格式**：推荐保存为 PDF 格式（矢量图），便于 LaTeX 引用。
4. **主动询问**：在执行任何可能修改系统状态的操作（安装包、创建文件）前，务必先向用户确认。
5. **Windows 路径**：本项目运行于 Windows，路径分隔符使用 `\`（PowerShell/CMD）或 `/`（Git Bash 均可）。

---

## 📂 推荐目录结构

```
src/
├── README.md              # 本说明文件（你正在读的）
├── requirements.txt       # pip 依赖定义文件
├── utils/                 # 公共工具函数
│   ├── __init__.py
│   ├── uncertainty.py     # 不确定度计算工具
│   └── plotting.py        # 绘图样式配置
└── 实验名称/              # 每个实验一个子目录
    ├── data/              # 原始数据（csv / xlsx）
    ├── figures/           # 生成的图片（供 LaTeX 引用）
    └── process.py         # 数据处理脚本
```

---

## 💡 常用代码片段

### 1. 基本数据处理与绘图

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 测量数据
x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
y = np.array([5.2, 10.3, 15.1, 20.4, 25.0])

# 线性拟合
coeffs = np.polyfit(x, y, 1)
y_fit = np.polyval(coeffs, x)

plt.figure(figsize=(8, 5))
plt.scatter(x, y, color='red', label='实验数据', zorder=5)
plt.plot(x, y_fit, 'b--', label=f'拟合: y = {coeffs[0]:.2f}x + {coeffs[1]:.2f}')
plt.xlabel('U / V')
plt.ylabel('I / mA')
plt.title('U-I 特性曲线')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('figures/UI_curve.pdf', dpi=300)
plt.show()
```

### 2. 不确定度计算

```python
from uncertainties import ufloat
import numpy as np

# 带不确定度的测量值
L = ufloat(25.30, 0.03)   # mm
d = ufloat(10.02, 0.02)   # mm

# 运算中自动传递不确定度
area = np.pi * (d / 2) ** 2
volume = area * L

print(f"体积 V = {volume:.2uP}")   # 自动输出 值 ± 不确定度
```

### 3. scipy 曲线拟合

```python
from scipy.optimize import curve_fit
import numpy as np

def model(x, a, b):
    """线性模型 y = ax + b"""
    return a * x + b

x_data = np.array([1, 2, 3, 4, 5])
y_data = np.array([2.1, 3.9, 6.2, 7.8, 10.1])

popt, pcov = curve_fit(model, x_data, y_data)
perr = np.sqrt(np.diag(pcov))  # 参数标准误差

print(f"a = {popt[0]:.4f} ± {perr[0]:.4f}")
print(f"b = {popt[1]:.4f} ± {perr[1]:.4f}")
```
