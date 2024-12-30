import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain.tools import DuckDuckGoSearchRun
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

class AIUseGenerator:
    def __init__(self):
        self.search_tool = DuckDuckGoSearchRun()
        self.llm = GoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7
        )

    def analyze_company(self, company_name: str):
        try:
            # Create all three agents
            research_agent = Agent(
                role='Industry Researcher',
                goal=f'Research {company_name} industry',
                backstory='Expert in market research and industry analysis',
                tools=[self.search_tool],
                llm=self.llm,
                verbose=True
            )

            use_case_agent = Agent(
                role='AI Solution Expert',
                goal=f'Generate AI use cases for {company_name}',
                backstory='Expert in AI applications and solutions',
                tools=[self.search_tool],
                llm=self.llm,
                verbose=True
            )

            resource_agent = Agent(
                role='Resource Specialist',
                goal='Find relevant AI resources and tools',
                backstory='Expert in AI implementation resources and datasets',
                tools=[self.search_tool],
                llm=self.llm,
                verbose=True
            )

            # Create tasks with clear section markers
            research_task = Task(
                description=f"""Analyze the {company_name} industry and provide:
                ## Market Research Summary
                - Current market state and size
                - Key industry trends
                - Major players and competitors
                Keep it brief and informative.""",
                agent=research_agent
            )

            use_case_task = Task(
                description=f"""Generate 2 practical AI use cases for {company_name}:
                ## AI/ML Use Cases
                1. First Use Case
                   - Problem it solves
                   - AI solution approach
                   - Expected benefits

                2. Second Use Case
                   - Problem it solves
                   - AI solution approach
                   - Expected benefits""",
                agent=use_case_agent
            )

            resource_task = Task(
                description=f"""Find specific resources for {company_name}'s AI implementation:
                ## Implementation Resources
                1. Tools and Frameworks
                   - List 2-3 relevant AI/ML tools
                   - Mention specific versions/capabilities

                2. Datasets
                   - Identify 2-3 relevant datasets
                   - Include sources/links

                3. Implementation Guides
                   - Find 2-3 practical guides
                   - Include documentation links""",
                agent=resource_agent
            )

            # Create crew with all three agents
            crew = Crew(
                agents=[research_agent, use_case_agent, resource_agent],
                tasks=[research_task, use_case_task, resource_task],
                verbose=2,
                process=Process.sequential
            )

            # Get result
            result = crew.kickoff()
            
            # Format and save results
            formatted_result = f"""# AI/ML Implementation Analysis for {company_name}

{result}"""
            
            self.save_results(formatted_result, company_name)
            return formatted_result

        except Exception as e:
            logger.error(f"Error in analysis: {str(e)}")
            return self.get_fallback_response(company_name)

    def get_fallback_response(self, company_name: str) -> str:
        """Provide a detailed fallback response"""
        return f"""# AI/ML Implementation Analysis for {company_name}

## Market Research Summary
- The {company_name} industry is undergoing digital transformation
- Key trends include AI adoption and automation
- Major players are investing in advanced technologies

## AI/ML Use Cases
1. Process Automation
   - Problem: Manual operational processes
   - Solution: AI-powered automation systems
   - Benefits: Increased efficiency and reduced costs

2. Data Analytics
   - Problem: Complex data analysis needs
   - Solution: Machine learning analytics
   - Benefits: Better insights and decision-making

## Implementation Resources
1. Tools and Frameworks
   - TensorFlow/PyTorch for ML development
   - Cloud platforms (AWS, GCP, Azure)

2. Datasets
   - Industry-specific public datasets
   - Benchmark datasets for training

3. Implementation Guides
   - Official documentation
   - Industry best practices guides"""

    def save_results(self, result: str, company_name: str):
        try:
            if not os.path.exists('results'):
                os.makedirs('results')
            
            with open(f"results/{company_name}_analysis.md", "w", encoding='utf-8') as f:
                f.write(result)
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")