"""
代码分析器 - 分析Python项目中的导入和使用情况
"""

import ast
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Set, Tuple


class ImportAnalyzer:
    """分析Python代码中的导入和使用情况"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.ignore_patterns = {
            "__pycache__",
            ".git",
            ".venv",
            "venv",
            ".env",
            "env",
            "node_modules",
            ".pytest_cache",
            ".mypy_cache",
            ".tox",
            "build",
            "dist",
            "egg-info",
            ".coverage",
            "htmlcov",
        }

        # 存储分析结果
        self.imports_data = defaultdict(
            lambda: {
                "functions": set(),
                "classes": set(),
                "modules": set(),
                "aliases": dict(),
                "files": set(),
            }
        )
        self.usage_data = defaultdict(
            lambda: {
                "functions": Counter(),
                "classes": Counter(),
                "modules": Counter(),
                "total_usage": 0,
            }
        )
        self.stdlib_modules = self._get_stdlib_modules()

    def _get_stdlib_modules(self) -> Set[str]:
        """获取Python标准库模块列表"""
        stdlib_modules = set()
        stdlib_modules.update(sys.builtin_module_names)

        common_stdlib = {
            "os",
            "sys",
            "json",
            "datetime",
            "time",
            "random",
            "math",
            "collections",
            "itertools",
            "functools",
            "operator",
            "re",
            "pathlib",
            "typing",
            "dataclasses",
            "enum",
            "abc",
            "copy",
            "pickle",
            "csv",
            "sqlite3",
            "urllib",
            "http",
            "email",
            "html",
            "xml",
            "logging",
            "unittest",
            "argparse",
            "configparser",
            "io",
            "tempfile",
            "shutil",
            "glob",
            "fnmatch",
            "linecache",
            "textwrap",
            "string",
            "struct",
            "codecs",
            "unicodedata",
            "calendar",
            "locale",
            "gettext",
            "threading",
            "multiprocessing",
            "concurrent",
            "asyncio",
            "queue",
            "socket",
            "ssl",
            "select",
            "subprocess",
            "signal",
            "platform",
            "ctypes",
            "array",
            "weakref",
            "gc",
            "inspect",
            "dis",
            "traceback",
            "warnings",
        }
        stdlib_modules.update(common_stdlib)
        return stdlib_modules

    def _should_ignore_path(self, path: Path) -> bool:
        """检查路径是否应该被忽略"""
        path_str = str(path)

        # 检查目录模式
        for pattern in self.ignore_patterns:
            if pattern in path_str:
                return True

        # 检查是否为Python文件
        if path.is_file() and not path.suffix == ".py":
            return True

        return False

    def _is_third_party_module(self, module_name: str) -> bool:
        """判断是否为第三方模块"""
        top_level = module_name.split(".")[0]

        # 检查是否为标准库
        if top_level in self.stdlib_modules:
            return False

        # 简单检查是否为项目内部模块
        if top_level == "vibehacks":
            return False

        return True

    def analyze_imports(self, file_path: Path) -> Dict[str, Any]:
        """分析单个文件的导入语句"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except (UnicodeDecodeError, PermissionError):
            return {}

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return {}

        file_imports = defaultdict(
            lambda: {
                "functions": set(),
                "classes": set(),
                "modules": set(),
                "aliases": dict(),
            }
        )

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name
                    if self._is_third_party_module(module_name):
                        alias_name = alias.asname or module_name
                        file_imports[module_name]["modules"].add(module_name)
                        file_imports[module_name]["aliases"][alias_name] = module_name

            elif isinstance(node, ast.ImportFrom):
                if node.module and self._is_third_party_module(node.module):
                    # 获取顶级包名，例如 rich.table -> rich
                    top_level_module = node.module.split(".")[0]
                    full_module_name = node.module

                    for alias in node.names:
                        import_name = alias.name
                        alias_name = alias.asname or import_name

                        # 尝试判断是函数还是类
                        if import_name[0].isupper():
                            file_imports[top_level_module]["classes"].add(import_name)
                        else:
                            file_imports[top_level_module]["functions"].add(import_name)

                        file_imports[top_level_module]["aliases"][alias_name] = (
                            f"{full_module_name}.{import_name}"
                        )

        return dict(file_imports)

    def analyze_usage(self, file_path: Path) -> Dict[str, Counter]:
        """分析单个文件中的使用情况"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except (UnicodeDecodeError, PermissionError):
            return {}

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return {}

        usage_counter = defaultdict(
            lambda: {"functions": Counter(), "classes": Counter(), "modules": Counter()}
        )

        # 首先获取该文件的导入信息
        file_imports = self.analyze_imports(file_path)

        # 创建别名到原始名称的映射
        alias_to_original = {}
        for module_name, import_data in file_imports.items():
            alias_to_original.update(import_data["aliases"])

        # 遍历AST节点统计使用情况
        # 用集合记录已处理的节点，避免重复计数
        processed_nodes = set()

        for node in ast.walk(tree):
            # 优先处理 Attribute 节点 (如 ast.parse)
            if isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name):
                    base_name = node.value.id
                    attr_name = node.attr

                    if base_name in alias_to_original:
                        original_path = alias_to_original[base_name]
                        # 获取顶级包名
                        top_level_module = original_path.split(".")[0]
                        if attr_name[0].isupper():
                            usage_counter[top_level_module]["classes"][attr_name] += 1
                        else:
                            usage_counter[top_level_module]["functions"][attr_name] += 1

                        # 标记base_name节点已处理，避免重复计数
                        processed_nodes.add(id(node.value))

            elif isinstance(node, ast.Name):
                # 只处理未被Attribute节点处理过的Name节点
                if id(node) not in processed_nodes:
                    name = node.id
                    if name in alias_to_original:
                        original = alias_to_original[name]
                        if "." in original:
                            # 从完整路径中提取顶级包名和项目名
                            parts = original.split(".")
                            top_level_module = parts[0]
                            item_name = parts[-1]
                            if item_name[0].isupper():
                                usage_counter[top_level_module]["classes"][
                                    item_name
                                ] += 1
                            else:
                                usage_counter[top_level_module]["functions"][
                                    item_name
                                ] += 1
                        else:
                            # 获取顶级包名
                            top_level_module = original.split(".")[0]
                            usage_counter[top_level_module]["modules"][
                                top_level_module
                            ] += 1

        return dict(usage_counter)

    def analyze_project(self) -> Tuple[Dict, Dict]:
        """分析整个项目"""
        print(f"开始分析项目: {self.project_path}")

        python_files = []
        for py_file in self.project_path.rglob("*.py"):
            if not self._should_ignore_path(py_file):
                python_files.append(py_file)

        print(f"找到 {len(python_files)} 个Python文件")

        # 分析导入
        for i, file_path in enumerate(python_files, 1):
            print(
                f"分析文件 {i}/{len(python_files)}: {file_path.relative_to(self.project_path)}"
            )

            file_imports = self.analyze_imports(file_path)
            file_usage = self.analyze_usage(file_path)

            # 合并导入数据
            for module_name, import_data in file_imports.items():
                self.imports_data[module_name]["functions"].update(
                    import_data["functions"]
                )
                self.imports_data[module_name]["classes"].update(import_data["classes"])
                self.imports_data[module_name]["modules"].update(import_data["modules"])
                self.imports_data[module_name]["aliases"].update(import_data["aliases"])
                self.imports_data[module_name]["files"].add(
                    str(file_path.relative_to(self.project_path))
                )

            # 合并使用数据
            for module_name, usage_data in file_usage.items():
                self.usage_data[module_name]["functions"].update(
                    usage_data.get("functions", {})
                )
                self.usage_data[module_name]["classes"].update(
                    usage_data.get("classes", {})
                )
                self.usage_data[module_name]["modules"].update(
                    usage_data.get("modules", {})
                )

        # 计算总使用次数
        for module_name in self.usage_data:
            total = (
                sum(self.usage_data[module_name]["functions"].values())
                + sum(self.usage_data[module_name]["classes"].values())
                + sum(self.usage_data[module_name]["modules"].values())
            )
            self.usage_data[module_name]["total_usage"] = total

        return dict(self.imports_data), dict(self.usage_data)
