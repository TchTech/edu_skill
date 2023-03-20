from json_manager import *
from useful_functions import *
from quest_getter import QuestGetter
from enums import *


class HandlerOfAlisa:
    def __init__ (self, request: dict):
        self._VERSION: str = request["version"]
        self._TEXT_IN_LOWER: str = request["request"]["command"]
        self._ORIGINAL_TEXT: str = request["request"]["original_utterance"]
        self._WORDS_OF_TEXT_IN_LOWER: list = request["request"]["nlu"]["tokens"]
        self._IS_FIRST_MESSAGE: bool = request["session"]["new"]
        self._IS_END_SESSION: bool = False
        self._SESSIONAL_DATA: dict = create_sessional_data (request["state"]["session"])
        self._INTERSESSIONAL_DATA: dict = create_intersessional_data (request["state"]["user"])
        self._BUTTONS = [ ]
        self._working_with_user ( )


    def _working_with_user (self) -> None:
        # Абсолютно новый пользователь
        if self._INTERSESSIONAL_DATA["new_user"]:
            self._OUTPUT_TEXT = get_text_for_new_user ( )
            self._INTERSESSIONAL_DATA["new_user"] = False
            self._BUTTONS = create_buttons_of_main_menu ( )

        # Пользователь в главном меню впервые
        elif self._user_is_in_main_menu and self._IS_FIRST_MESSAGE:
            self._OUTPUT_TEXT = get_user_greeting ( )
            self._BUTTONS = create_buttons_of_main_menu ( )

        # Пользователь просто в главном меню
        elif self._user_is_in_main_menu:
            self._OUTPUT_TEXT = get_text_that_says_user_is_just_in_main_menu ( )
            self._BUTTONS = create_buttons_of_main_menu ( )
            self._working_with_user_in_main_menu ( )

        # Пользователь не в главном меню
        else:
            self._working_with_user_outside_main_menu ( )

    @property
    def _user_is_in_main_menu (self) -> bool:
        # Если в _SESSIONAL_DATA есть хоть одно True-значение,
        # то это значит, что пользователь не в главном меню
        sessional_data = self._SESSIONAL_DATA
        for key in sessional_data.keys():
            if sessional_data[key]:
                return False
        return True


    def _working_with_user_in_main_menu (self) -> None:
        # Пока навык в разработке
        if self._has_all_words_in_text_in_lower ("сбрось", "настройки") or \
           self._has_all_words_in_text_in_lower ("сбросить", "настройки"):
            self._INTERSESSIONAL_DATA["new_user"] = True
            self._INTERSESSIONAL_DATA["last_lesson"] = 0
            self._INTERSESSIONAL_DATA["last_task"] = 0
            self._OUTPUT_TEXT = "Настройки сброшены."

        elif self._has_one_word_in_text_in_lower (
                "курс", "курса", "курсу", "курсом", "курсе"):
            """Последняя тема, на которой вы остановились: (ТЕМА) /
               (если пользователь ещё не проходил темы то Алиса пишет:
               "Вы ещё не прошли ни одной темы").
               Продолжим?
            """
            # FIXME
            self._SESSIONAL_DATA["working_with_course"] = True
            self._OUTPUT_TEXT = "Пока \"Курс\" ничего не умеет...\n"
            self._OUTPUT_TEXT += "Может, на главное меню?"
            self._BUTTONS = create_buttons ("На главное меню", "Пока!")

        elif self._has_one_word_in_text_in_lower (
                "задачка", "задачки", "задачку", "задачке", "задачкой",
                "задача", "задачи", "задачу", "задаче", "задачей"):
            """Чем отличаются задачки от квеста?"""
            # FIXME
            self._SESSIONAL_DATA["working_with_tasks"] = True
            self._OUTPUT_TEXT = "Пока \"Задачка\" ничего не умеет...\n"
            self._OUTPUT_TEXT += "Может, на главное меню?"
            self._BUTTONS = create_buttons ("На главное меню", "Пока!")

        elif self._has_one_word_in_text_in_lower (
                "квест", "квеста", "квесту", "квестом", "квесте"):
            # Просто доделать
            # FIXME
            self._SESSIONAL_DATA["working_with_quest"] = True
            self._OUTPUT_TEXT = "Какой уровень сложности вы предпочитаете?\n"
            self._OUTPUT_TEXT += "Лёгкий.\n"
            self._OUTPUT_TEXT += "Средний.\n"
            self._OUTPUT_TEXT += "Высокий.\n"
            self._OUTPUT_TEXT += "Случайный."
            self._BUTTONS = self._buttons_for_choosing_difficutly_level

        elif self._user_wants_to_go_to_main_menu:
            self._OUTPUT_TEXT = "Вы уже на главном меню!"

        elif self._user_wants_to_end_session:
            self._end_the_session ( )

        else:
            self._OUTPUT_TEXT = get_apology_text ( )

    @property
    def _buttons_for_choosing_difficutly_level (self) -> dict:
        return create_buttons ("Лёгкий", "Средний", "Высокий", "Рандом",
                               "На главное меню", "Пока!")


    def _working_with_user_outside_main_menu (self) -> None:
        # Само собой нужно доработать working-методы
        if self._SESSIONAL_DATA["working_with_course"]:
            self._working_with_course ( )
        elif self._SESSIONAL_DATA["working_with_tasks"]:
            self._working_with_tasks ( )
        elif self._SESSIONAL_DATA["working_with_quest"]:
            self._working_with_quest ( )
        elif self._SESSIONAL_DATA["choosing_right_answer_for_quest"]:
            self._choosing_right_answer_for_quest ( )
        elif self._SESSIONAL_DATA["choosing_between_repeating_and_changing_difficulty_level"]:
            self._choosing_between_repeating_and_changing_difficulty_level ( )

    def _working_with_course (self) -> None:
        if self._user_wants_to_go_to_main_menu:
            self._go_to_main_menu ( )

        elif self._user_wants_to_end_session:
            self._end_the_session ( )

        else:
            self._OUTPUT_TEXT = get_apology_text ( )
            self._BUTTONS = create_buttons ("На главное меню", "Пока!")

    @property
    def _user_wants_to_go_to_main_menu (self) -> bool:
        if self._has_all_words_in_text_in_lower ("на", "главное", "меню"):
            return True
        else:
            return False

    @property
    def _user_wants_to_end_session (self) -> bool:
        if self._has_one_word_in_text_in_lower ("выход", "выйти", "пока", "прощай"):
            return True
        else:
            return False

    def _working_with_tasks (self) -> None:
        if self._user_wants_to_go_to_main_menu:
            self._go_to_main_menu ( )

        elif self._user_wants_to_end_session:
            self._end_the_session ( )

        else:
            self._OUTPUT_TEXT = get_apology_text ( )
            self._BUTTONS = create_buttons ("На главное меню", "Пока!")

    def _working_with_quest (self) -> None:
        if self._user_wants_to_go_to_main_menu:
            self._go_to_main_menu ( )

        elif self._user_wants_to_end_session:
            self._end_the_session ( )

        elif self._has_one_word_in_text_in_lower (
                "лёгкий", "лёгкого", "лёгкому", "лёгким", "лёгком",
                "легкий", "легкого", "легкому", "легким", "легком"):
            self._SESSIONAL_DATA["difficulty_level"] = DifficultyLevelsOfQuest.EASY.value
            self._SESSIONAL_DATA["working_with_quest"] = False
            self._SESSIONAL_DATA["choosing_right_answer_for_quest"] = True
            self._save_text_and_correct_answer_of_easy_quest_in_session_data ( )
            self._OUTPUT_TEXT = "Хорошо.\n"
            self._OUTPUT_TEXT += self._get_text_of_current_quest ( )
            self._BUTTONS = self._buttons_for_choosing_correct_answer

        # FIXME
        elif self._has_one_word_in_text_in_lower ("средний"):
            self._OUTPUT_TEXT = "Пока не настроен файлик, доступен только лёгкий уровень сложности.\n"
            self._OUTPUT_TEXT += "Выберите другой уровень сложности."
            self._BUTTONS = self._buttons_for_choosing_difficutly_level

        # FIXME
        elif self._has_one_word_in_text_in_lower ("высокий"):
            self._OUTPUT_TEXT = "Пока не настроен файлик, доступен только лёгкий уровень сложности.\n"
            self._OUTPUT_TEXT += "Выберите другой уровень сложности."
            self._BUTTONS = self._buttons_for_choosing_difficutly_level

        # FIXME
        elif self._has_one_word_in_text_in_lower ("рандом"):
            self._OUTPUT_TEXT = "Пока не настроен файлик, доступен только лёгкий уровень сложности.\n"
            self._OUTPUT_TEXT += "Выберите другой уровень сложности."
            self._BUTTONS = self._buttons_for_choosing_difficutly_level

        else:
            self._OUTPUT_TEXT = get_apology_text ( )
            self._BUTTONS = self._buttons_for_choosing_difficutly_level

    def _save_text_and_correct_answer_of_easy_quest_in_session_data (self) -> None:
        quest_getter = QuestGetter ( )
        quest_getter.save_random_easy_quest ( )
        self._SESSIONAL_DATA["text_of_quest"] = quest_getter.prepared_text_of_random_easy_quest
        self._SESSIONAL_DATA["correct_answer_of_quest"] = quest_getter.correct_answer_of_random_easy_quest

    def _save_text_and_correct_answer_of_medium_quest_in_session_data (self) -> None:
        quest_getter = QuestGetter ( )
        quest_getter.save_random_medium_quest ( )
        self._SESSIONAL_DATA["text_of_quest"] = quest_getter.prepared_text_of_random_medium_quest
        self._SESSIONAL_DATA["correct_answer_of_quest"] = quest_getter.correct_answer_of_random_medium_quest

    def _save_text_and_correct_answer_of_hard_quest_in_session_data (self) -> None:
        quest_getter = QuestGetter ( )
        quest_getter.save_random_hard_quest ( )
        self._SESSIONAL_DATA["text_of_quest"] = quest_getter.prepared_text_of_random_hard_quest
        self._SESSIONAL_DATA["correct_answer_of_quest"] = quest_getter.correct_answer_of_random_hard_quest

    def _get_text_of_current_quest (self) -> str:
        return self._SESSIONAL_DATA["text_of_quest"]

    @property
    def _buttons_for_choosing_correct_answer (self) -> dict:
        return create_buttons ("Первое", "Второе", "Третье", "На главное меню", "Пока!")


    def _choosing_right_answer_for_quest (self) -> None:
        if self._has_one_word_in_text_in_lower ("1", "один", "первый", "первое"):
            if self._SESSIONAL_DATA["correct_answer_of_quest"] == 1:
                self._correct_answer_of_quest_is_selected ( )
            else:
                self._wrong_answer_of_quest_is_selected ( )

        elif self._has_one_word_in_text_in_lower ("2", "два", "второй", "второе"):
            if self._SESSIONAL_DATA["correct_answer_of_quest"] == 2:
                self._correct_answer_of_quest_is_selected ( )
            else:
                self._wrong_answer_of_quest_is_selected ( )

        elif self._has_one_word_in_text_in_lower ("3", "три", "третий", "третье"):
            if self._SESSIONAL_DATA["correct_answer_of_quest"] == 3:
                self._correct_answer_of_quest_is_selected ( )
            else:
                self._wrong_answer_of_quest_is_selected ( )

        elif self._has_all_words_in_text_in_lower ("на", "главное", "меню"):
            self._go_to_main_menu ( )

        elif self._user_wants_to_end_session:
            self._end_the_session ( )

        else:
            self._OUTPUT_TEXT = "Извините, такого ответа нет."
            self._BUTTONS = self._buttons_for_choosing_correct_answer

    def _correct_answer_of_quest_is_selected (self) -> None:
        self._OUTPUT_TEXT = "Ура! Ты ответил правильно!\n"
        self._OUTPUT_TEXT += "Показать следующий квест или сменить уровень сложности?"
        self._SESSIONAL_DATA["choosing_right_answer_for_quest"] = False
        self._SESSIONAL_DATA["choosing_between_repeating_and_changing_difficulty_level"] = True
        self._BUTTONS = self._buttons_for_next_quest_or_changing_difficulty_level

    @property
    def _buttons_for_next_quest_or_changing_difficulty_level (self) -> dict:
        return create_buttons ("Следующий квест", "Сменить уровень сложности",
                               "На главное меню", "Пока!")

    def _wrong_answer_of_quest_is_selected (self) -> None:
        self._OUTPUT_TEXT = "К сожалению, это неверный ответ."
        self._BUTTONS = self._buttons_for_choosing_correct_answer


    def _choosing_between_repeating_and_changing_difficulty_level (self) -> None:
        if self._has_one_word_in_text_in_lower ("дальше", "далее", "следующий"):
            self._SESSIONAL_DATA["choosing_between_repeating_and_changing_difficulty_level"] = False
            self._SESSIONAL_DATA["choosing_right_answer_for_quest"] = True
            self._save_text_and_correct_answer_of_quest_with_any_difficulty_level_in_session_data ( )
            self._OUTPUT_TEXT = "Хорошо.\n"
            self._OUTPUT_TEXT += self._get_text_of_current_quest ( )
            self._BUTTONS = self._buttons_for_choosing_correct_answer

        elif self._has_one_word_in_text_in_lower ("сменить", "изменить"):
            self._SESSIONAL_DATA["working_with_quest"] = True
            self._OUTPUT_TEXT = "Отлично.\nТеперь просто скажите нужный уровень сложности:\n"
            self._OUTPUT_TEXT += "Лёгкий.\n"
            self._OUTPUT_TEXT += "Средний.\n"
            self._OUTPUT_TEXT += "Высокий.\n"
            self._OUTPUT_TEXT += "Рандом."
            self._BUTTONS = self._buttons_for_choosing_difficutly_level

        elif self._user_wants_to_go_to_main_menu:
            self._go_to_main_menu ( )

        elif self._user_wants_to_end_session:
            self._end_the_session ( )

        else:
            self._OUTPUT_TEXT = get_apology_text ( )
            self._BUTTONS = self._buttons_for_next_quest_or_changing_difficulty_level

    def _save_text_and_correct_answer_of_quest_with_any_difficulty_level_in_session_data (self) -> None:
        match self._SESSIONAL_DATA["difficulty_level"]:
            case DifficultyLevelsOfQuest.EASY.value:
                self._save_text_and_correct_answer_of_easy_quest_in_session_data ( )
            case DifficultyLevelsOfQuest.MEDIUM.value:
                self._save_text_and_correct_answer_of_medium_quest_in_session_data ( )
            case DifficultyLevelsOfQuest.HARD.value:
                self._save_text_and_correct_answer_of_hard_quest_in_session_data ( )
            #case _:
            #    raise ValueError ("В self._SESSIONAL_DATA[\"difficulty_level\"]" +
            #                     f"класса {__class__.__name__} записано значение "+
            #                      "{self._SESSIONAL_DATA["difficulty_level"]},\n" +
            #                      "хотя должно быть записано 0, 1 или 2!")


    def _has_all_words_in_text_in_lower (self, *words) -> bool:
        for word in words:
            if not word in self._WORDS_OF_TEXT_IN_LOWER:
                return False
        return True

    def _has_one_word_in_text_in_lower (self, *words) -> bool:
        for word in words:
            if word in self._WORDS_OF_TEXT_IN_LOWER:
                return True
        return False


    def _go_to_main_menu (self) -> None:
        self._OUTPUT_TEXT = get_text_that_says_user_is_just_in_main_menu ( )
        self._BUTTONS = create_buttons_of_main_menu ( )
        self._make_all_sessional_data_false ( )

    def _make_all_sessional_data_false (self) -> None:
        """Если всё в _SESSIONAL_DATA будет False,
        значит пользователь на главном меню"""
        for key in self._SESSIONAL_DATA.keys():
            self._SESSIONAL_DATA[key] = False


    def _end_the_session (self) -> None:
        self._OUTPUT_TEXT = get_farewell_text ( )
        self._IS_END_SESSION = True


    def get_response (self) -> dict:
        return {
            "version": self._VERSION,
            "response": {
                "text": self._OUTPUT_TEXT,
                "end_session": self._IS_END_SESSION,
                "buttons": self._BUTTONS},
            "session_state": self._SESSIONAL_DATA,
            "user_state_update": self._INTERSESSIONAL_DATA
            }



# Функция, вызываемая Яндексом для запуска скрипта Алисы (в коде вызывать её не нужно).
def main (request_from_alisa: dict, context) -> dict:
    handler_of_alisa = HandlerOfAlisa (request_from_alisa)
    return handler_of_alisa.get_response ( )