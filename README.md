# ZJU Physics Lab Reports

浙江大学物理实验课程的 LaTeX 报告工作区，包含实验报告模板、实验报告源文件与数据处理脚本。

## 工作流指南

完整的 AI Agent 辅助实验报告工作流（环境搭建、课件解析、报告生成与归档）见：
[AI Agent + 大物实验报告工作流](https://peagothedreamer.github.io/learning/ai-agent-physics-lab-report/)

## 目录结构

```
.
├── Phy_lab/                      # 模板工作区：LaTeX 模板、公共工具、课程安排
├── 密立根油滴实验/
├── 用霍尔法测直流圆线圈与亥姆霍兹线圈磁场/
├── 直流双臂电桥/
└── 铁磁材料居里温度测量/
```

每个实验目录的结构：

```
<实验名称>/
├── Courseware/   # 教材、课件及原理截图
├── Template/     # LaTeX 模板与报告源文件（.tex）
├── src/          # 数据处理脚本
├── data/         # 原始实验数据与图片
└── Rst/          # 最终编译完成的 PDF
```

## 实验清单

| 实验 | 已有内容 |
| --- | --- |
| 密立根油滴实验 | 预习报告、实验报告、数据处理脚本 |
| 用霍尔法测直流圆线圈与亥姆霍兹线圈磁场 | 预习报告、实验报告、数据处理脚本 |
| 直流双臂电桥 | 预习报告、实验报告、数据处理脚本 |
| 铁磁材料居里温度测量 | 预习报告、实验报告、数据处理脚本 |

## 环境要求

- **Python 3.13**，依赖见各实验目录下的 `src/requirements.txt`
- **TeX Live 2026** + **XeLaTeX**（含 `xeCJK`、`fontspec`，不能用 pdfLaTeX）
- 推荐 VS Code + LaTeX Workshop

虚拟环境统一放在仓库根目录：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r Phy_lab\src\requirements.txt
```

## 编译报告

```bash
cd <实验名称>/Template
latexmk -xelatex Phyport底板.tex   # 实验报告
latexmk -xelatex Preport底板.tex   # 预习报告
```

编译产物中的最终 PDF 归档到对应实验目录的 `Rst/`。

## 数据处理

```bash
.venv\Scripts\python.exe <实验名称>\src\<脚本>.py
```

绘图默认使用 `SimHei` 显示中文，输出 PDF 矢量图供 LaTeX 引用。

## 仓库说明

- `.venv/`、LaTeX 中间文件、MinerU 解析中间文件均不纳入版本管理。
- `References/` 目录（他人实验报告）未包含在本仓库中。
- 铁磁材料的磁滞回线和基本磁化曲线实验暂未上传。
