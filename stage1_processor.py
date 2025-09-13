import re
import os
from typing import List, Dict
from rich.console import Console
from rich.prompt import Prompt
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class UniversalStage1Processor:
    def __init__(self):
        self.console = Console()
        self.client = AsyncOpenAI(
            base_url=os.getenv("BASE_URL"),
            api_key=os.getenv("API_KEY")
        )
        self.model = os.getenv("MODEL")
        
    async def generate_questions(self, markdown_content: str) -> List[Dict[str, str]]:
        """Generate questions from markdown content using XML tags"""
        
        prompt = f"""Based on the project tech stack analysis report, generate targeted skill assessment questions. For common libraries, test deep understanding; for specialized libraries, focus on basic knowledge assessment.

## Question Generation Strategy:

### Common Libraries Deep Assessment (e.g., pandas, numpy, requests, flask):
- Core concepts and principles understanding
- Advanced features and best practices
- Performance optimization and pitfall avoidance
- Integration usage with other libraries

### Specialized Libraries Basic Assessment:
- Basic usage and application scenarios
- Core functionality awareness
- Usage experience level

### Question Type Design:
1. **Conceptual Understanding** - Test understanding of library core concepts
2. **Practical Application** - Test actual usage experience and patterns
3. **Problem Solving** - Test ability to handle common issues
4. **Best Practices** - Test knowledge of optimization and standards

Please generate 5-7 questions based on library usage in the analysis report. Prioritize frequently used libraries, and question difficulty should match library popularity.

Output format requirements:

<questions>
<question>
<text>In-depth question targeting specific library</text>
<category>Category (e.g., Data Processing, Web Framework, AI/ML, etc.)</category>
<type>multiple_choice</type>
<options>
<option>Technical Option A (demonstrates deep understanding)</option>
<option>Technical Option B (common knowledge)</option>
<option>Technical Option C (basic familiarity)</option>
<option>Other (please specify)</option>
<option>Not familiar with this library</option>
</options>
</question>
</questions>

## Project Tech Stack Usage Analysis:
{markdown_content}

Focus: Generate in-depth questions for frequently used libraries, reflecting VibeDock's intelligent adaptation professionalism.
"""

        system_message = """You are a skill assessment expert for VibeDock's intelligent adaptation system.

Your expertise:
- Designing layered questions based on library popularity and complexity
- Common libraries (pandas, numpy, requests, django, etc.): Deep technical questions testing best practices
- Specialized libraries (domain-specific tools): Basic knowledge questions understanding application scenarios
- Question design reflects progressive learning paths, helping identify real skill levels

Design principles:
- Option design should have clear differentiation, reflecting different proficiency levels
- Deep questions should include common scenarios from actual development
- Avoid purely theoretical questions, focus on practical application abilities"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.6
        )
        
        response_text = response.choices[0].message.content
        return self._extract_questions(response_text)
    
    def _extract_questions(self, response_text: str) -> List[Dict]:
        """Extract questions from XML tags using regex"""
        questions = []
        
        # Find all question blocks
        question_pattern = r'<question>(.*?)</question>'
        question_matches = re.findall(question_pattern, response_text, re.DOTALL)
        
        for question_block in question_matches:
            # Extract basic info
            text_match = re.search(r'<text>(.*?)</text>', question_block, re.DOTALL)
            category_match = re.search(r'<category>(.*?)</category>', question_block, re.DOTALL)
            type_match = re.search(r'<type>(.*?)</type>', question_block, re.DOTALL)
            
            # Extract options
            options_section = re.search(r'<options>(.*?)</options>', question_block, re.DOTALL)
            options = []
            if options_section:
                option_pattern = r'<option>(.*?)</option>'
                option_matches = re.findall(option_pattern, options_section.group(1), re.DOTALL)
                options = [opt.strip() for opt in option_matches]
            
            if text_match and category_match:
                questions.append({
                    'question': text_match.group(1).strip(),
                    'category': category_match.group(1).strip(),
                    'type': type_match.group(1).strip() if type_match else 'open_text',
                    'options': options
                })
        
        return questions
    
    def ask_user_purpose(self) -> str:
        """Ask user about their purpose with this project"""
        self.console.print("\n[bold blue]Before we start the technical assessment...[/bold blue]")
        self.console.print("[yellow]What is your primary goal with this project?[/yellow]")
        
        purposes = [
            "Active development - I want to contribute code to this project",
            "Learning - I want to understand how this project works", 
            "Maintenance - I need to maintain/debug existing code",
            "Integration - I want to integrate this project into my work",
            "Evaluation - I'm evaluating this project for potential use",
            "Other (please specify)"
        ]
        
        self.console.print("\n[dim]Options:[/dim]")
        for idx, purpose in enumerate(purposes, 1):
            self.console.print(f"  {idx}. {purpose}")
        
        while True:
            try:
                choice = Prompt.ask(f"Please select your purpose (1-{len(purposes)})")
                choice_idx = int(choice) - 1
                
                if 0 <= choice_idx < len(purposes):
                    selected_purpose = purposes[choice_idx]
                    
                    if "other" in selected_purpose.lower():
                        custom_purpose = Prompt.ask("Please specify your purpose")
                        return f"{selected_purpose}: {custom_purpose}"
                    else:
                        return selected_purpose
                else:
                    self.console.print(f"[red]Please enter a number between 1 and {len(purposes)}[/red]")
            except ValueError:
                self.console.print("[red]Please enter a valid number[/red]")
    
    def collect_answers(self, questions: List[Dict]) -> Dict[str, str]:
        """Collect user answers interactively"""
        answers = {}
        self.console.print("\n[bold yellow]Now let's assess your technical background:[/bold yellow]")
        
        for i, q_data in enumerate(questions, 1):
            self.console.print(f"\n[bold cyan]Question {i} - Category: {q_data['category']}[/bold cyan]")
            self.console.print(f"[green]{q_data['question']}[/green]")
            
            if q_data['type'] == 'multiple_choice' and q_data['options']:
                # Display multiple choice options
                self.console.print("\n[dim]Options:[/dim]")
                for idx, option in enumerate(q_data['options'], 1):
                    self.console.print(f"  {idx}. {option}")
                
                # Get user choice
                while True:
                    try:
                        choice = Prompt.ask(f"Please select an option (1-{len(q_data['options'])})")
                        choice_idx = int(choice) - 1
                        
                        if 0 <= choice_idx < len(q_data['options']):
                            selected_option = q_data['options'][choice_idx]
                            
                            # Handle "Other (please specify)" option
                            if "other" in selected_option.lower() and "specify" in selected_option.lower():
                                custom_answer = Prompt.ask("Please specify your answer")
                                answers[q_data['question']] = f"{selected_option}: {custom_answer}"
                            else:
                                answers[q_data['question']] = selected_option
                            break
                        else:
                            self.console.print(f"[red]Please enter a number between 1 and {len(q_data['options'])}[/red]")
                    except ValueError:
                        self.console.print("[red]Please enter a valid number[/red]")
            else:
                # Fallback to open text for other question types
                answer = Prompt.ask("Your answer")
                answers[q_data['question']] = answer
            
        return answers
    
    def format_qa_markdown(self, answers: Dict[str, str]) -> str:
        """Format the Q&A session into a markdown string"""
        markdown = "# Tech Stack Q&A Record\n\n"
        for question, answer in answers.items():
            markdown += f"**Q: {question}**\n"
            markdown += f"A: {answer}\n\n"
        return markdown.strip()