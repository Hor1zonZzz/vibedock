# Python项目第三方包分析报告

## 📊 总体统计

| 指标 | 数量 |
|------|------|
| 第三方包总数 | 11 |
| 导入函数总数 | 2 |
| 导入类总数 | 10 |
| 总使用次数 | 91 |

## 🏆 最常用的包 (Top 10)

| 排名 | 包名 | 使用次数 | 导入函数数 | 导入类数 |
|------|------|----------|------------|----------|
| 1 | loguru | 40 | 1 | 0 |
| 2 | base | 12 | 0 | 2 |
| 3 | ocr | 6 | 0 | 2 |
| 4 | config | 6 | 0 | 2 |
| 5 | factory | 6 | 0 | 1 |
| 6 | base64 | 6 | 0 | 0 |
| 7 | dotenv | 5 | 1 | 0 |
| 8 | yaml | 4 | 0 | 0 |
| 9 | mistralai | 4 | 0 | 1 |
| 10 | providers | 2 | 0 | 1 |

## 📦 包详细信息

### loguru

**基本信息:**
- 总使用次数: 40
- 使用文件数: 4
- 导入函数数: 1
- 导入类数: 0

**🔧 函数使用情况:**

| 函数名 | 使用次数 |
|--------|----------|
| error | 22 |
| success | 10 |
| info | 8 |

**📁 使用文件:**

- ocr/config/mistral.py
- ocr/providers/mistral.py
- ocr0909/ocr/config/mistral.py
- ocr0909/ocr/providers/mistral.py

---

### base

**基本信息:**
- 总使用次数: 12
- 使用文件数: 10
- 导入函数数: 0
- 导入类数: 2

**🏗️ 类使用情况:**

| 类名 | 使用次数 |
|------|----------|
| BaseOCRProvider | 10 |
| BaseConfig | 2 |

**📁 使用文件:**

- ocr/__init__.py
- ocr/config/mistral.py
- ocr/factory.py
- ocr/processor.py
- ocr/providers/mistral.py
- ocr0909/ocr/__init__.py
- ocr0909/ocr/config/mistral.py
- ocr0909/ocr/factory.py
- ocr0909/ocr/processor.py
- ocr0909/ocr/providers/mistral.py

---

### ocr

**基本信息:**
- 总使用次数: 6
- 使用文件数: 4
- 导入函数数: 0
- 导入类数: 2

**🔧 函数使用情况:**

| 函数名 | 使用次数 |
|--------|----------|
| _configs | 2 |

**🏗️ 类使用情况:**

| 类名 | 使用次数 |
|------|----------|
| OCRProcessor | 4 |

**📁 使用文件:**

- example_new_architecture.py
- ocr0909/test_check_the_ocr_module_work.py
- ocr_processor.py
- test_check_the_ocr_module_work.py

---

### config

**基本信息:**
- 总使用次数: 6
- 使用文件数: 8
- 导入函数数: 0
- 导入类数: 2

**🏗️ 类使用情况:**

| 类名 | 使用次数 |
|------|----------|
| MistralConfig | 6 |

**📁 使用文件:**

- ocr/__init__.py
- ocr/base.py
- ocr/factory.py
- ocr/providers/mistral.py
- ocr0909/ocr/__init__.py
- ocr0909/ocr/base.py
- ocr0909/ocr/factory.py
- ocr0909/ocr/providers/mistral.py

---

### factory

**基本信息:**
- 总使用次数: 6
- 使用文件数: 4
- 导入函数数: 0
- 导入类数: 1

**🔧 函数使用情况:**

| 函数名 | 使用次数 |
|--------|----------|
| create_provider | 4 |
| get_supported_providers | 2 |

**📁 使用文件:**

- ocr/__init__.py
- ocr/processor.py
- ocr0909/ocr/__init__.py
- ocr0909/ocr/processor.py

---

