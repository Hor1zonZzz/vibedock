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
        """Generate prompt for LLM to create HTML report"""
        prompt = f"""
Please generate a professional HTML learning path report based on the following documents. This is the core output of VibeDock's AI-driven intelligent adaptation system.

## Design Requirements (White Premium Style):
1. **Modern Minimalist Design**: Pure white background + light gray sections, showcasing clean professionalism
2. **High-end Visual Effects**: Delicate shadows (0 2px 8px rgba(0,0,0,0.06)), rounded cards, subtle gradient borders
3. **Refined Color Scheme**:
   - Primary: #2563eb (blue) #059669 (green)
   - Secondary: #64748b (gray text) #f8fafc (background gray)
   - Accent: #dc2626 (warning red) #7c3aed (purple highlight)
4. **Elegant Typography**: Inter, -apple-system, 'Segoe UI', sans-serif
5. **Micro-interactions**: Hover lift effects, smooth transitions, delicate animations

## Layout Structure:
- **Top Header**: VibeDock branding + generation timestamp
- **Side Navigation**: Fixed navigation bar with smooth anchor scrolling
- **Main Content Area**: Card-based layout with modular content

## Core Feature Modules:

1. **Personalized Gap Analysis Dashboard**
   - Knowledge gap scoring cards (circular progress bars)
   - Skills radar chart (using Chart.js)
   - Priority-sorted list (colored tags)

2. **Intelligent Learning Path Recommendations**
   - Each gap provides 3-5 curated learning resources
   - Resource cards: icon + title + description + difficulty tag
   - Beautiful "Start Learning" buttons (rounded + gradient + hover effects)
   - Support for official docs, video tutorials, GitHub project links

3. **Project Tech Stack Insights**
   - Tech stack tag cloud
   - Dependency tree diagram
   - Core component description cards

4. **30-Day Learning Path Planning**
   - Timeline-style learning schedule
   - Milestone node markers
   - Progress tracking checkboxes

## UI Component Standards:
- **Buttons**: 8px radius, gradient background, hover shadows
- **Cards**: White background, border-radius: 12px, gentle box-shadow
- **Tags**: Small radius, light background, dark text
- **Icons**: Use Lucide Icons or Heroicons
- **Spacing**: 16px base spacing, 24px section spacing

## Interactive Experience:
- Hover effects: Card slight lift + shadow deepening
- Button interactions: Background gradient + slight scaling
- Smooth scroll navigation
- Responsive design (mobile-friendly)

## Data Sources:

### User Knowledge Gap Analysis:
{gap_content}

### Project Tech Stack Analysis:
{report_content}

Please generate a complete HTML file with the following requirements:
- Modern white minimalist style, avoid dark/purple themes
- Inline CSS (CSS variables + Grid/Flexbox layout)
- Chart.js data visualization
- Smooth interactive animations
- Report title: "VibeDock 智能学习路径报告"
- Ensure all learning resources have clickable beautiful buttons
- **IMPORTANT: All content in the HTML report must be in Chinese language**

Focus: White premium feel + actionability, allowing users to see action paths at a glance.
"""
        return prompt

    def call_llm(self, prompt):
        """调用大模型生成HTML内容"""
        try:
            print("🤖 正在生成高端智能学习路径报告...")
            
            system_prompt = """You are the core HTML architect of VibeDock's AI-driven intelligent adaptation system.

Your expertise:
- Creating modern web interfaces with premium feel and technological sophistication
- Mastering CSS Grid, Flexbox, CSS variables, and modern animations
- Specializing in personalized learning paths and gap analysis dashboards
- Familiar with data visualization and interaction design principles

Design principles:
- Minimalist yet sophisticated, pursuing ultimate visual experience
- Every UI element has clear functionality and interactive feedback
- Color schemes reflect professionalism and futuristic feel
- Clear information architecture that guides users to take action

Output requirements:
- Generate complete HTML files with all CSS and JavaScript
- Ensure all learning resources have clickable action buttons
- Clear code structure with comprehensive comments
- Responsive design compatible with various devices
- **CRITICAL: All text content in the generated HTML must be in Chinese language**"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
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
        filename = f'output/VibeDock_智能学习路径_{timestamp}.html'

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