---
description: 运行物理实验 Python 数据处理脚本（自动检测/创建 venv 环境）
---

# 运行 Python 脚本工作流

当用户要求运行 `src/` 目录下的 Python 脚本时，**必须**按以下步骤操作。
每一步涉及系统修改的操作前，都需要向用户确认。

> 本项目使用 **venv** 虚拟环境（不使用 conda），环境位于**项目父目录** `../.venv/`（与 `Phy_lab` 同级）。

---

## 步骤 1：检测 venv 是否存在

// turbo
```bash
test -d ../.venv && echo "VENV_EXISTS" || echo "VENV_NOT_FOUND"
```

### 如果输出 `VENV_EXISTS`

继续步骤 2。

### 如果输出 `VENV_NOT_FOUND`

向用户询问：
> "❌ 未检测到虚拟环境 `../.venv`。是否为您创建？（需要安装 numpy, scipy, matplotlib 等科学计算包，大约需要几分钟）"

- 用户确认 → 继续步骤 3
- 用户拒绝 → **停止执行**

---

## 步骤 2：检测依赖是否齐全

// turbo
```bash
../.venv/Scripts/pip.exe list 2>/dev/null || ../.venv/Scripts/pip list 2>/dev/null
```

检查输出中是否包含 numpy、scipy、matplotlib 等核心包。如果缺失较多，建议重新安装全部依赖：

向用户确认：
> "⚠️ 检测到部分依赖缺失，是否为您重新安装所有依赖？"

用户确认后：
```bash
../.venv/Scripts/pip.exe install -r src/requirements.txt
```

如果依赖齐全，跳到步骤 4。

---

## 步骤 3：创建 venv 并安装依赖

```bash
# 1. 创建虚拟环境（位于项目父目录）
python -m venv ../.venv

# 2. 升级 pip
../.venv/Scripts/python.exe -m pip install --upgrade pip

# 3. 安装依赖
../.venv/Scripts/pip.exe install -r src/requirements.txt
```

创建完成后，向用户报告：
> "✅ 虚拟环境创建成功！已安装 numpy, scipy, matplotlib, pandas, pillow, PyQt6, sympy, openpyxl, uncertainties, lmfit 等模块。"

---

## 步骤 4：验证关键模块

// turbo
```bash
../.venv/Scripts/python.exe -c "
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

  用户确认后安装：
  ```bash
  ../.venv/Scripts/pip.exe install xxx yyy
  ```

  注意：PIL 对应的包名是 `pillow`。

---

## 步骤 5：运行脚本

**关键：使用 venv 中的 python，不要使用全局 python。**

// turbo
```bash
../.venv/Scripts/python.exe <脚本的绝对路径>
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
| **不要使用全局 python** | 始终用 `../.venv/Scripts/python.exe`（venv 位于项目父目录），避免版本不一致 |
| **使用绝对路径** | 运行脚本和保存文件时都用绝对路径 |
| **中文绘图字体** | 脚本中需要设置 `rcParams['font.sans-serif'] = ['SimHei']` |
| **图片格式** | 推荐 PDF（矢量图），便于 LaTeX 引用 |
| **修改前必须询问** | 安装包、创建文件等操作前务必先向用户确认 |
| **Windows 路径** | PowerShell 用 `\`，Git Bash 用 `/`，两者均可执行 |
