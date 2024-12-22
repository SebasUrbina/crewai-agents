import pandas as pd
import os
from datetime import datetime
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
from pydantic import BaseModel

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

class QuestionAnswer(BaseModel):
	question_id: str
	question: str
	answer: str
	explanation: str

class Answer(BaseModel):
	answers: list[QuestionAnswer]

@CrewBase
class Auditia():
	"""Auditia crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['analyst'],
			verbose=True
		)

	@task
	def analyst_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyst_task'],
			output_pydantic=Answer,
			verbose=True
		)

	# @agent
	# def customer_service_analyst(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['customer_service_analyst'],
	# 		verbose=True
	# 	)

	# @task
	# def customer_service_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['customer_service_task'],
	# 		output_pydantic=Answer,
	# 		verbose=True
	# 	)

	# @agent
	# def technical_analyst(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['technical_analyst'],
	# 		verbose=True
	# 	)

	# @task
	# def technical_support_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['technical_support_task'],
	# 		output_pydantic=Answer,
	# 		verbose=True
	# 	)	
	# @agent
	# def sales_analyst(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['sales_analyst'],
	# 		verbose=True
	# 	)

	# @task
	# def sales_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['sales_task'],
	# 		output_pydantic=Answer,
	# 		verbose=True
	# 	)

	@after_kickoff
	def process_output(self, output):


		print(f"Pydantic Output: {output.pydantic}")

		# Create list of dictionaries for DataFrame
		data = []
		for answer in output.pydantic.answers:
			data.append({
				'question_id': answer.question_id,
				'question': answer.question,
				'answer': answer.answer,
				'explanation': answer.explanation
			})

		# Create DataFrame and save to CSV
		df = pd.DataFrame(data)
		
		# Create results directory if it doesn't exist
		os.makedirs('results', exist_ok=True)
		
		# Save with timestamp
		timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
		csv_path = f'results/answers_{timestamp}.csv'
		df.to_csv(csv_path, index=False)

		return output

	@crew
	def crew(self) -> Crew:
		"""Creates the Auditia crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)