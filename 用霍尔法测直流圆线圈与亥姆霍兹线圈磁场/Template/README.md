# 浙江大学物理实验报告 LaTeX 模版

## 📁 文件结构

```
Template/
├── Phyport.cls          # 物理实验报告（正式报告）的文档类
├── Phyport底板.tex       # 正式报告的模板文件（使用时复制此文件）
├── Preport.cls          # 物理实验预习报告的文档类
├── Preport底板.tex       # 预习报告的模板文件（使用时复制此文件）
├── 功能实例.tex          # 图片、表格、公式等功能的使用示例
├── 注意事项.tex          # 末尾"注意事项"部分（被 \input 引入）
├── figures/             # 图片资源目录
│   └── 浙江大学.pdf     # 封面校名 logo
└── README.md            # 本说明文件
```

---

## 🧩 模版原理

### 两套文档类

本模版提供 **两个文档类**（`.cls`），分别用于两种实验文档：

| 文档类 | 用途 | 底板文件 |
| --- | --- | --- |
| `Phyport` | 物理实验**正式报告** | `Phyport底板.tex` |
| `Preport` | 物理实验**预习报告** | `Preport底板.tex` |

两者结构相似，区别在于：
- `Phyport` 封面包含**浙江大学校名 logo** 和"物理实验报告"标题，支持 `\extable{}`（实验桌号）字段
- `Preport` 封面标题为"物理实验预习报告"，无实验桌号字段，无校名 logo

### 基础架构

两个 `.cls` 均基于 **`ctexart`** 文档类，使用 **XeLaTeX** 编译引擎。主要特性包括：

- **字体配置**：主字体为 SimSun（宋体），粗体 SimHei（黑体），斜体 KaiTi（楷体），等宽字体 DejaVu Sans Mono
- **自定义字体命令**：`\fbsong{}`（伪粗宋体）、`\fbfangsong{}`（伪粗仿宋体）
- **章节编号**：一级标题使用中文数字（"一、""二、"），二级使用阿拉伯数字（"1." "2."），三级使用括号（"(1)"）
- **页面布局**：上下边距 1in，左右边距 1.91cm，行距 1.2 倍
- **代码排版**：内置 `listings` 配置，使用中国传统色彩（松花绿、靛蓝、琥珀等）高亮
- **图片路径**：默认搜索 `figures/` 目录（通过 `\graphicspath{{figures/}}` 设置）
- **封面生成**：通过 `\makecover` 命令自动排版封面

### 已加载的宏包

`.cls` 文件中已经加载了以下宏包，**无需在 `.tex` 文件中重复引入**：

| 宏包 | 功能 |
| --- | --- |
| `graphicx` | 图片插入 |
| `xcolor` | 颜色支持 |
| `tikz` | 绘图 |
| `geometry` | 页面布局 |
| `titlesec` | 标题格式 |
| `fancyhdr` | 页眉页脚 |
| `listings` | 代码排版 |
| `cncolours` | 中国传统色彩 |
| `indentfirst` | 首段缩进 |
| `enumitem` | 列表定制 |
| `zhnumber` | 中文数字 |
| `fontspec` | 字体选择（XeLaTeX） |
| `stackengine` | 堆叠排版（用于下划线） |

---

## 🚀 使用方式

### 1. 新建实验报告

**不要直接修改底板文件！** 应将底板文件**复制一份**来使用：

```bash
# 正式报告
cp Phyport底板.tex  我的实验报告.tex

# 预习报告
cp Preport底板.tex  我的预习报告.tex
```

### 2. 填写基本信息

在复制出的 `.tex` 文件中，填写封面信息：

```latex
\exname{用霍尔法测磁场}    % 实验名称
\extable{7}                % 实验桌号（仅 Phyport）
\instructor{张三}          % 指导教师
\class{物理2501}           % 班级
\name{李四}                % 姓名
\stuid{12345678}           % 学号

\nyear{2026}               % 年
\nmonth{3}                 % 月
\nday{14}                  % 日
\nweekday{六}              % 星期几

\redate{}                  % 补做日期（无则留空）
\resitu{}                  % 情况说明（无则留空）
```

### 3. 撰写报告内容

在 `\begin{document}` ... `\end{document}` 之间，按照模版大纲填写各部分内容。模板结构（以正式报告为例）：

```
一、预习报告（10分）
   1. 实验综述（5分）
   2. 实验重点（3分）
   3. 实验难点（2分）
二、原始数据（20分）
三、结果与分析（60分）
   1. 数据处理与结果（30分）
   2. 误差分析（20分）
   3. 实验探讨（10分）
四、思考题（10分）
```

### 4. 插入图片

将图片文件放入 `figures/` 目录，然后在文中引用：

```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.6\linewidth]{你的图片文件名}
    \caption{图片说明}
    \label{fig:xxx}
\end{figure}
```

> 由于 `\graphicspath` 已设为 `figures/`，文件名无需包含路径前缀。

### 5. 插入三线表

推荐在导言区额外加载 `booktabs` 和 `float` 宏包：

```latex
\usepackage{float}
\usepackage{booktabs}
```

然后使用三线表：

```latex
\begin{table}[H]
    \centering
    \caption{数据记录表}
    \label{tab:xxx}
    \begin{tabular}{ccc}
        \toprule
        序号 & 测量值 / mm & 偏差 / mm \\
        \midrule
        1 & 25.32 & 0.02 \\
        2 & 25.28 & $-0.02$ \\
        \bottomrule
    \end{tabular}
\end{table}
```

> 更多图片和表格的用法示例请参考 `功能实例.tex`。

---

## ⚙️ 编译方式

### 编译引擎

本模版 **必须** 使用 **XeLaTeX** 编译（因为使用了 `fontspec` 和 `xeCJK` 进行中文字体配置）。

> ⚠️ **不能使用 pdfLaTeX 编译**，否则会报错！

### 命令行编译

```bash
# 方式一：直接使用 xelatex（需编译两次以生成正确的交叉引用）
xelatex 我的实验报告.tex
xelatex 我的实验报告.tex

# 方式二：使用 latexmk 自动处理多次编译（推荐）
latexmk -xelatex 我的实验报告.tex
```

### VS Code（LaTeX Workshop 插件）编译

在 VS Code 中使用 **LaTeX Workshop** 插件时，需要确保编译配置（recipe）使用的是 `xelatex`。

推荐在 `.vscode/settings.json` 或全局设置中配置：

```json
{
    "latex-workshop.latex.tools": [
        {
            "name": "xelatex",
            "command": "xelatex",
            "args": [
                "-synctex=1",
                "-interaction=nonstopmode",
                "-file-line-error",
                "%DOC%"
            ]
        }
    ],
    "latex-workshop.latex.recipes": [
        {
            "name": "xelatex × 2",
            "tools": ["xelatex", "xelatex"]
        }
    ]
}
```

### 清理临时文件

编译会生成大量临时文件（`.aux`, `.log`, `.out`, `.synctex.gz` 等），可通过以下命令清理：

```bash
latexmk -c            # 清理临时文件，保留 PDF
latexmk -C            # 清理所有生成文件（包括 PDF）
```

---

## ⚠️ 注意事项

### 1. 字体依赖

模版要求系统中安装以下字体：

| 字体名 | 说明 |
| --- | --- |
| **SimSun**（宋体） | CJK 主字体 |
| **SimHei**（黑体） | CJK 粗体 |
| **KaiTi**（楷体） | CJK 斜体 |
| **FangSong**（仿宋） | 注意事项部分使用 |
| **DejaVu Sans Mono** | 等宽/代码字体 |

如果缺少字体会导致编译报错。Linux 系统下需要手动安装 Windows 中文字体（SimSun、SimHei、KaiTi、FangSong）。

### 2. 文件编码

所有 `.tex` 文件应使用 **UTF-8** 编码保存，否则中文可能出现乱码。

### 3. 图片格式

XeLaTeX 支持的图片格式包括 **PDF、PNG、JPG**。推荐：
- **矢量图**（公式推导、电路图）使用 PDF 格式
- **照片**（原始数据扫描件等）使用 JPG 或 PNG 格式

### 4. `选用宏.tex` 文件

`Phyport底板.tex` 中有一行 `\input{选用宏.tex}`。如果你不需要额外的自定义宏，可以：
- 创建一个空的 `选用宏.tex` 文件
- 或者注释掉该行（在行首加 `%`）

否则编译时会因找不到文件而报错。

### 5. 不要重复加载已有宏包

`.cls` 中已加载了 `graphicx`、`xcolor`、`tikz` 等宏包（见上表），在 `.tex` 文件中无需再次 `\usepackage`，否则可能引起冲突。

### 6. 浮动体位置

在物理实验报告中，推荐对所有图表使用 `[H]`（需加载 `float` 宏包）来强制在当前位置显示，避免 LaTeX 自动将图表浮动到其他位置导致阅读不便。

### 7. `\makecover` 必须在 `\begin{document}` 之后

封面命令 `\makecover` 要放在 `\begin{document}` 后面调用，且在所有正文内容之前。模版底板中已正确放置，不要改动其位置。

### 8. 提交格式

根据课程要求：
- 最终提交 **PDF 格式**
- 文件命名格式：`姓名+学号+实验名称+周次`
- 提交到"学在浙大"对应实验项目的"作业"模块

---

## 📖 参考资料

- [LaTeX 入门（刘海洋）](https://book.douban.com/subject/24703731/)
- [一份（不太）简短的 LaTeX2e 介绍](https://mirrors.ctan.org/info/lshort/chinese/lshort-zh-cn.pdf)
- [booktabs 宏包文档（三线表）](https://ctan.org/pkg/booktabs)
- [浙江大学物理实验中心](https://phylab.zju.edu.cn/)
