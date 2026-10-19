---
description: 运行物理实验 Python 数据处理脚本（自动检测/创建 phylab 环境）
---

# 运行 Python 脚本工作流

当用户要求运行 `src/` 目录下的 Python 脚本时，**必须**按以下步骤操作。
每一步涉及系统修改的操作前，都需要向用户确认。

---

## 步骤 1：检测 conda 是否可用

// turbo
```bash
conda --version
```

- **成功**（输出版本号）→ 继续步骤 2
- **失败**（command not found）→ 向用户报告：
  > "❌ 您的系统中未检测到 conda。请先安装 Miniconda：https://docs.conda.io/en/latest/miniconda.html"
  
  **停止执行**，等待用户解决。

---

## 步骤 2：检测 phylab 环境是否存在

// turbo
```bash
conda env list | grep -q "phylab" && echo "ENV_EXISTS" || echo "ENV_NOT_FOUND"
```

### 如果输出 `ENV_EXISTS`

向用户确认：
> "✅ 检测到已有的 `phylab` conda 环境。是否使用该环境运行脚本？（回复'重建'可以重新创建环境）"

- 用户确认使用 → **跳到步骤 4**
- 用户要求重建 → 执行 `conda env remove -n phylab -y`，然后继续步骤 3

### 如果输出 `ENV_NOT_FOUND`

向用户询问：
> "❌ 未检测到 `phylab` conda 环境。是否为您创建该环境？（需要安装 numpy, scipy, matplotlib 等科学计算包，大约需要几分钟）"

- 用户确认 → 继续步骤 3
- 用户拒绝 → **停止执行**

---

## 步骤 3：创建 phylab 环境

首先检查 `environment.yml` 是否存在：

// turbo
```bash
test -f /home/zju_jsc/latex/WIP/Phy_lab/src/environment.yml && echo "YML_EXISTS" || echo "YML_NOT_FOUND"
```

### 如果 `YML_EXISTS`

```bash
conda env create -f /home/zju_jsc/latex/WIP/Phy_lab/src/environment.yml
```

### 如果 `YML_NOT_FOUND`

```bash
conda create -n phylab python=3.10 numpy scipy matplotlib pandas pillow pyqt sympy openpyxl -y
```

然后安装 pip 包（找到 phylab 的 pip 路径）：

// turbo
```bash
PHYLAB_PIP=$(dirname $(conda run -n phylab which python))/pip && $PHYLAB_PIP install uncertainties lmfit
```

如果上面的方式失败，尝试直接指定路径：
```bash
~/miniconda3/envs/phylab/bin/pip install uncertainties lmfit
```

创建完成后，向用户报告：
> "✅ phylab 环境创建成功！已安装 numpy, scipy, matplotlib, pandas, sympy, openpyxl, uncertainties, lmfit 等模块。"

---

## 步骤 4：验证关键模块

// turbo
```bash
conda run -n phylab python -c "
mods = ['numpy','scipy','matplotlib','pandas','sympy','openpyxl','uncertainties','lmfit','PIL']
missing = []
for m in mods:
    try: __import__(m)
    except ImportError: missing.append(m)
if missing: print('MISSING:' + ','.join(missing))
else: print('ALL_OK')
"
```

- **`ALL_OK`** → 继续步骤 5
- **`MISSING:xxx,yyy`** → 向用户询问：
  > "⚠️ 以下模块缺失：`xxx`, `yyy`。是否为您安装？"

  用户确认后安装缺失模块：
  ```bash
  conda install -n phylab <包名> -y       # conda 优先
  conda run -n phylab pip install <包名>  # pip 兜底
  ```

  注意：PIL 对应的包名是 `pillow`。

---

## 步骤 5：运行脚本

**关键：不要使用 `conda activate`**，在非交互式 shell 中可能失败。

// turbo
```bash
conda run -n phylab python <脚本的绝对路径>
```

将 `<脚本的绝对路径>` 替换为用户指定的脚本路径。

---

## 步骤 6：检查结果

1. **退出码为 0**：脚本执行成功
   - 如果生成了图片文件，告知用户保存路径
   - 询问用户："是否需要将生成的图片引用到 LaTeX 报告中？"

2. **退出码非 0**：脚本执行失败
   - 分析 stderr 错误信息
   - 向用户解释错误原因
   - 询问用户："是否需要我帮您修复这个错误？"

---

## 注意事项速查

| 事项 | 说明 |
| --- | --- |
| **不要 `conda activate`** | Agent 终端是非交互式的，始终用 `conda run -n phylab` |
| **使用绝对路径** | 运行脚本和保存文件时都用绝对路径 |
| **中文绘图字体** | 脚本中需要设置 `rcParams['font.sans-serif'] = ['SimHei']` |
| **图片格式** | 推荐 PDF（矢量图），便于 LaTeX 引用 |
| **修改前必须询问** | 安装包、删除环境、创建文件等操作前务必先向用户确认 |
| **模块安装优先级** | conda 优先，pip 兜底 |
