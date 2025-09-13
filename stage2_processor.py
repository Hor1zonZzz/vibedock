import re
import os
from typing import List, Dict
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class UniversalStage2Processor:
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url=os.getenv("BASE_URL"),
            api_key=os.getenv("API_KEY")
        )
        self.model = os.getenv("MODEL")
        
    async def generate_gap_report(self, markdown_content: str, qa_markdown: str, user_purpose: str = "") -> Dict:
        """Generate gap assessment report using XML tags"""
        
        purpose_context = ""
        if user_purpose:
            purpose_context = f"\n\n## User's Purpose\n{user_purpose}\n\nIMPORTANT: Tailor your gap analysis and recommendations specifically to this user's stated purpose. Focus on the skills and knowledge most relevant to their goals."
        
        prompt = f"""You are a senior tech lead. Your task is to perform a comprehensive gap analysis. You will be given:
1. A technical stack usage analysis (showing specific libraries, usage counts, methods, classes)
2. A Q&A record of a user's technical proficiency
3. The user's stated purpose for engaging with this project

Your analysis should:
- Identify what technologies are actually used in the project (from the usage analysis)
- Compare the user's proficiency with these specific technologies
- Focus recommendations on what's most critical for the user's stated purpose
- Provide actionable, priority-ranked recommendations

Please provide your response in the following XML format:

<gap_assessment>
<summary>
A high-level summary of the gap analysis tailored to the user's purpose (2-3 sentences)
</summary>
<project_tech_stack>
List the key technologies/libraries actually used in this project based on the usage analysis
</project_tech_stack>
<gaps>
<gap>
<area>Technical area name (e.g., Frontend Framework)</area>
<priority>HIGH/MEDIUM/LOW based on user's purpose</priority>
<current_level>User's current proficiency level in this area</current_level>
<required_level>Level needed for user's stated purpose</required_level>
<description>Description of the gap between project needs and user skills</description>
<recommendation>Specific, actionable recommendation with learning resources/steps</recommendation>
</gap>
</gaps>
</gap_assessment>

## Project Technical Stack Usage Analysis

{markdown_content}

## User Q&A Record

{qa_markdown}{purpose_context}

Analyze the actual usage patterns in the project and provide priority-ranked, purpose-specific recommendations."""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.7
        )
        
        response_text = response.choices[0].message.content
        return self._extract_gap_assessment(response_text)
    
    def _extract_gap_assessment(self, response_text: str) -> Dict:
        """Extract gap assessment from XML tags using regex"""
        result = {"summary": "", "project_tech_stack": "", "gaps": []}
        
        # Extract summary
        summary_match = re.search(r'<summary>(.*?)</summary>', response_text, re.DOTALL)
        if summary_match:
            result["summary"] = summary_match.group(1).strip()
        
        # Extract project tech stack
        tech_stack_match = re.search(r'<project_tech_stack>(.*?)</project_tech_stack>', response_text, re.DOTALL)
        if tech_stack_match:
            result["project_tech_stack"] = tech_stack_match.group(1).strip()
        
        # Extract gaps
        gaps_section = re.search(r'<gaps>(.*?)</gaps>', response_text, re.DOTALL)
        if gaps_section:
            gap_pattern = r'<gap>(.*?)</gap>'
            gap_matches = re.findall(gap_pattern, gaps_section.group(1), re.DOTALL)
            
            for gap_block in gap_matches:
                area_match = re.search(r'<area>(.*?)</area>', gap_block, re.DOTALL)
                priority_match = re.search(r'<priority>(.*?)</priority>', gap_block, re.DOTALL)
                current_level_match = re.search(r'<current_level>(.*?)</current_level>', gap_block, re.DOTALL)
                required_level_match = re.search(r'<required_level>(.*?)</required_level>', gap_block, re.DOTALL)
                desc_match = re.search(r'<description>(.*?)</description>', gap_block, re.DOTALL)
                rec_match = re.search(r'<recommendation>(.*?)</recommendation>', gap_block, re.DOTALL)
                
                if area_match and desc_match and rec_match:
                    result["gaps"].append({
                        "area": area_match.group(1).strip(),
                        "priority": priority_match.group(1).strip() if priority_match else "MEDIUM",
                        "current_level": current_level_match.group(1).strip() if current_level_match else "Unknown",
                        "required_level": required_level_match.group(1).strip() if required_level_match else "Unknown",
                        "gap_description": desc_match.group(1).strip(),
                        "recommendation": rec_match.group(1).strip()
                    })
        
        return result
    
    def format_gap_report(self, report_data: Dict) -> str:
        """Format the gap assessment into a markdown string"""
        markdown = "# Gap Assessment Report\n\n"
        
        # Summary
        markdown += f"## Executive Summary\n\n{report_data.get('summary', 'No summary provided.')}\n\n"
        
        # Project Tech Stack
        if report_data.get('project_tech_stack'):
            markdown += f"## Project Technologies\n\n{report_data.get('project_tech_stack')}\n\n"
        
        # Gaps organized by priority
        gaps = report_data.get('gaps', [])
        if not gaps:
            markdown += "## Assessment Results\n\nNo specific gaps were identified.\n"
        else:
            # Sort gaps by priority (HIGH > MEDIUM > LOW)
            priority_order = {'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
            sorted_gaps = sorted(gaps, key=lambda x: priority_order.get(x.get('priority', 'MEDIUM'), 2))
            
            markdown += "## Gap Analysis Results\n\n"
            
            for gap in sorted_gaps:
                priority = gap.get('priority', 'MEDIUM')
                priority_emoji = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}.get(priority, '🟡')
                
                markdown += f"### {priority_emoji} {gap.get('area', 'N/A')} [{priority} Priority]\n\n"
                
                # Skill levels comparison
                current = gap.get('current_level', 'Unknown')
                required = gap.get('required_level', 'Unknown')
                if current != 'Unknown' and required != 'Unknown':
                    markdown += f"**Current Level:** {current} | **Required Level:** {required}\n\n"
                
                markdown += f"**Gap:** {gap.get('gap_description', 'N/A')}\n\n"
                markdown += f"**Action Plan:** {gap.get('recommendation', 'N/A')}\n\n"
                markdown += "---\n\n"
        
        return markdown.strip()