from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_community.tools import DuckDuckGoSearchRun
from crewai.tools import tool
from crewai import LLM

# Advanced configuration with detailed parameters
llm = LLM(
    model="gpt-4o",
    temperature=0
)

search_tool = DuckDuckGoSearchRun()


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

#@tool # Décorateur pour enregistrer l'outil
#def duckduckgo_search(self) -> DuckDuckGoSearchRun: # Le nom de la méthode correspond à la clé YAML
#    """Outil pour effectuer des recherches générales sur le web."""
#    return DuckDuckGoSearchRun()

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
        #    tools=[duckduckgo_search],
            verbose=True
        )
    
    @agent
    def seo_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['seo_specialist'],
        #    tools=[duckduckgo_search],
            verbose=True
        )
    
    @agent
    def recipe_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['recipe_writer'],
            verbose=True
        )
    
    @agent
    def human_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['human_editor'],
            verbose=True
        )

    @agent
    def plagiarism_checker(self) -> Agent:
        return Agent(
            config=self.agents_config['plagiarism_checker'],
            verbose=True
        )
    
    @agent
    def content_quality_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['content_quality_manager'],
            verbose=True, 
            allow_delegation=True
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
            output_file='report.md'
        )
    
    @task
    def task_write_recipe(self) -> Task:
        return Task(
            config=self.tasks_config['task_write_recipe'],
            output_file='recipe_article.md'
        )
    
    @task
    def task_human_editing(self) -> Task:
        return Task(
            config=self.tasks_config['task_human_editing'],
            output_file='edited_article.md'
        )

    @task
    def task_check_plagiarism(self) -> Task:
        return Task(
            config=self.tasks_config['task_check_plagiarism'],
            output_file='plagiarism_report.md' # New output file
        )

    @task
    def task_manage_article_creation(self) -> Task:
         # This task now drives the whole process via the manager's delegation
         return Task(
             config=self.tasks_config['task_manage_article_creation'],
             output_file='manage_report.md'
         )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Copyright crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        worker_agents = [
            self.recipe_researcher(),
            self.seo_specialist(),
            self.recipe_writer(),
            self.human_editor(),
            self.plagiarism_checker()
        ]
        
        return Crew(
            agents=worker_agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.hierarchical,
            tools=[search_tool], 
            manager_agent=self.content_quality_manager(),
            verbose=True,
            llm=llm
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )