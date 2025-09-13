import asyncio
from tech_stack_questionnaire import run_questionnaire
import fileprocess
from html_report_generator import generate_html_report

async def main():
    """VibeDock - AI-Driven Intelligent Adaptation Engine"""
    print("\n" + "─" * 60)
    print(" VibeDock | AI驱动的智能适配引擎")
    print(" 重新定义项目理解与技术栈学习")
    print("─" * 60)
    
    # Stage 1: Technical Stack Analysis
    print("\n→ 智能项目分析")
    await fileprocess.run_complete_analysis()
    
    # Stage 2: Personalized Gap Analysis
    print("\n→ 个性化差距评估")
    results = await run_questionnaire('report.md')
    
    if results:
        print("  ✓ 适配完成")
        if 'gaps_count' in results:
            print(f"  • 识别 {results['gaps_count']} 个关键学习点")
        if 'user_purpose' in results:
            purpose_brief = results['user_purpose'].split(' - ')[0] if ' - ' in results['user_purpose'] else results['user_purpose']
            print(f"  • 目标导向: {purpose_brief}")
    else:
        print("  ⚠ 评估中断")
    
    # Stage 3: Knowledge Visualization
    print("\n→ 知识图谱生成")
    html_success = await generate_html_report()
    
    print("\n" + "─" * 60)
    if html_success:
        print(" 智能适配完成 | 个性化学习路径已就绪")
    else:
        print(" 核心分析完成 | 可视化报告生成异常")
    print("─" * 60)

if __name__ == "__main__":
    asyncio.run(main())