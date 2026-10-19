# src/ — 物理实验数据处理 Python 环境

本目录用于存放物理实验课程中数据处理、绘图、拟合等 Python 脚本。

---

## 🐍 Conda 虚拟环境

- **环境名称**: `phylab`
- **Python 版本**: `3.10`
- **环境定义文件**: `environment.yml`（位于本目录下）

---

## 📦 所需 Python 模块

以下为大物实验课数据处理常用的 Python 模块：

| 模块 | 用途 | 安装来源 |
| --- | --- | --- |
| **numpy** | 数值计算、数组运算、统计量计算 | conda |
| **scipy** | 科学计算（曲线拟合 `curve_fit`、插值、积分等） | conda |
| **matplotlib** | 绑图（B-x 曲线、磁滞回线、拟合直线等） | conda |
| **pandas** | 表格数据读写与处理 | conda |
| **pillow** | 图片处理（裁剪原始数据扫描件等） | conda |
| **PyQt6** | matplotlib 的 Qt 后端（交互式绘图窗口） | conda |
| **uncertainties** | 不确定度传递与误差计算 | pip |
| **sympy** | 符号计算（公式推导、不确定度表达式化简） | conda |
| **openpyxl** | 读写 Excel 文件（`.xlsx`） | conda |
| **lmfit** | 高级曲线拟合（比 scipy 更灵活的参数约束） | pip |

---

## 🔧 手动环境创建（面向人类用户）

### 方式一：使用 `environment.yml` 一键创建（推荐）

```bash
# 创建环境（首次）
conda env create -f environment.yml

# 更新环境（environment.yml 修改后）
conda env update -f environment.yml --prune
```

### 方式二：手动创建

```bash
# 1. 创建 conda 环境
conda create -n phylab python=3.10 -y

# 2. 激活环境
conda activate phylab

# 3. 安装 conda 可用的包
conda install numpy scipy matplotlib pandas pillow pyqt sympy openpyxl -y

# 4. 安装 pip 专属的包
pip install uncertainties lmfit
```

### 常用环境管理命令

```bash
conda activate phylab      # 激活环境
conda deactivate           # 退出环境
conda env remove -n phylab # 删除环境（如需重建）
```

---

## 🤖 AI Agent 工作流指引

> **本节面向 Claude / Codex / Gemini 等 AI 编程助手。**
> 当你需要运行 `src/` 目录下的 Python 脚本时，请严格按照以下流程操作。

### 步骤 0：先确认用户要用的虚拟环境/解释器（必须）

在执行任何 `python` 之前，先向用户确认使用哪一种方式运行脚本：

- **推荐**：使用本项目的 conda 环境 `phylab`
- **可选**：使用用户已有的 conda 环境（给出环境名，例如 `myenv`）
- **可选**：使用用户已有的 venv/解释器路径（给出 `python` 的绝对路径，例如 `~/.venv/bin/python`）

确认后，用一个变量在后续步骤中统一表示“Python 运行命令”：

```bash
# 例 1：项目推荐 conda 环境（推荐）
PYTHON_RUN='conda run -n phylab python'

# 例 2：用户自定义 conda 环境
# PYTHON_RUN='conda run -n <ENV_NAME> python'

# 例 3：用户自定义 venv/解释器路径
# PYTHON_RUN='<ABSOLUTE_PATH_TO_PYTHON>'
```

> 若用户不确定或未提供信息：默认先询问是否使用 `phylab`；只有用户明确同意后才继续。

### 总体流程图

```
开始
 │
 ▼
[步骤 0] 询问并确认虚拟环境/解释器
 │
 ▼
[步骤 1] 检测宿主机是否安装 conda
 │
 ├── 未安装 → 告知用户并停止，给出安装指引
 │
 ▼
[步骤 2] 检测 phylab 环境是否存在
 │
 ├── 存在 → 询问用户"检测到 phylab 环境，是否直接使用？" 
 │           ├── 用户确认 → 跳到 [步骤 4]
 │           └── 用户要求重建 → 删除并跳到 [步骤 3]
 │
 └── 不存在 → 询问用户"未检测到 phylab 环境，是否为您创建？"
              ├── 用户确认 → 进入 [步骤 3]
              └── 用户拒绝 → 停止
 │
 ▼
[步骤 3] 创建 phylab 环境并安装依赖
 │
 ▼
[步骤 4] 验证关键模块是否可用
 │
 ├── 缺少模块 → 询问用户"发现缺失模块 xxx，是否安装？"
 │               ├── 用户确认 → 安装缺失模块
 │               └── 用户拒绝 → 告知风险后继续
 │
 ▼
[步骤 5] 运行 Python 脚本
 │
 ▼
[步骤 6] 检查输出与结果
```

---

### 步骤 1：检测宿主机 conda 是否可用

运行以下命令：

```bash
conda --version
```

- **成功**（输出版本号如 `conda 25.x.x`）：继续步骤 2。
- **失败**（`command not found`）：
  - ⚠️ 向用户报告：`"您的系统中未检测到 conda。请先安装 Miniconda 或 Anaconda。"`
  - 提供安装链接：`https://docs.conda.io/en/latest/miniconda.html`
  - **停止执行**，等待用户解决。

---

### 步骤 2：检测 phylab 环境是否存在

运行以下命令：

```bash
conda env list | grep "phylab"
```

#### 情况 A：环境已存在（有输出行）

向用户报告并确认：

> ✅ 检测到已存在的 `phylab` conda 环境。是否直接使用该环境运行脚本？
> - **回复"是"或确认** → 跳到步骤 4
> - **回复"重建"** → 我将删除并重新创建该环境
> - **回复其他需求** → 请告诉我您的想法

如果用户要求重建：

```bash
conda env remove -n phylab -y
```

然后进入步骤 3。

#### 情况 B：环境不存在（无输出）

向用户报告并询问：

> ❌ 未检测到 `phylab` conda 环境。本项目的 Python 脚本需要该环境才能运行。
> 是否为您创建 `phylab` 环境？（创建过程可能需要几分钟）

- 用户确认 → 进入步骤 3
- 用户拒绝 → 停止执行

---

### 步骤 3：创建 phylab 环境

**优先方式**：使用本目录下的 `environment.yml`：

```bash
conda env create -f <本项目 src 目录的绝对路径>/environment.yml
```

**备选方式**（如果 `environment.yml` 不存在）：

```bash
conda create -n phylab python=3.10 numpy scipy matplotlib pandas pillow pyqt sympy openpyxl -y
```

然后安装 pip 包（注意：非交互式环境下不要用 `conda activate`，直接指定路径）：

```bash
# 找到 phylab 环境的 pip 路径
PHYLAB_PIP=$(conda run -n phylab which pip)
$PHYLAB_PIP install uncertainties lmfit

# 或者直接用绝对路径（更可靠）
# 通常位于: ~/miniconda3/envs/phylab/bin/pip
```

创建完成后，向用户报告：

> ✅ phylab 环境创建完成！已安装以下模块：numpy, scipy, matplotlib, pandas, pillow, PyQt6, sympy, openpyxl, uncertainties, lmfit。

---

### 步骤 4：验证关键模块可用性

运行以下验证命令：

```bash
conda run -n phylab python -c "
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

  > ⚠️ 以下模块在 phylab 环境中缺失：`xxx`, `yyy`。
  > 是否为您安装这些模块？

  用户确认后，按需安装：
  ```bash
  conda install -n phylab <conda包名> -y          # conda 优先
  conda run -n phylab pip install <pip包名>        # conda 无法安装时用 pip
  ```

---

### 步骤 5：运行 Python 脚本

使用“步骤 0”中确认的 `PYTHON_RUN` 来执行脚本。若用户确认使用 `phylab`，则用 `conda run`（**无需 `conda activate`**）：

```bash
$PYTHON_RUN <脚本的绝对路径>
```

> **⚠️ 重要**：不要使用 `conda activate`，因为在非交互式 shell（Agent 环境）中可能失败。始终使用 `conda run -n phylab`。

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

1. **非交互式环境限制**：Agent 的终端通常是非交互式的，`conda activate` 可能不可用。始终使用 `conda run -n phylab <命令>` 来代替。
2. **绝对路径**：运行脚本时始终使用绝对路径，避免工作目录不一致导致的路径问题。
3. **中文绘图字体**：如果脚本生成含中文的图表，需在脚本开头配置 matplotlib 字体：
   ```python
   import matplotlib
   matplotlib.rcParams['font.sans-serif'] = ['SimHei']
   matplotlib.rcParams['axes.unicode_minus'] = False
   ```
4. **图片输出格式**：推荐保存为 PDF 格式（矢量图），便于 LaTeX 引用。
5. **主动询问**：在执行任何可能修改系统状态的操作（安装包、删除环境、创建文件）前，务必先向用户确认。
6. **模块安装优先级**：conda 优先，pip 兜底。混用时注意依赖冲突。

---

## 📂 推荐目录结构

```
src/
├── README.md              # 本说明文件（你正在读的）
├── environment.yml        # conda 环境定义文件
├── 实验名称/              # 每个实验一个子目录
│   ├── data/              # 原始数据（csv / xlsx）
│   ├── figures/           # 生成的图片（供 LaTeX 引用）
│   └── process.py         # 数据处理脚本
└── utils/                 # 公共工具函数（可选）
    ├── __init__.py
    ├── uncertainty.py     # 不确定度计算工具
    └── plotting.py        # 绑图样式配置
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
