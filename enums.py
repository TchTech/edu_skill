import enum
import random

from typing import Literal


@enum.unique
class DifficultyLevels (enum.IntEnum):
	EASY = 0
	MEDIUM = 1
	HARD = 2
	VERY_HARD = 3

	def get_random_difficulty_level_for_quest ( ) -> Literal[0, 1, 2]:
		return random.randint (0, 2)

	def get_random_difficulty_level_for_task ( ) -> Literal[0, 1, 2, 3]:
		return random.randint (0, 3)


if __name__ == '__main__':
	print ("DifficultyLevels.get_random_difficulty_level_for_task: ",
			DifficultyLevels.get_random_difficulty_level_for_task ( ),
			sep = "")