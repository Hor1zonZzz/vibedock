import asyncio
from tech_stack_questionnaire import run_questionnaire
import fileprocess
from html_report_generator import generate_html_report

async def main():
    """Main entry point for the Tech Stack Questionnaire application"""
    print("🚀 开始三阶段分析流程...")

    # Stage 1: Run complete analysis to generate report
    print("\n📊 阶段1: 生成项目技术栈分析报告")
    await fileprocess.run_complete_analysis()

    # Stage 2: Run questionnaire based on report
    print("\n❓ 阶段2: 运行知识差距问卷调查")
    results = await run_questionnaire('report.md')

    # Display stage 2 results summary if available
    if results:
        print("\n✅ 第二阶段评估完成!")
        if 'user_purpose' in results:
            print(f"📋 Purpose: {results['user_purpose']}")
        if 'questions_count' in results:
            print(f"❓ Questions: {results['questions_count']}")
        if 'gaps_count' in results:
            print(f"🎯 Gaps identified: {results['gaps_count']}")
        if 'qa_record' in results:
            print(f"📄 Q&A Record: {results['qa_record']}")
        if 'gap_report' in results:
            print(f"📊 Gap Report: {results['gap_report']}")
    else:
        print("\n❌ 第二阶段评估无法完成.")

    # Stage 3: Generate HTML report and open in browser
    print("\n🎨 阶段3: 生成HTML报告并在浏览器中打开")
    html_success = await generate_html_report()

    if html_success:
        print("\n🎉 所有三个阶段都已成功完成!")
    else:
        print("\n⚠️ HTML报告生成失败，但前两个阶段已完成")

if __name__ == "__main__":
    asyncio.run(main())