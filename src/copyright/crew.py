from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import WebsiteSearchTool
from langchain_community.tools import DuckDuckGoSearchRun

web_rag_tool = DuckDuckGoSearchRun()


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Copyright():
    """Copyright crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def recipe_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['recipe_researcher'],
            tools=[web_rag_tool],
            verbose=True
        )
    
    @agent
    def seo_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['seo_specialist'],
            tools=[web_rag_tool],
            verbose=True
        )
    
    @task
    def task_research_recipe(self) -> Task:
        return Task(
            config=self.tasks_config['task_research_recipe'],
            output_file='report.md'
        )

    @task
    def task_seo_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['task_seo_analysis'],
            #context=[task_research_recipe_here],
            output_file='report.md'
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Copyright crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
 #   @agent
 #   def researcher(self) -> Agent:
 #       return Agent(
 #           config=self.agents_config['researcher'],
 #           verbose=True
 #       )

 #   @agent
 #   def reporting_analyst(self) -> Agent:
 #       return Agent(
 #           config=self.agents_config['reporting_analyst'],
 #           verbose=True
 #       )
    

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
 #   @task
 #   def research_task(self) -> Task:
 #       return Task(
 #           config=self.tasks_config['research_task'],
 #       )

 #   @task
 #   def reporting_task(self) -> Task:
 #       return Task(
 #           config=self.tasks_config['reporting_task'],
 #           output_file='report.md'
 #       )
