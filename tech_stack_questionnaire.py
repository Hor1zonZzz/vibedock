"""
Tech Stack Questionnaire Library

A comprehensive library for analyzing technical skill gaps based on project tech stack usage
and user proficiency assessment.
"""

import asyncio
import os
from typing import Dict, Optional
from rich.console import Console
from stage1_processor import UniversalStage1Processor
from stage2_processor import UniversalStage2Processor


class TechStackQuestionnaire:
    """Main class for conducting tech stack questionnaire and gap analysis"""
    
    def __init__(self, input_file: str = 'report.md'):
        self.console = Console()
        self.input_file = input_file
        self.stage1 = UniversalStage1Processor()
        self.stage2 = UniversalStage2Processor()
        
    async def run_full_assessment(self) -> Dict[str, str]:
        """
        Run the complete assessment process:
        1. Ask user purpose
        2. Generate and collect question answers
        3. Generate gap assessment report
        
        Returns:
            Dict containing file paths of generated reports
        """
        
        self.console.print("[bold green]Starting the Tech Stack Questionnaire...[/bold green]")
        
        # Show current configuration
        self.console.print(f"[dim]Using API: {os.getenv('BASE_URL')}[/dim]")
        self.console.print(f"[dim]Model: {os.getenv('MODEL')}[/dim]")

        # Check input file
        if not os.path.exists(self.input_file):
            self.console.print(f"[bold red]Error: Input file '{self.input_file}' not found.[/bold red]")
            return {}

        # Read input markdown
        with open(self.input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Get user purpose
        user_purpose = self.stage1.ask_user_purpose()
        self.console.print(f"[dim]Your purpose: {user_purpose}[/dim]")

        # Stage 1: Generate questions and collect answers
        self.console.print("[bold blue]--- Stage 1: Technical Skills Assessment ---[/bold blue]")
        
        try:
            # Generate questions
            self.console.print("Generating tailored questions from tech stack analysis...")
            questions = await self.stage1.generate_questions(markdown_content)
            
            if not questions:
                self.console.print("[bold red]Could not generate any questions from the document.[/bold red]")
                return {}
            
            self.console.print(f"[bold green]Generated {len(questions)} questions[/bold green]")
            
            # Collect answers
            answers = self.stage1.collect_answers(questions)
            qa_markdown = self.stage1.format_qa_markdown(answers)
            
            # Save Q&A record
            qa_file = 'qa_record.md'
            with open(qa_file, 'w', encoding='utf-8') as f:
                f.write(qa_markdown)
            self.console.print(f"[bold green]Q&A record saved to '{qa_file}'[/bold green]")
            
        except Exception as e:
            self.console.print(f"[bold red]Stage 1 failed: {str(e)}[/bold red]")
            return {}

        # Stage 2: Generate gap assessment report
        self.console.print("[bold blue]--- Stage 2: Personalized Gap Analysis ---[/bold blue]")
        
        try:
            self.console.print("Analyzing gaps and generating personalized recommendations...")
            report = await self.stage2.generate_gap_report(markdown_content, qa_markdown, user_purpose)
            
            if not report:
                self.console.print("[bold red]Could not generate the gap assessment report.[/bold red]")
                return {'qa_record': qa_file}
            
            # Format and save report
            gap_report_md = self.stage2.format_gap_report(report)
            report_file = 'gap_summary.md'
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(gap_report_md)
            self.console.print(f"[bold green]Gap assessment report saved to '{report_file}'[/bold green]")
            
            # Show summary
            self.console.print("\n[bold cyan]--- Assessment Complete ---[/bold cyan]")
            self.console.print(f"✅ Questions answered: {len(questions)}")
            self.console.print(f"✅ Gaps identified: {len(report.get('gaps', []))}")
            self.console.print(f"✅ Purpose-focused analysis: {user_purpose.split(' - ')[0]}")
            self.console.print(f"📁 Files generated: {qa_file}, {report_file}")
            
            return {
                'qa_record': qa_file,
                'gap_report': report_file,
                'user_purpose': user_purpose,
                'questions_count': len(questions),
                'gaps_count': len(report.get('gaps', []))
            }
            
        except Exception as e:
            self.console.print(f"[bold red]Stage 2 failed: {str(e)}[/bold red]")
            return {'qa_record': qa_file}

    async def run_stage1_only(self) -> Optional[str]:
        """Run only stage 1 (questions and answers collection)"""
        
        if not os.path.exists(self.input_file):
            self.console.print(f"[bold red]Error: Input file '{self.input_file}' not found.[/bold red]")
            return None

        with open(self.input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        user_purpose = self.stage1.ask_user_purpose()
        
        try:
            questions = await self.stage1.generate_questions(markdown_content)
            if not questions:
                return None
                
            answers = self.stage1.collect_answers(questions)
            qa_markdown = self.stage1.format_qa_markdown(answers)
            
            qa_file = 'qa_record.md'
            with open(qa_file, 'w', encoding='utf-8') as f:
                f.write(qa_markdown)
            
            return qa_file
            
        except Exception as e:
            self.console.print(f"[bold red]Stage 1 failed: {str(e)}[/bold red]")
            return None

    async def run_stage2_only(self, qa_file: str = 'qa_record.md', user_purpose: str = "") -> Optional[str]:
        """Run only stage 2 (gap analysis) with existing Q&A data"""
        
        if not os.path.exists(self.input_file):
            self.console.print(f"[bold red]Error: Input file '{self.input_file}' not found.[/bold red]")
            return None
            
        if not os.path.exists(qa_file):
            self.console.print(f"[bold red]Error: Q&A file '{qa_file}' not found.[/bold red]")
            return None

        with open(self.input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
            
        with open(qa_file, 'r', encoding='utf-8') as f:
            qa_markdown = f.read()

        try:
            report = await self.stage2.generate_gap_report(markdown_content, qa_markdown, user_purpose)
            if not report:
                return None
                
            gap_report_md = self.stage2.format_gap_report(report)
            report_file = 'gap_summary.md'
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(gap_report_md)
            
            return report_file
            
        except Exception as e:
            self.console.print(f"[bold red]Stage 2 failed: {str(e)}[/bold red]")
            return None


# Convenience function for the main workflow
async def run_questionnaire(input_file: str = 'report.md') -> Dict[str, str]:
    """
    Convenience function to run the complete questionnaire workflow
    
    Args:
        input_file: Path to the tech stack analysis markdown file
        
    Returns:
        Dictionary with results and file paths
    """
    questionnaire = TechStackQuestionnaire(input_file)
    return await questionnaire.run_full_assessment()

"""
作为库使用：
from tech_stack_questionnaire import run_questionnaire, TechStackQuestionnaire

# 完整流程
results = await run_questionnaire('report.md')

# 或使用类
questionnaire = TechStackQuestionnaire('report.md')
results = await questionnaire.run_full_assessment()
"""