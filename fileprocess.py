import os
import re

from gitingest import ingest

from vibehacks.analyzer import ImportAnalyzer
from vibehacks.reporter import AnalysisReporter


def generate_analysis_report(project_path=".", output_file="report.md"):
    """
    分析项目并生成Markdown格式的报告

    Args:
        project_path (str): 要分析的项目路径，默认为当前目录
        output_file (str): 输出文件名，默认为report.md

    Returns:
        bool: 是否成功生成报告
    """
    try:
        # 创建分析器并运行分析
        analyzer = ImportAnalyzer(project_path)
        imports_data, usage_data = analyzer.analyze_project()

        # 创建报告生成器并生成报告
        reporter = AnalysisReporter(imports_data, usage_data)
        reporter.export_to_markdown(output_file)

        return True

    except Exception as e:
        print(f"  ⚠ 分析失败: {e}")
        return False


def load_report():
    """
    加载report.md文件内容作为变量

    Returns:
        str: report.md文件内容，如果加载失败则返回None
    """
    try:
        with open("report.md", "r", encoding="utf-8") as f:
            report_content = f.read()
        return report_content
    except FileNotFoundError:
        print("  ⚠ 报告文件未找到")
        return None
    except Exception as e:
        print(f"  ⚠ 报告加载失败: {e}")
        return None


def extract_json_from_response(response_text):
    """
    从AI响应中提取XML内容并转换为JSON格式

    Args:
        response_text (str): AI的响应文本

    Returns:
        dict: 转换后的JSON数据，如果解析失败返回None
    """
    try:
        import xml.etree.ElementTree as ET

        # 使用正则表达式查找XML代码块
        xml_pattern = r"```xml\s*(.*?)\s*```"
        match = re.search(xml_pattern, response_text, re.DOTALL)

        if match:
            xml_str = match.group(1).strip()
            # 解析XML
            root = ET.fromstring(xml_str)

            # 转换为JSON格式
            libraries = []
            for library in root.findall("library"):
                lib_data = {
                    "name": library.find("name").text
                    if library.find("name") is not None
                    else "",
                    "github_url": library.find("github_url").text
                    if library.find("github_url") is not None
                    else "",
                    "description": library.find("description").text
                    if library.find("description") is not None
                    else "",
                }
                libraries.append(lib_data)

            return {"third_party_libraries": libraries}
        else:
            return None

    except ET.ParseError as e:
        print(f"  ⚠ 响应解析异常: {e}")
        return None
    except Exception as e:
        print(f"  ⚠ 数据提取异常: {e}")
        return None


def analyze_and_get_libraries_info(project_path=".", output_file="report.md"):
    """
    分析项目并使用AI获取第三方库的详细信息

    Args:
        project_path (str): 要分析的项目路径
        output_file (str): 报告输出文件名

    Returns:
        dict: 包含分析结果和库信息的字典
    """
    # 首先生成分析报告
    success = generate_analysis_report(project_path, output_file)
    if not success:
        return None

    # 加载生成的报告
    report_content = load_report() if output_file == "report.md" else None
    if not report_content and output_file != "report.md":
        try:
            with open(output_file, "r", encoding="utf-8") as f:
                report_content = f.read()
        except Exception as e:
            print(f"[错误] 无法读取报告文件: {e}")
            return None

    if not report_content:
        return None

    # 构造AI提示词
    prompt = f"""
请分析以下Python项目的第三方包使用报告，为每个第三方包提供详细信息。

{report_content}

请以JSON格式返回结果，包含以下字段：
- name: 包名
- github_url: GitHub仓库地址
- description: 包的简短描述

请只返回JSON格式，不要添加额外说明。格式如下：
```json
{{
  "third_party_libraries": [
    {{
      "name": "包名",
      "github_url": "https://github.com/...",
      "description": "包的描述"
    }}
  ]
}}
```
"""

    # 发送AI请求
    ai_response = send_ai_request(prompt, max_tokens=2048)

    if not ai_response:
        print("  ⚠ AI分析失败")
        return None

    # 解析JSON响应
    libraries_info = extract_json_from_response(ai_response)

    return {
        "report_content": report_content,
        "libraries_info": libraries_info,
        "ai_response": ai_response,
    }


def get_repo_context(github_url, repo_name):
    """
    获取单个仓库的上下文信息并保存到对应文件夹

    Args:
        github_url (str): GitHub仓库URL
        repo_name (str): 仓库名称，用作文件夹名
    """
    try:
        summary, tree, content = ingest(github_url)

        # 为每个仓库创建独立的输出目录
        output_dir = os.path.join("output", repo_name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 将三个字符串分别保存到txt文件
        files_data = {"summary.txt": summary, "tree.txt": tree, "content.txt": content}

        for filename, data in files_data.items():
            filepath = os.path.join(output_dir, filename)
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(data)
            except Exception as e:
                print(f"  ⚠ {repo_name} 保存异常: {e}")

        return summary, tree, content
    except Exception as e:
        print(f"  ⚠ {repo_name} 获取失败")
        return None, None, None


async def get_all_repos_context(github_links):
    """
    异步获取所有GitHub仓库的上下文信息

    Args:
        github_links (list): GitHub链接列表
    """
    import asyncio

    async def process_repo(github_url):
        # 从URL提取仓库名称
        repo_name = github_url.split("/")[-1]
        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]

        # 在线程中运行同步的ingest函数
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, get_repo_context, github_url, repo_name)

    # 创建主输出目录
    if not os.path.exists("output"):
        os.makedirs("output")

    # 并发处理所有仓库
    tasks = [process_repo(url) for url in github_links]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    return results


# AI配置信息 - 从环境变量读取
import os
from dotenv import load_dotenv

load_dotenv()

AI_CONFIG = {
    "api_key": os.getenv("API_KEY"),
    "base_url": os.getenv("BASE_URL"),
    "model": os.getenv("MODEL"),
    "default_max_tokens": 4096,
}


def send_ai_request(prompt, max_tokens=None, system_message=None):
    """
    发送AI请求的通用函数

    Args:
        prompt (str): 用户提示词
        max_tokens (int, optional): 最大token数，默认使用配置中的值
        system_message (str, optional): 系统消息

    Returns:
        str: AI响应内容
    """
    try:
        from openai import OpenAI
        
        # 初始化OpenAI兼容客户端
        client = OpenAI(
            api_key=AI_CONFIG["api_key"],
            base_url=AI_CONFIG["base_url"],
        )

        # 准备消息列表
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        # 发送请求
        response = client.chat.completions.create(
            model=AI_CONFIG["model"],
            max_tokens=max_tokens or AI_CONFIG["default_max_tokens"],
            messages=messages,
        )

        # 提取响应内容
        return response.choices[0].message.content

    except Exception as e:
        return None


async def run_complete_analysis(project_path=".", output_file="report.md"):
    """
    运行完整的项目分析流程

    Args:
        project_path (str): 要分析的项目路径，默认为当前目录
        output_file (str): 输出文件名，默认为report.md

    Returns:
        list: GitHub链接列表
    """
    # 使用默认参数
    project_path = "."
    output_file = "report.md"

    # 生成项目分析报告并获取库信息
    result = analyze_and_get_libraries_info(project_path, output_file)

    # 加载report.md内容
    report_content = load_report()
    prompt = f"""
这个是一个Python项目的依赖分析报告，内容如下：
{report_content}
请基于以上内容，帮我生成用户如果维护需要了解的第三方库的GitHub链接
输出格式仅限xml标签，不允许输出除xml其他任何内容
示例输出：
```xml
<third_party_libraries>
  <library>
    <name>rich</name>
    <github_url>https://github.com/Textualize/rich</github_url>
    <description>Rich text and beautiful formatting in the terminal</description>
  </library>
  <library>
    <name>click</name>
    <github_url>https://github.com/pallets/click</github_url>
    <description>Python composable command line interface toolkit</description>
  </library>
  <library>
    <name>pandas</name>
    <github_url>https://github.com/pandas-dev/pandas</github_url>
    <description>Powerful data structures for data analysis, time series, and statistics</description>
  </library>
  <library>
    <name>anthropic</name>
    <github_url>https://github.com/anthropics/anthropic-sdk-python</github_url>
    <description>The official Python library for the Anthropic API</description>
  </library>
  <library>
    <name>gitingest</name>
    <github_url>https://github.com/cyclotruc/gitingest</github_url>
    <description>Turn any Git repository into a prompt-friendly text ingest for LLMs</description>
  </library>
</third_party_libraries>
```
"""
    response = send_ai_request(prompt, max_tokens=1024)

    json_data = extract_json_from_response(response)
    github_links = []

    if json_data and "third_party_libraries" in json_data:
        for lib in json_data["third_party_libraries"]:
            github_links.append(lib["github_url"])

    # 移除调试输出

    # 异步获取所有仓库上下文
    await get_all_repos_context(github_links)

    return github_links


# 测试函数
if __name__ == "__main__":
    # 让用户输入项目路径
    project_path = input("请输入要分析的项目路径 (直接回车使用当前目录): ").strip()
    if not project_path:
        project_path = "."

    # 让用户输入输出文件名
    output_file = input("请输入输出文件名 (直接回车使用 report.md): ").strip()
    if not output_file:
        output_file = "report.md"

    run_complete_analysis(project_path, output_file)
