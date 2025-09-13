"""
命令行接口 - VibehHacks Python代码库分析工具
"""

import click
from pathlib import Path
from .analyzer import ImportAnalyzer
from .reporter import AnalysisReporter


@click.command()
@click.argument('project_path', type=click.Path(exists=True, path_type=Path))
@click.option('--output-markdown', '-md', type=str, help='导出Markdown报告到指定文件')
@click.option('--package', '-p', type=str, help='显示特定包的详细信息')
@click.option('--quiet', '-q', is_flag=True, help='静默模式，只输出结果')
def analyze(project_path, output_markdown, package, quiet):
    """
    分析Python项目中第三方包的导入和使用情况
    
    PROJECT_PATH: Python项目的根目录路径
    """
    if not quiet:
        click.echo(f"开始分析Python项目: {project_path}")
    
    # 创建分析器并执行分析
    analyzer = ImportAnalyzer(str(project_path))
    imports_data, usage_data = analyzer.analyze_project()
    
    if not imports_data:
        click.echo("未找到任何第三方包导入")
        return
    
    # 创建报告生成器
    reporter = AnalysisReporter(imports_data, usage_data)
    
    if not quiet:
        # 显示详细报告
        reporter.print_detailed_report()
        
        # 显示特定包的详细信息
        if package:
            if package in imports_data:
                reporter.print_package_details(package)
            else:
                click.echo(f"未找到包: {package}")
        else:
            # 显示前5个最常用包的详细信息
            reporter.print_package_details()
    
    # 导出markdown报告
    if output_markdown:
        reporter.export_to_markdown(output_markdown)
    
    if not quiet:
        click.echo("分析完成!")


@click.group()
def main():
    """VibehHacks - Python代码库分析工具"""
    pass


main.add_command(analyze)


if __name__ == '__main__':
    main()