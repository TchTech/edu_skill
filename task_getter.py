import json
import random

from enums import DifficultyLevels


class TaskGetter:
	def __init__ (self):
		self._load_all_tasks_from_file ( )
		self._create_groups ( )
		self._group_tasks ( )

	def _load_all_tasks_from_file (self) -> None:
		with open (self._name_of_file_with_tasks, "r") as file_with_tasks:
			self.all_tasks = json.load (file_with_tasks)

	@property
	def _name_of_file_with_tasks (self) -> str:
		return "tasks.json"

	def _create_groups (self) -> None:
		self.easy_tasks = [ ]
		self.medium_tasks = [ ]
		self.hard_tasks = [ ]
		self.very_hard_tasks = [ ]

	def _group_tasks (self) -> None:
		for task_number in self.all_tasks.keys():
			task = self.all_tasks[task_number]
			match task["difficulty"]:
				case DifficultyLevels.EASY.value:
					self.easy_tasks.append (task)
				case DifficultyLevels.MEDIUM.value:
					self.medium_tasks.append (task)
				case DifficultyLevels.HARD.value:
					self.hard_tasks.append (task)
				case DifficultyLevels.VERY_HARD.value:
					self.very_hard_tasks.append (task)
				case _:
					raise ValueError (f"Неправильно задана сложность квеста №{task_number}!")


	def get_random_easy_task (self) -> dict[str, str]:
		return random.choice (self.easy_tasks)

	def get_random_medium_task (self) -> dict[str, str]:
		return random.choice (self.medium_tasks)

	def get_random_hard_task (self) -> dict[str, str]:
		return random.choice (self.hard_tasks)

	def get_random_very_hard_task (self) -> dict[str, str]:
		return random.choice (self.very_hard_tasks)
	def get_random_task(self):
		return random.choice(self.all_tasks)