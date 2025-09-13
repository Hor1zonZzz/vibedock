import os
import webbrowser
from datetime import datetime
from dotenv import load_dotenv
import openai

load_dotenv()

class HTMLReportGenerator:
    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        self.base_url = os.getenv('BASE_URL')
        self.model = os.getenv('MODEL')

        if not all([self.api_key, self.base_url, self.model]):
            raise ValueError("Missing required environment variables: API_KEY, BASE_URL, MODEL")

        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def read_markdown_files(self):
        """读取 gap_summary.md 和 report.md 文件内容"""
        gap_content = ""
        report_content = ""

        try:
            with open('gap_summary.md', 'r', encoding='utf-8') as f:
                gap_content = f.read()
        except FileNotFoundError:
            print("⚠️ gap_summary.md 文件未找到")

        try:
            with open('report.md', 'r', encoding='utf-8') as f:
                report_content = f.read()
        except FileNotFoundError:
            print("⚠️ report.md 文件未找到")

        return gap_content, report_content

    def generate_html_prompt(self, gap_content, report_content):
        """生成用于大模型的提示词"""
        prompt = f"""
请基于以下两个文档的内容，生成一份精美的HTML报告，要求：

1. 使用现代的响应式设计，包含CSS样式
2. 报告应该包含清晰的标题、导航和章节
3. 使用适当的颜色主题和图标
4. 将知识差距分析和技术栈分析整合到一个连贯的报告中
5. 添加图表或可视化元素（使用Chart.js或类似库）
6. 确保报告在浏览器中显示良好

## 用户知识差距分析（gap_summary.md）：
{gap_content}

## 项目技术栈分析（report.md）：
{report_content}

请生成完整的HTML文件内容，包含内联CSS和JavaScript。报告标题可以是"技术栈学习路径与项目分析报告"。
"""
        return prompt

    def call_llm(self, prompt):
        """调用大模型生成HTML内容"""
        try:
            print("🤖 正在调用大模型生成HTML报告...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的技术报告生成专家，擅长创建美观的HTML报告。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ 调用大模型失败: {e}")
            return None

    def save_html_report(self, html_content):
        """保存HTML报告到文件"""
        if not os.path.exists('output'):
            os.makedirs('output')

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'output/tech_report_{timestamp}.html'

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ HTML报告已保存: {filename}")
            return filename
        except Exception as e:
            print(f"❌ 保存HTML文件失败: {e}")
            return None

    def open_in_browser(self, filename):
        """在浏览器中打开HTML报告"""
        try:
            abs_path = os.path.abspath(filename)
            webbrowser.open(f'file://{abs_path}')
            print(f"🌐 已在浏览器中打开报告: {abs_path}")
        except Exception as e:
            print(f"❌ 打开浏览器失败: {e}")

    def generate_and_display_report(self):
        """完整的报告生成流程"""
        print("\n🎯 开始生成HTML报告...")

        # 读取markdown文件
        gap_content, report_content = self.read_markdown_files()

        if not gap_content and not report_content:
            print("❌ 无法读取任何源文件，无法生成报告")
            return False

        # 生成提示词
        prompt = self.generate_html_prompt(gap_content, report_content)

        # 调用大模型
        html_content = self.call_llm(prompt)

        if not html_content:
            print("❌ 无法生成HTML内容")
            return False

        # 保存文件
        filename = self.save_html_report(html_content)

        if not filename:
            return False

        # 在浏览器中打开
        self.open_in_browser(filename)

        return True

async def generate_html_report():
    """异步包装函数，用于在main.py中调用"""
    generator = HTMLReportGenerator()
    return generator.generate_and_display_report()

if __name__ == "__main__":
    import asyncio
    asyncio.run(generate_html_report())