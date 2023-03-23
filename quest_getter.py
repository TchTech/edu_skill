import json
import random

from typing import Literal
from enums import DifficultyLevelsOfQuest


class QuestGetter:
    """Создаётся экземпляр класса, затем вызывается метод,
    сохраняющий один случайный квест указанной сложности.
    Затем можно получить подготовленный текст сохраннённого
    квеста и правильный ответ на него."""
    def __init__ (self):
        self._load_all_quests_from_file ( )
        self._group_quests ( )

    def _load_all_quests_from_file (self) -> None:
        with open (self._name_of_file_with_quests, "r") as file:
            self.all_quests: dict = json.load (file)

    @property
    def _name_of_file_with_quests (self) -> str:
        return "quests.json"

    def _group_quests (self) -> None:
        self._create_empty_grouped_quests ( )
        for key in self.all_quests.keys():
            match self.all_quests[key]["difficulty_level"]:
                case DifficultyLevelsOfQuest.EASY.value:
                    self.easy_quests.append (self.all_quests[key])
                case DifficultyLevelsOfQuest.MEDIUM.value:
                    self.medium_quests.append (self.all_quests[key])
                case DifficultyLevelsOfQuest.HARD.value:
                    self.hard_quests.append (self.all_quests[key])
                case _:
                    raise ValueError ("Указан неверный уровень сложности " +
                                     f"в файле {self._name_of_file_with_quests}\n." +
                                     f"Номер неправильного квеста: {key}.")

    def _create_empty_grouped_quests (self) -> None:
        self.easy_quests = [ ]
        self.medium_quests = [ ]
        self.hard_quests = [ ]


    def save_random_easy_quest (self) -> None:
        self.saved_random_easy_quest = random.choice (self.easy_quests)

    def save_random_medium_quest (self) -> None:
        self.saved_random_medium_quest = random.choice (self.medium_quests)

    def save_random_hard_quest (self) -> None:
        self.saved_random_hard_quest = random.choice (self.hard_quests)


    def get_random_easy_quest (self) -> None:
        return random.choice (self.easy_quests)

    def get_random_medium_quest (self) -> None:
        return random.choice (self.medium_quests)

    def get_random_hard_quest (self) -> None:
        return random.choice (self.hard_quests)


    @property
    def text_of_random_easy_quest (self) -> str:
        return self.saved_random_easy_quest["quest_text"]

    @property
    def prepared_text_of_random_easy_quest (self) -> str:
        return self._get_prepared_quest_text_for_user (self.saved_random_easy_quest)

    @property
    def correct_answer_of_random_easy_quest (self) -> Literal[1, 2, 3]:
        return self.saved_random_easy_quest["correct_answer"] + 1 # В файле первый ответ 0, а не 1

    @property
    def answers_of_random_easy_quest_as_str (self) -> list[str]:
        return ", ".join (self.saved_random_easy_quest["answers"] )

    @property
    def answers_to_speech_of_random_easy_quest (self) -> list[str]:
        return self.saved_random_easy_quest["answers_to_speech"]

    @property
    def answers_to_speech_of_random_easy_quest_as_str (self) -> str:
        return " ".join (self.answers_to_speech_of_random_easy_quest)

    @property
    def text_of_random_medium_quest (self) -> str:
        return self.saved_random_medium_quest["quest_text"]

    @property
    def prepared_text_of_random_medium_quest (self) -> str:
        return self._get_prepared_quest_text_for_user (self.saved_random_medium_quest)

    @property
    def correct_answer_of_random_medium_quest (self) -> Literal[1, 2, 3]:
        return self.saved_random_medium_quest["correct_answer"] + 1 # В файле первый ответ 0, а не 1

    @property
    def answers_of_random_medium_quest_as_str (self) -> list[str]:
        return ", ".join (self.saved_random_medium_quest["answers"] )

    @property
    def answers_to_speech_of_random_medium_quest (self) -> list[str]:
        return self.saved_random_medium_quest["answers_to_speech"]

    @property
    def answers_to_speech_of_random_medium_quest_as_str (self) -> str:
        return " ".join (self.answers_to_speech_of_random_medium_quest)

    @property
    def text_of_random_hard_quest (self) -> str:
        return self.saved_random_hard_quest["quest_text"]

    @property
    def prepared_text_of_random_hard_quest (self) -> str:
        return self._get_prepared_quest_text_for_user (self.saved_random_hard_quest)

    @property
    def correct_answer_of_random_hard_quest (self) -> Literal[1, 2, 3]:
        return self.saved_random_hard_quest["correct_answer"] + 1 # В файле первый ответ 0, а не 1

    @property
    def answers_of_random_hard_quest_as_str (self) -> list[str]:
        return ", ".join (self.saved_random_hard_quest["answers"] )

    @property
    def answers_to_speech_of_random_hard_quest (self) -> list[str]:
        return self.saved_random_hard_quest["answers_to_speech"]

    @property
    def answers_to_speech_of_random_hard_quest_as_str (self) -> str:
        return " ".join (self.answers_to_speech_of_random_hard_quest)


    def _get_prepared_quest_text_for_user (self, quest: dict) -> str:
        prepared_quest_text = quest["quest_text"] + "\n"
        answer_number = 1
        for answer in quest["answers"]:
            prepared_quest_text += f"{answer_number}) {answer}\n"
            answer_number += 1
        return prepared_quest_text