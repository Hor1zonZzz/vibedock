import asyncio
from tech_stack_questionnaire import run_questionnaire
import fileprocess

async def main():
    """Main entry point for the Tech Stack Questionnaire application"""
    # First run the complete analysis to generate report
    await fileprocess.run_complete_analysis()

    results = await run_questionnaire('report.md')

    # Display results summary if available
    if results:
        print("\n✅ Assessment completed successfully!")
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
        print("\n❌ Assessment could not be completed.")

if __name__ == "__main__":
    asyncio.run(main())