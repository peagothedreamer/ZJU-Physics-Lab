# 浙江大学物理实验报告工作区

## 项目简介

本项目是浙江大学物理实验课程的 LaTeX 报告工作区，配合 AI 助手（Claude）自动生成预习报告与实验报告。

## 目录结构

```
Phy_lab/
├── CLAUDE.md            # 本文件 — 项目说明
├── Prompt.md            # AI 助手角色与工作流定义
├── Courseware/          # 实验教材电子版及原理截图
│   └── 课程安排.md       # 实验名称/周次/任课教师/地点/日期 的权威来源
├── References/          # 优秀实验报告实例（参考格式与风格）
├── src/                 # 数据处理 Python 脚本
│   ├── requirements.txt # pip 依赖清单
│   ├── README.md        # Python 环境与数据处理指南
│   └── utils/           # 公共工具函数
├── Template/            # LaTeX 模板
│   ├── Phyport.cls      # 正式报告文档类
│   ├── Preport.cls      # 预习报告文档类
│   ├── Phyport底板.tex   # 正式报告模板
│   ├── Preport底板.tex   # 预习报告模板
│   ├── 功能实例.tex      # 图片/表格/公式代码示例（核心参考）
│   ├── 注意事项.tex      # 末尾注意事项部分
│   ├── 选用宏.tex        # 额外宏包声明
│   └── figures/         # 图片资源（含校名 logo）
├── Rst/                 # 最终成品 PDF 存放目录（预习报告 / 实验报告）
├── .agent/workflows/    # AI Agent 工作流
├── .vscode/settings.json# VS Code 配置（LaTeX Workshop + Python）
└── .gitignore
```

## Python 环境

- 使用 Python venv
- Python 3.13，虚拟环境位于项目根目录 `.venv/`
- 依赖定义：`src/requirements.txt`
- 创建环境：`python -m venv .venv` → `.venv\Scripts\Activate.ps1` → `pip install -r src\requirements.txt`
- 运行脚本：`.venv\Scripts\python.exe <脚本路径>`

## LaTeX 编译

- **编译引擎**：XeLaTeX（必须，因 fontspec/xeCJK）
- **不能使用 pdfLaTeX**
- 编译命令：`latexmk -xelatex 文件名.tex` 或 `xelatex 文件名.tex`（执行两次）
- 清理临时文件：`latexmk -c`
- TeX Live 2026 安装位置：`F:\texlive\2026\`

## 常用工作流

1. **做预习报告**：阅读 `Courseware/` → 填充 `Template/Preport底板.tex`
2. **做实验报告**：迁移预习内容 → 运行 `src/` 数据处理脚本 → 填充 `Template/Phyport底板.tex`
3. **插入图片/表格**：严格参照 `Template/功能实例.tex` 的代码格式
4. **产出最终 PDF**：编译成功后，将最终 PDF 复制（不要移动/覆盖草稿）到 `Rst/` 目录，并按以下规则命名：
   - 预习报告：`姓名-学号-实验名称预习报告-第x周.pdf`
   - 实验报告：`姓名-学号-实验名称实验报告-第x周.pdf`
   - 示例：`管云哲-3250104519-用霍尔法测直流圆线圈与亥姆霍兹线圈磁场预习报告-第1周.pdf`
   - **实验名称一律使用 `课程安排.md` 中的全称**，不得简写、缩写或改写
   - 若姓名/学号未知，主动询问用户后再命名保存，不得臆造

## 课程安排（元信息来源）

`Courseware/课程安排.md` 是**实验名称、上课周次、任课教师**的权威来源，含实验地址与上课日期。每次开始撰写报告前先读取该文件，按下表字段对应填入封面：

| 课程安排.md 字段 | 用途 |
| --- | --- |
| 实验名称 | `\exname{}`，以及 `Rst/` 中 PDF 的文件名；**使用全称，不得简写** |
| 上课周次（如"第3周"） | `Rst/` 中 PDF 文件名的"第x周"，可与 `\nday` 等封面日期互校 |
| 任课教师 | `\instructor{}`（取"编号 \| 姓名"中的姓名部分） |
| 实验地址 / 上课日期 / 上课时间 | 仅供核对，模板无对应字段；若用户要求可写入说明 |
| 实验次数为 2 的项（如第11,12周） | 同一实验占用两周，命名时确认用户要填哪一个周次 |

**实验名称必须逐字照抄表中的全称**，例如写"用霍尔法测直流圆线圈与亥姆霍兹线圈磁场"，不得写成"用霍尔法测磁场"。

需注意的两个文件名细节：
- 第11-14周的"必做"实验全称含 `:` 和 `+`（如"必做1: 示波器的使用+组装振流器"）。Windows 文件名不允许半角 `:`，归档时应将 `:` 替换为全角 `：`，其余字符保留，并把替换结果告知用户。
- "迈克尔逊干涉仪的应用G"结尾的 `G` 是光学实验类别标记（非实验名称的一部分），归档命名时应删除，写作"迈克尔逊干涉仪的应用"。

## 注意事项

- 所有 `.tex` 文件使用 UTF-8 编码
- 图片放入 `Template/figures/` 目录，引用时无需路径前缀
- 不要重复加载 `.cls` 中已有的宏包（graphicx, xcolor, tikz 等）
- 不要删除模板中的指导性注释文字
- `\makecover` 必须在 `\begin{document}` 之后
