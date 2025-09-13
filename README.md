# VibehHacks - Python代码库分析工具

一个强大的Python工具，用于分析Python项目中第三方包的导入和使用情况，提供详细的统计和可视化报告。

## 🚀 功能特性

- 🔍 **智能分析**: 自动识别并分析Python项目中的第三方包导入
- 📊 **详细统计**: 统计导入的函数、类和模块，以及它们的使用频次
- 🎯 **精准过滤**: 自动过滤标准库和项目内部模块，专注于第三方依赖
- 📈 **丰富报告**: 生成美观的控制台报告和Markdown格式的分析结果
- 🏆 **Top 20排行**: 显示使用最频繁的前20个包及其详细信息
- 🚀 **高性能**: 快速扫描大型代码库，智能忽略不必要的文件和目录

## 📦 安装

### 方法一：直接安装 (推荐)

```bash
# 克隆项目
git clone <repository-url>
cd vibehacks

# 安装包 (会自动安装所有依赖)
pip install .
```

### 方法二：开发模式安装

```bash
# 开发模式安装 (可编辑安装)
pip install -e .

# 如需开发工具 (测试、覆盖率等)
pip install -e .[dev]
```

### 系统要求

- Python 3.13 或更高版本
- 所有依赖会自动安装，无需手动处理

## 🛠️ 使用方法

### 命令行使用

```bash
# 基本分析 - 分析当前目录
vibehacks analyze .

# 分析指定项目目录
vibehacks analyze /path/to/your/project

# 分析并导出Markdown报告
vibehacks analyze /path/to/your/project --output-markdown report.md

# 查看特定包的详细信息
vibehacks analyze /path/to/your/project --package pandas

# 静默模式 (只输出到文件，不显示控制台报告)
vibehacks analyze /path/to/your/project --quiet --output-markdown report.md
```

### 命令行选项

- `PROJECT_PATH`: Python项目的根目录路径 (必需)
- `--output-markdown, -md`: 导出Markdown报告到指定文件
- `--package, -p`: 显示特定包的详细信息
- `--quiet, -q`: 静默模式，只输出结果到文件

### Python API使用

```python
from vibehacks.analyzer import ImportAnalyzer
from vibehacks.reporter import AnalysisReporter

# 创建分析器
analyzer = ImportAnalyzer("/path/to/your/project")

# 执行分析
imports_data, usage_data = analyzer.analyze_project()

# 创建报告生成器
reporter = AnalysisReporter(imports_data, usage_data)

# 打印详细的控制台报告
reporter.print_detailed_report()

# 显示特定包详情
reporter.print_package_details("pandas")

# 导出Markdown报告
reporter.export_to_markdown("analysis_report.md")

# 生成摘要报告
summary = reporter.generate_summary_report()
print(summary)
```

## 📊 分析结果

### 总体统计
- 第三方包总数
- 导入函数总数
- 导入类总数
- 总使用次数

### 🏆 Top 20包排行
按使用频次排序，显示：
- 包名和排名
- 总使用次数
- 导入的函数数量
- 导入的类数量

### 包详细信息
- 具体导入的函数和类列表
- 各函数/类的使用频次统计 (Top 20)
- 使用该包的源文件列表

## 📄 报告格式

### 控制台报告
使用Rich库美化的表格显示，包含：
- 彩色输出和格式化
- 清晰的统计表格
- 详细的使用情况展示

### Markdown报告
结构化的文档格式，包含：
- 总体统计表格
- Top 20包使用排行榜
- 每个重要包的详细使用分析
- 函数和类的使用频次排行

示例Markdown输出：
```markdown
# Python项目第三方包分析报告

## 📊 总体统计
| 指标 | 数量 |
|------|------|
| 第三方包总数 | 15 |
| 导入函数总数 | 87 |
| 导入类总数 | 23 |
| 总使用次数 | 234 |

## 🏆 最常用的包 (Top 20)
| 排名 | 包名 | 使用次数 | 导入函数数 | 导入类数 |
|------|------|----------|------------|----------|
| 1 | pandas | 45 | 8 | 2 |
| 2 | requests | 23 | 5 | 0 |
...
```

## ⚙️ 配置说明

### 自动忽略的文件和目录
工具智能过滤以下内容：
- 缓存目录: `__pycache__`, `.pytest_cache`, `.mypy_cache`
- 版本控制: `.git`, `.svn`
- 虚拟环境: `venv`, `.venv`, `env`, `.env`
- 构建目录: `build`, `dist`, `*.egg-info`
- Node.js: `node_modules`
- 配置文件: `.gitignore`, `setup.py`, `pyproject.toml`

### 包分类逻辑
- **第三方包**: 除标准库和项目内模块外的所有导入
- **项目内模块**: 当前项目目录下的Python模块
- **标准库**: Python内置标准库模块

## 🔧 依赖包

核心运行依赖：
- `click>=8.0.0`: 命令行接口框架
- `rich>=13.0.0`: 美观的控制台输出
- `pandas>=2.0.0`: 数据处理
- `ast-tools>=0.1.0`: AST分析增强
- `matplotlib>=3.7.0`: 可视化支持
- `seaborn>=0.12.0`: 统计图表

开发依赖 (可选):
- `pytest>=7.0.0`: 测试框架
- `pytest-cov>=4.0.0`: 覆盖率报告

## 🎯 使用场景

- **依赖审计**: 了解项目真实使用了哪些第三方包
- **代码重构**: 识别未充分利用或过度依赖的包
- **性能优化**: 分析高频使用的包和函数
- **文档生成**: 自动生成项目依赖文档
- **代码审查**: 评估第三方依赖的使用合理性

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个工具！

## 📄 许可证

MIT License