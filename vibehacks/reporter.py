"""
报告生成器 - 生成分析结果的详细报告
"""

import json
from pathlib import Path
from typing import Dict

import pandas as pd
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


class AnalysisReporter:
    """分析结果报告生成器"""

    def __init__(self, imports_data: Dict, usage_data: Dict):
        self.imports_data = imports_data
        self.usage_data = usage_data
        self.console = Console()

    def generate_summary_report(self) -> str:
        """生成摘要报告"""
        total_packages = len(self.imports_data)
        total_functions = sum(
            len(data["functions"]) for data in self.imports_data.values()
        )
        total_classes = sum(len(data["classes"]) for data in self.imports_data.values())
        total_usage = sum(
            data.get("total_usage", 0) for data in self.usage_data.values()
        )

        summary = f"""
# Python项目第三方包分析报告

## 总体统计
- 第三方包总数: {total_packages}
- 导入函数总数: {total_functions}
- 导入类总数: {total_classes}
- 总使用次数: {total_usage}

## 最常用的包 (按使用次数排序)
"""

        # 按使用次数排序包
        sorted_packages = sorted(
            self.usage_data.items(),
            key=lambda x: x[1].get("total_usage", 0),
            reverse=True,
        )

        for i, (package, usage) in enumerate(sorted_packages[:20], 1):
            total_usage = usage.get("total_usage", 0)
            summary += f"{i}. {package}: {total_usage} 次使用\n"

        return summary

    def print_detailed_report(self):
        """打印详细的控制台报告"""
        self.console.print(Panel.fit("Python项目第三方包分析报告", style="bold blue"))

        # 总体统计
        stats_table = Table(title="总体统计", box=box.ROUNDED)
        stats_table.add_column("指标", style="cyan")
        stats_table.add_column("数量", style="magenta")

        total_packages = len(self.imports_data)
        total_functions = sum(
            len(data["functions"]) for data in self.imports_data.values()
        )
        total_classes = sum(len(data["classes"]) for data in self.imports_data.values())
        total_usage = sum(
            data.get("total_usage", 0) for data in self.usage_data.values()
        )

        stats_table.add_row("第三方包总数", str(total_packages))
        stats_table.add_row("导入函数总数", str(total_functions))
        stats_table.add_row("导入类总数", str(total_classes))
        stats_table.add_row("总使用次数", str(total_usage))

        self.console.print(stats_table)
        self.console.print()

        # 最常用的包
        usage_table = Table(title="最常用的包 (Top 20)", box=box.ROUNDED)
        usage_table.add_column("排名", style="cyan", width=6)
        usage_table.add_column("包名", style="green")
        usage_table.add_column("使用次数", style="magenta")
        usage_table.add_column("导入函数数", style="yellow")
        usage_table.add_column("导入类数", style="blue")

        sorted_packages = sorted(
            self.usage_data.items(),
            key=lambda x: x[1].get("total_usage", 0),
            reverse=True,
        )

        for i, (package, usage) in enumerate(sorted_packages[:20], 1):
            total_usage = usage.get("total_usage", 0)
            func_count = len(self.imports_data.get(package, {}).get("functions", set()))
            class_count = len(self.imports_data.get(package, {}).get("classes", set()))

            usage_table.add_row(
                str(i), package, str(total_usage), str(func_count), str(class_count)
            )

        self.console.print(usage_table)
        self.console.print()

    def print_package_details(self, package_name: str = None):
        """打印特定包的详细信息"""
        if package_name:
            packages_to_show = (
                [package_name] if package_name in self.imports_data else []
            )
        else:
            # 显示使用次数最多的前5个包的详细信息
            sorted_packages = sorted(
                self.usage_data.items(),
                key=lambda x: x[1].get("total_usage", 0),
                reverse=True,
            )
            packages_to_show = [pkg[0] for pkg in sorted_packages[:5]]

        for package in packages_to_show:
            import_data = self.imports_data.get(package, {})
            usage_data = self.usage_data.get(package, {})

            self.console.print(Panel.fit(f"{package} 详细信息", style="bold green"))

            # 基本信息
            info_table = Table(box=box.SIMPLE)
            info_table.add_column("属性", style="cyan")
            info_table.add_column("值", style="white")

            info_table.add_row("总使用次数", str(usage_data.get("total_usage", 0)))
            info_table.add_row("使用文件数", str(len(import_data.get("files", set()))))
            info_table.add_row(
                "导入函数数", str(len(import_data.get("functions", set())))
            )
            info_table.add_row("导入类数", str(len(import_data.get("classes", set()))))

            self.console.print(info_table)

            # 函数使用情况
            if usage_data.get("functions"):
                func_table = Table(title="函数使用情况", box=box.ROUNDED)
                func_table.add_column("函数名", style="yellow")
                func_table.add_column("使用次数", style="magenta")

                sorted_funcs = sorted(
                    usage_data["functions"].items(), key=lambda x: x[1], reverse=True
                )

                for func_name, count in sorted_funcs[:20]:  # 显示前20个
                    func_table.add_row(func_name, str(count))

                self.console.print(func_table)

            # 类使用情况
            if usage_data.get("classes"):
                class_table = Table(title="类使用情况", box=box.ROUNDED)
                class_table.add_column("类名", style="blue")
                class_table.add_column("使用次数", style="magenta")

                sorted_classes = sorted(
                    usage_data["classes"].items(), key=lambda x: x[1], reverse=True
                )

                for class_name, count in sorted_classes[:20]:  # 显示前20个
                    class_table.add_row(class_name, str(count))

                self.console.print(class_table)

            # 使用文件列表
            if import_data.get("files"):
                files_text = Text("使用文件:\n", style="bold cyan")
                for file_path in sorted(import_data["files"]):
                    files_text.append(f"  - {file_path}\n", style="white")

                self.console.print(Panel(files_text, box=box.ROUNDED))

            self.console.print()

    def export_to_json(self, output_path: str):
        """导出分析结果到JSON文件"""
        # 转换set为list以便JSON序列化
        json_data = {
            "imports": {},
            "usage": self.usage_data,
            "summary": {
                "total_packages": len(self.imports_data),
                "total_functions": sum(
                    len(data["functions"]) for data in self.imports_data.values()
                ),
                "total_classes": sum(
                    len(data["classes"]) for data in self.imports_data.values()
                ),
                "total_usage": sum(
                    data.get("total_usage", 0) for data in self.usage_data.values()
                ),
            },
        }

        for package, data in self.imports_data.items():
            json_data["imports"][package] = {
                "functions": list(data["functions"]),
                "classes": list(data["classes"]),
                "modules": list(data["modules"]),
                "aliases": data["aliases"],
                "files": list(data["files"]),
            }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        self.console.print(f"分析结果已导出到: {output_path}")

    def export_to_csv(self, output_dir: str):
        """导出分析结果到CSV文件"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # 导出包使用统计
        packages_data = []
        for package, usage in self.usage_data.items():
            import_data = self.imports_data.get(package, {})
            packages_data.append(
                {
                    "package": package,
                    "total_usage": usage.get("total_usage", 0),
                    "function_count": len(import_data.get("functions", set())),
                    "class_count": len(import_data.get("classes", set())),
                    "file_count": len(import_data.get("files", set())),
                }
            )

        df_packages = pd.DataFrame(packages_data)
        df_packages.to_csv(
            output_path / "packages_summary.csv", index=False, encoding="utf-8"
        )

        # 导出函数使用详情
        functions_data = []
        for package, usage in self.usage_data.items():
            for func_name, count in usage.get("functions", {}).items():
                functions_data.append(
                    {"package": package, "function": func_name, "usage_count": count}
                )

        if functions_data:
            df_functions = pd.DataFrame(functions_data)
            df_functions.to_csv(
                output_path / "functions_usage.csv", index=False, encoding="utf-8"
            )

        # 导出类使用详情
        classes_data = []
        for package, usage in self.usage_data.items():
            for class_name, count in usage.get("classes", {}).items():
                classes_data.append(
                    {"package": package, "class": class_name, "usage_count": count}
                )

        if classes_data:
            df_classes = pd.DataFrame(classes_data)
            df_classes.to_csv(
                output_path / "classes_usage.csv", index=False, encoding="utf-8"
            )

        self.console.print(f"CSV报告已导出到: {output_path}")

    def export_to_markdown(self, output_path: str):
        """导出分析结果到Markdown文件"""
        # 计算统计数据
        total_packages = len(self.imports_data)
        total_functions = sum(
            len(data["functions"]) for data in self.imports_data.values()
        )
        total_classes = sum(len(data["classes"]) for data in self.imports_data.values())
        total_usage = sum(
            data.get("total_usage", 0) for data in self.usage_data.values()
        )

        # 构建markdown内容
        markdown_content = f"""# Python项目第三方包分析报告

## 📊 总体统计

| 指标 | 数量 |
|------|------|
| 第三方包总数 | {total_packages} |
| 导入函数总数 | {total_functions} |
| 导入类总数 | {total_classes} |
| 总使用次数 | {total_usage} |

## 🏆 最常用的包 (Top 20)

| 排名 | 包名 | 使用次数 | 导入函数数 | 导入类数 |
|------|------|----------|------------|----------|
"""

        # 添加最常用包的排行
        sorted_packages = sorted(
            self.usage_data.items(),
            key=lambda x: x[1].get("total_usage", 0),
            reverse=True,
        )

        for i, (package, usage) in enumerate(sorted_packages[:20], 1):
            total_usage_count = usage.get("total_usage", 0)
            func_count = len(self.imports_data.get(package, {}).get("functions", set()))
            class_count = len(self.imports_data.get(package, {}).get("classes", set()))

            markdown_content += f"| {i} | {package} | {total_usage_count} | {func_count} | {class_count} |\n"

        # 添加详细包信息
        markdown_content += "\n## 📦 包详细信息\n\n"

        # 显示使用次数最多的前5个包的详细信息
        for package, _ in sorted_packages[:5]:
            import_data = self.imports_data.get(package, {})
            usage_data = self.usage_data.get(package, {})

            markdown_content += f"### {package}\n\n"
            markdown_content += "**基本信息:**\n"
            markdown_content += f"- 总使用次数: {usage_data.get('total_usage', 0)}\n"
            markdown_content += (
                f"- 使用文件数: {len(import_data.get('files', set()))}\n"
            )
            markdown_content += (
                f"- 导入函数数: {len(import_data.get('functions', set()))}\n"
            )
            markdown_content += (
                f"- 导入类数: {len(import_data.get('classes', set()))}\n\n"
            )

            # 函数使用情况
            if usage_data.get("functions"):
                markdown_content += "**🔧 函数使用情况:**\n\n"
                markdown_content += "| 函数名 | 使用次数 |\n"
                markdown_content += "|--------|----------|\n"

                sorted_funcs = sorted(
                    usage_data["functions"].items(), key=lambda x: x[1], reverse=True
                )

                for func_name, count in sorted_funcs[:20]:
                    markdown_content += f"| {func_name} | {count} |\n"
                markdown_content += "\n"

            # 类使用情况
            if usage_data.get("classes"):
                markdown_content += "**🏗️ 类使用情况:**\n\n"
                markdown_content += "| 类名 | 使用次数 |\n"
                markdown_content += "|------|----------|\n"

                sorted_classes = sorted(
                    usage_data["classes"].items(), key=lambda x: x[1], reverse=True
                )

                for class_name, count in sorted_classes[:20]:
                    markdown_content += f"| {class_name} | {count} |\n"
                markdown_content += "\n"

            # 使用文件列表
            if import_data.get("files"):
                markdown_content += "**📁 使用文件:**\n\n"
                for file_path in sorted(import_data["files"]):
                    markdown_content += f"- {file_path}\n"
                markdown_content += "\n"

            markdown_content += "---\n\n"

        # 写入文件
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        self.console.print(f"Markdown报告已导出到: {output_path}")
