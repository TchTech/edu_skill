import enum
import random


@enum.unique
class DifficultyLevelsOfQuest (enum.IntEnum):
	EASY = 0
	MEDIUM = 1
	HARD = 2

	def get_random_difficulty_level ( ) -> int:
		return random.randint (0, 2)


if __name__ == '__main__':
	print ("DifficultyLevelsOfQuest.get_random_difficulty_level: ",
			DifficultyLevelsOfQuest.get_random_difficulty_level ( ),
			sep = "")