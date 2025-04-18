from pathlib import Path
import yaml
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from recruitment.tools.linkedin import LinkedInTool
from openai import OpenAI
from langchain.chat_models import ChatOpenAI
from config import llm
from os import environ as env
from dotenv import load_dotenv

# ===== Environment & API Setup =====
load_dotenv()
api_key = env["OPENAI_API_KEY"]
serper_api_key = env["SERPER_API_KEY"]

CONFIG_DIR = Path(__file__).parent.parent / "config"

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

@CrewBase
class RecruitmentCrew:
    """Recruitment crew powered by CrewAI"""

    def __init__(self):
        self.agents_config = load_yaml(CONFIG_DIR / "agents.yaml")
        self.tasks_config = load_yaml(CONFIG_DIR / "tasks.yaml")

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[SerperDevTool(), ScrapeWebsiteTool(), LinkedInTool()],
            allow_delegation=False,
            verbose=True
        )

    @agent
    def matcher(self) -> Agent:
        return Agent(
            config=self.agents_config['matcher'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            allow_delegation=False,
            verbose=True
        )

    @agent
    def communicator(self) -> Agent:
        return Agent(
            config=self.agents_config['communicator'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            allow_delegation=False,
            verbose=True
        )

    @agent
    def reporter(self) -> Agent:
        return Agent(
            config=self.agents_config['reporter'],
            allow_delegation=False,
            verbose=True
        )

    @task
    def research_candidates_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_candidates_task'],
            agent=self.researcher()
        )

    @task
    def match_and_score_candidates_task(self) -> Task:
        return Task(
            config=self.tasks_config['match_and_score_candidates_task'],
            agent=self.matcher()
        )

    @task
    def outreach_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['outreach_strategy_task'],
            agent=self.communicator()
        )

    @task
    def report_candidates_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_candidates_task'],
            agent=self.reporter(),
            context=[
                self.research_candidates_task(),
                self.match_and_score_candidates_task(),
                self.outreach_strategy_task()
            ],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Recruitment crew"""
        return Crew(
            agents=[
                self.researcher(),
                self.matcher(),
                self.communicator(),
                self.reporter()
            ],
            tasks=[
                self.research_candidates_task(),
                self.match_and_score_candidates_task(),
                self.outreach_strategy_task(),
                self.report_candidates_task()
            ],
            process=Process.sequential,
            verbose=2,
            manager_llm=llm
        )
