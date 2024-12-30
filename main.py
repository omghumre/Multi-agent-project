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
            # Market Research Agent
            research_agent = Agent(
                role='Industry Research Specialist',
                goal=f'Conduct comprehensive market research for {company_name}',
                backstory="""You are an expert market researcher specializing in industry analysis 
                and technology adoption trends. Your analysis helps companies identify opportunities 
                for AI/ML implementation.""",
                tools=[self.search_tool],
                llm=self.llm,
                verbose=True
            )

            # Use Case Generation Agent
            use_case_agent = Agent(
                role='AI Solutions Architect',
                goal=f'Generate specific and implementable AI/ML use cases for {company_name}',
                backstory="""You are an AI/ML solutions architect with expertise in identifying 
                practical applications that enhance operations and customer experiences.""",
                tools=[self.search_tool],
                llm=self.llm,
                verbose=True
            )

            # Resource Agent
            resource_agent = Agent(
                role='Technology Resource Specialist',
                goal='Identify specific resources and implementation assets',
                backstory="""You are an expert in finding and evaluating AI/ML implementation 
                resources, focusing on practical tools and datasets.""",
                tools=[self.search_tool],
                llm=self.llm,
                verbose=True
            )

            # Market Research Task
            research_task = Task(
                description=f"""Conduct market research for {company_name}:

                Required Analysis:
                1. Industry Overview
                   - Market size and growth potential
                   - Current technology adoption trends
                   - Key industry challenges
                
                2. Company Position
                   - Current digital maturity level
                   - Existing technology infrastructure
                   - Main operational pain points
                
                3. Competitive Landscape
                   - Key competitors' AI/ML initiatives
                   - Industry best practices
                   - Technology adoption benchmarks
                
                Format as a clear, structured report with specific insights.""",
                agent=research_agent
            )

            # Use Case Generation Task
            use_case_task = Task(
                description=f"""Generate specific AI/ML use cases for {company_name} based on the research:

                For each use case, provide:
                1. Operational Enhancement Use Cases
                   - Process automation opportunities
                   - Efficiency improvement areas
                   - Cost reduction possibilities
                
                2. Customer Experience Use Cases
                   - Customer service enhancement
                   - Personalization opportunities
                   - Engagement improvement
                
                3. For each use case, specify:
                   - Problem Statement
                   - Proposed AI/ML Solution
                   - Expected Benefits
                   - Implementation Requirements
                   - ROI Metrics
                
                Present 2-3 detailed use cases for each category.""",
                agent=use_case_agent
            )

            # Resource Collection Task
            resource_task = Task(
                description=f"""Identify specific resources for implementing the proposed use cases:

                Required Resources:
                1. Technical Assets
                   - Relevant open-source tools
                   - API services
                   - Development frameworks
                
                2. Data Resources
                   - Public datasets
                   - Industry-specific data sources
                   - Benchmark datasets
                
                3. Implementation Guides
                   - Technical documentation
                   - Best practices
                   - Case studies
                
                Provide direct links and brief descriptions for each resource.""",
                agent=resource_agent
            )

            # Create and execute crew
            crew = Crew(
                agents=[research_agent, use_case_agent, resource_agent],
                tasks=[research_task, use_case_task, resource_task],
                verbose=2,
                process=Process.sequential
            )

            result = crew.kickoff()
            
            # Format and save results
            formatted_result = self.format_results(result, company_name)
            self.save_results(formatted_result, company_name)
            
            return formatted_result

        except Exception as e:
            logger.error(f"Error in analysis: {str(e)}")
            return f"Analysis failed: {str(e)}"

    def format_results(self, result: str, company_name: str) -> str:
        """Format the results in a structured way"""
        formatted_output = f"""
# AI/ML Implementation Analysis for {company_name}

## Market Research Summary
{result.split('Use Cases')[0] if 'Use Cases' in result else ''}

## AI/ML Use Cases
{result.split('Use Cases')[1].split('Resources')[0] if 'Use Cases' in result and 'Resources' in result else ''}

## Implementation Resources
{result.split('Resources')[1] if 'Resources' in result else ''}
"""
        return formatted_output

    def save_results(self, result: str, company_name: str):
        try:
            if not os.path.exists('results'):
                os.makedirs('results')
                
            with open(f"results/{company_name}_analysis.md", "w", encoding='utf-8') as f:
                f.write(result)

        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")