# VibeDock - AI驱动的智能适配系统

> 从"代码即文档"跨越到"智能即理解"时代

VibeDock通过构建一个AI驱动的智能适配系统，彻底重新定义了项目理解和技术栈学习的方式。我们的核心理念是：**每个开发者都应该获得最适合自己的项目理解路径**。

## ✨ 核心功能

### 🧠 多维度智能适配引擎
- **⚡ 快速理解模式** - 紧急项目维护的最短路径策略
- **🔄 功能迭代模式** - 理解深度与开发效率的完美平衡  
- **🎯 个性化Gap分析** - AI驱动的学习路径定制
- **📊 知识图谱可视化** - 项目结构一目了然

### 🤖 AI驱动的个性化Gap分析引擎
- 深度对话式技能评估
- 智能识别知识差距
- 生成专属学习路径
- 提供精选学习资源

## 🚀 快速开始

### 环境配置

1. **安装Python环境**
   ```bash
   # 需要Python >= 3.13
   python --version
   ```

2. **安装uv包管理工具**
   ```bash
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # macOS/Linux  
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **克隆并设置项目**
   ```bash
   git clone <repository-url>
   cd vibedock-main
   uv sync  # 自动创建虚拟环境并安装依赖
   ```

### API配置

创建 `.env` 文件，配置你的AI服务：

```env
# 推荐使用DeepSeek API（性价比高）
BASE_URL="https://api.deepseek.com/v1"
MODEL="deepseek-chat" 
API_KEY="your-api-key-here"

# 也支持其他OpenAI兼容API
# BASE_URL="https://api.openai.com/v1"
# MODEL="gpt-4"
# API_KEY="your-openai-key"
```

### 运行VibeDock

```bash
uv run main.py
```

## 📖 使用指南

### 第一次使用

1. **启动系统**
   ```bash
   uv run main.py
   ```

2. **选择使用目的**
   - 🔧 Active development - 参与项目开发
   - 📚 Learning - 理解项目原理
   - 🛠️ Maintenance - 维护现有代码
   - 🔗 Integration - 集成到自己项目
   - 🔍 Evaluation - 评估项目价值

3. **回答技能评估问题**
   - 系统会根据项目技术栈生成针对性问题
   - 诚实回答以获得最准确的学习路径

4. **获取学习报告**
   - 自动在浏览器中打开高端可视化报告
   - 包含个性化Gap分析和学习资源推荐

### 三阶段智能适配流程

```
→ 智能项目分析
  🤖 AI分析项目技术栈和架构模式
  📈 生成多维度技术评估报告

→ 个性化差距评估  
  💬 智能对话式技能评估
  🎯 精准识别学习需求

→ 知识图谱可视化
  🌐 生成交互式学习路径
  📱 浏览器中开启智能理解体验
```

## 📂 项目结构

```
vibedock-main/
├── main.py                     # 主程序入口
├── fileprocess.py             # 项目分析模块
├── tech_stack_questionnaire.py # 问卷调查系统
├── html_report_generator.py    # HTML报告生成器
├── stage1_processor.py        # 第一阶段处理器
├── stage2_processor.py        # 第二阶段处理器
├── vibehacks/                 # 核心分析工具
│   ├── analyzer.py           # 代码分析器
│   ├── reporter.py           # 报告生成器
│   └── cli.py               # 命令行界面
├── output/                   # 输出文件夹
├── .env                     # API配置文件
└── README.md               # 使用说明
```

## 🎨 报告功能

生成的HTML报告包含：

### 📊 个性化Gap分析仪表板
- 知识差距热力图
- 技能熟练度雷达图  
- 学习优先级排序

### 🎯 智能学习路径推荐
- 每个Gap提供3-5个精选学习资源
- 官方文档、视频教程、实战项目链接
- 每个资源都有**"开始学习"按钮**

### 🏗️ 项目技术栈洞察
- 技术栈架构可视化
- 依赖关系图谱
- 关键组件说明

### 📅 行动计划生成器
- 30天学习计划
- 里程碑设置
- 进度追踪建议

## 🛠️ 高级用法

### 自定义API配置

支持多种AI服务商：

```env
# DeepSeek (推荐，性价比最高)
BASE_URL="https://api.deepseek.com/v1"
MODEL="deepseek-chat"

# OpenAI
BASE_URL="https://api.openai.com/v1"  
MODEL="gpt-4"

# 智谱AI
BASE_URL="https://open.bigmodel.cn/api/paas/v4"
MODEL="glm-4"

# 月之暗面
BASE_URL="https://api.moonshot.cn/v1"
MODEL="moonshot-v1-8k"
```

### 批量分析多个项目

```bash
# 分析特定项目目录
cd /path/to/your/project
uv run /path/to/vibedock-main/main.py
```

### 报告文件管理

```bash
# 查看生成的报告
ls output/
# VibeDock_智能学习路径_20241201_143052.html
# report.md
# gap_summary.md
```

## 🔧 故障排除

### 常见问题

1. **API调用失败**
   ```bash
   # 检查.env文件配置
   cat .env
   # 确认API密钥有效性
   ```

2. **依赖安装失败**  
   ```bash
   # 清除缓存重新安装
   uv cache clean
   uv sync --refresh
   ```

3. **Python版本不匹配**
   ```bash
   # 检查Python版本
   python --version  # 需要 >= 3.13
   # 使用pyenv管理Python版本
   ```

4. **HTML报告打开异常**
   - 确保浏览器支持现代CSS特性
   - 检查防火墙是否阻止本地文件访问

### 性能优化

- **大项目分析**：首次分析可能需要1-3分钟
- **API调用频率**：根据使用量调整API配置
- **内存使用**：分析大型项目时建议16GB+内存

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🌟 技术架构

VibeDock采用模块化设计，核心组件：

- **分析引擎**：基于AST的Python代码静态分析
- **AI适配器**：支持多种大语言模型API
- **报告生成器**：现代化HTML报告模板
- **交互系统**：智能问卷和对话界面

---

**让每个开发者都获得最适合自己的项目理解路径** 🚀