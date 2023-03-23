import random

from json_manager import *
from useful_functions import *
from quest_getter import QuestGetter
from buttons import Buttons
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
        self._TEXT_TO_SPEECH = ""
        self._BUTTONS = Buttons ( )
        self._working_with_user ( )


    def _working_with_user (self) -> None:
        # Абсолютно новый пользователь
        if self._INTERSESSIONAL_DATA["new_user"]:
            self._OUTPUT_TEXT = get_text_for_new_user ( )
            self._TEXT_TO_SPEECH = get_text_for_new_user ( ) + "\n"
            self._TEXT_TO_SPEECH += get_main_commands_of_skill ( )
            self._INTERSESSIONAL_DATA["new_user"] = False
            self._BUTTONS.add_buttons_of_main_menu_in_text ( )

        # Пользователь в главном меню впервые
        elif self._user_is_in_main_menu and self._IS_FIRST_MESSAGE:
            user_greeting = get_user_greeting ( )
            self._OUTPUT_TEXT = user_greeting
            self._TEXT_TO_SPEECH = user_greeting
            self._TEXT_TO_SPEECH += get_main_commands_of_skill ( )
            self._BUTTONS.add_buttons_of_main_menu_in_text ( )

        # Пользователь просто в главном меню
        elif self._user_is_in_main_menu:
            text_that_says_user_is_just_in_main_menu = get_text_that_says_user_is_just_in_main_menu ( )
            self._OUTPUT_TEXT = text_that_says_user_is_just_in_main_menu
            self._TEXT_TO_SPEECH = text_that_says_user_is_just_in_main_menu
            self._TEXT_TO_SPEECH += get_main_commands_of_skill ( )
            self._BUTTONS.add_buttons_of_main_menu_in_text ( )
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
        self._BUTTONS.remove_all_buttons ( )
        self._TEXT_TO_SPEECH = ""
        # Пока навык в разработке
        if self._has_all_words_in_text_in_lower ("сбрось", "настройки") or \
           self._has_all_words_in_text_in_lower ("сбросить", "настройки"):
            self._INTERSESSIONAL_DATA["new_user"] = True
            self._INTERSESSIONAL_DATA["last_lesson"] = 0
            self._INTERSESSIONAL_DATA["last_task"] = 0
            self._OUTPUT_TEXT = "Настройки сброшены.\n"
            self._OUTPUT_TEXT = "Перезагрузите навык."

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
            self._BUTTONS.add_buttons ("На главное меню", "Пока!", hide_all = True)

        elif self._has_one_word_in_text_in_lower (
                "задачка", "задачки", "задачку", "задачке", "задачкой",
                "задача", "задачи", "задачу", "задаче", "задачей"):
            """Чем отличаются задачки от квеста?"""
            # FIXME
            self._SESSIONAL_DATA["working_with_tasks"] = True
            self._OUTPUT_TEXT = "Пока \"Задачка\" ничего не умеет...\n"
            self._OUTPUT_TEXT += "Может, на главное меню?"
            self._BUTTONS.add_buttons ("На главное меню", "Пока!", hide_all = True)

        elif self._has_one_word_in_text_in_lower (
                "квест", "квеста", "квесту", "квестом", "квесте"):
            # Просто доделать
            self._SESSIONAL_DATA["working_with_quest"] = True
            self._OUTPUT_TEXT = "Какой уровень сложности вы предпочитаете?\n"
            self._TEXT_TO_SPEECH = "Какой уровень сложности вы предпочитаете?\n"
            self._TEXT_TO_SPEECH += f"{', '.join (self._difficulty_levels)}"
            self._BUTTONS.add_buttons (*self._difficulty_levels, hide_all = False)
            self._BUTTONS.add_buttons ("Узнать мои результаты", "На главное меню", "Пока", hide_all = True)

        elif self._has_all_words_in_text_in_lower ("на", "урок"):
            self._SESSIONAL_DATA["working_with_course"] = True
            self._OUTPUT_TEXT = "Пока \"Перейти на урок\" ничего не умеет...\n"
            self._OUTPUT_TEXT += "Может, на главное меню?"
            self._BUTTONS.add_buttons ("На главное меню", "Пока!", hide_all = True)

        elif self._has_one_word_in_text_in_lower (
                "пожаловаться", "жалоба", "жалобу", "отчёт", "отчет"):
            self._SESSIONAL_DATA["sending_report"] = True
            self._OUTPUT_TEXT = "Я не знаю, на какую почту отправлять жалобу...\n"
            self._OUTPUT_TEXT += "Может, на главное меню?"
            self._BUTTONS.add_buttons ("На главное меню", "Пока!", hide_all = True)

        elif self._has_one_word_in_text_in_lower (
                "консультант", "консультанта", "консультанту", "консультантом", "консультанте"
                "консультация", "консультации", "консультацию", "консультацией", "проконсультируй"):
            self._SESSIONAL_DATA["consulting"] = True
            self._OUTPUT_TEXT = "Пока я не могу вас проконсультировать, извините...\n"
            self._OUTPUT_TEXT += "Может, на главное меню?"
            self._BUTTONS.add_buttons ("На главное меню", "Пока!", hide_all = True)

        elif self._has_all_words_in_text_in_lower ("оцени", "знания"):
            self._OUTPUT_TEXT = "Зачем \"Оцени мои знания\", когда есть \"Квест\"?\n"
            self._OUTPUT_TEXT += "Скажи \"Квест\", чтобы его попробовать."
            self._BUTTONS.add_buttons_of_main_menu_in_text ( )

        elif self._user_wants_to_go_to_main_menu:
            self._OUTPUT_TEXT = "Вы уже на главном меню!"

        elif self._user_wants_to_end_session:
            self._end_the_session ( )

        else:
            self._OUTPUT_TEXT = get_apology_text ( )

    @property
    def _difficulty_levels (self) -> tuple[str, str, str, str]:
        return "Лёгкий", "Средний", "Высокий", "Случайный"

    @property
    def _buttons_for_choosing_difficutly_level (self) -> dict:
        return "Лёгкий", "Средний", "Высокий", "Случайный", "Узнать мои результаты", "На главное меню", "Пока!"


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
        elif self._SESSIONAL_DATA["viewing_quest_results"]:
            self._viewing_quest_results ( )
        elif self._SESSIONAL_DATA["sending_report"]:
            self._sending_report ( )
        elif self._SESSIONAL_DATA["consulting"]:
            self._consulting ( )

    def _working_with_course (self) -> None:
        if self._user_wants_to_go_to_main_menu:
            self._go_to_main_menu ( )

        elif self._user_wants_to_end_session:
            self._end_the_session ( )

        else:
            self._OUTPUT_TEXT = get_apology_text ( )
            self._BUTTONS.add_buttons ("На главное меню", "Пока!", hide_all = True)

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
            self._BUTTONS.add_buttons ("На главное меню", "Пока!", hide_all = True)

    def _working_with_quest (self) -> None:
        if self._has_one_word_in_text_in_lower (
                "лёгкий", "лёгкого", "лёгкому", "лёгким", "лёгком",
                "легкий", "легкого", "легкому", "легким", "легком"):
            self._SESSIONAL_DATA["difficulty_level"] = DifficultyLevelsOfQuest.EASY.value
            self._SESSIONAL_DATA["working_with_quest"] = False
            self._SESSIONAL_DATA["choosing_right_answer_for_quest"] = True
            self._save_text_and_correct_answer_of_easy_quest_in_session_data ( )
            self._OUTPUT_TEXT = random.choice (("Хорошо.", "Отлично.", "Прекрасно.")) + "\n\n"
            self._say_that_user_can_change_their_difficulty_level_if_it_is_not_said_yet ( )
            self._OUTPUT_TEXT += self._get_text_of_current_quest ( )
            self._BUTTONS.add_buttons (*self._buttons_for_choosing_correct_answer, hide_all = True)

        elif self._has_one_word_in_text_in_lower (
                "средний", "среднего", "среднему", "среднем",
                "средняя", "средней", "среднюю"):
            self._SESSIONAL_DATA["difficulty_level"] = DifficultyLevelsOfQuest.MEDIUM.value
            self._SESSIONAL_DATA["working_with_quest"] = False
            self._SESSIONAL_DATA["choosing_right_answer_for_quest"] = True
            self._save_text_and_correct_answer_of_medium_quest_in_session_data ( )
            self._OUTPUT_TEXT = random.choice (("Хорошо.", "Отлично.", "Прекрасно.")) + "\n\n"
            self._say_that_user_can_change_their_difficulty_level_if_it_is_not_said_yet ( )
            self._OUTPUT_TEXT += self._get_text_of_current_quest ( )
            self._BUTTONS.add_buttons (*self._buttons_for_choosing_correct_answer, hide_all = True)

        elif self._has_one_word_in_text_in_lower (  
                "высокий", "высокого", "высокому", "высоким", "высоком",
                "сложный", "сложного", "сложному", "сложным", "сложном"):
            self._SESSIONAL_DATA["difficulty_level"] = DifficultyLevelsOfQuest.HARD.value
            self._SESSIONAL_DATA["working_with_quest"] = False
            self._SESSIONAL_DATA["choosing_right_answer_for_quest"] = True
            self._save_text_and_correct_answer_of_hard_quest_in_session_data ( )
            self._OUTPUT_TEXT = random.choice (("Хорошо.", "Отлично.", "Прекрасно.")) + "\n\n"
            self._say_that_user_can_change_their_difficulty_level_if_it_is_not_said_yet ( )
            self._OUTPUT_TEXT += self._get_text_of_current_quest ( )
            self._BUTTONS.add_buttons (*self._buttons_for_choosing_correct_answer, hide_all = True)

        elif self._has_one_word_in_text_in_lower (
                "случайный", "случайного", "случайному", "случайным", "случайном",
                "случайная", "случайной", "случайную",
                "рандом", "рандома", "рандому", "рандомом", "рандоме",
                "рандомный", "рандомного", "рандомному", "рандомном",
                "рандомная", "рандомной", "рандомную"):
            difficulty_level = DifficultyLevelsOfQuest.get_random_difficulty_level ( )
            self._SESSIONAL_DATA["difficulty_level"] = difficulty_level
            self._SESSIONAL_DATA["working_with_quest"] = False
            self._SESSIONAL_DATA["choosing_right_answer_for_quest"] = True
            self._save_text_and_correct_answer_of_quest_in_session_data (difficulty_level)
            self._OUTPUT_TEXT = random.choice (("Хорошо.", "Отлично.", "Прекрасно.")) + "\n\n"
            self._say_that_user_can_change_their_difficulty_level_if_it_is_not_said_yet ( )
            self._OUTPUT_TEXT += self._get_text_of_current_quest ( )
            self._BUTTONS.add_buttons (*self._buttons_for_choosing_correct_answer, hide_all = True)

        elif self._has_one_word_in_text_in_lower ("результат", "результаты"):
            self._show_results_of_quest_and_next_quest ( )

        elif self._user_wants_to_go_to_main_menu:
            self._go_to_main_menu ( )

        elif self._user_wants_to_end_session:
            self._end_the_session ( )

        else:
            self._OUTPUT_TEXT = get_apology_text ( )
            self._BUTTONS.add_buttons (*self._buttons_for_choosing_difficutly_level, hide_all = True)

    def _save_text_and_correct_answer_of_easy_quest_in_session_data (self) -> None:
        quest_getter = QuestGetter ( )
        quest_getter.save_random_easy_quest ( )
        self._SESSIONAL_DATA["text_of_quest"] = quest_getter.prepared_text_of_random_easy_quest
        self._SESSIONAL_DATA["correct_answer_of_quest"] = quest_getter.correct_answer_of_random_easy_quest
        self._TEXT_TO_SPEECH = quest_getter.answers_to_speech_of_random_easy_quest_as_str

    def _save_text_and_correct_answer_of_medium_quest_in_session_data (self) -> None:
        quest_getter = QuestGetter ( )
        quest_getter.save_random_medium_quest ( )
        self._SESSIONAL_DATA["text_of_quest"] = quest_getter.prepared_text_of_random_medium_quest
        self._SESSIONAL_DATA["correct_answer_of_quest"] = quest_getter.correct_answer_of_random_medium_quest
        self._TEXT_TO_SPEECH = quest_getter.answers_to_speech_of_random_medium_quest_as_str

    def _save_text_and_correct_answer_of_hard_quest_in_session_data (self) -> None:
        quest_getter = QuestGetter ( )
        quest_getter.save_random_hard_quest ( )
        self._SESSIONAL_DATA["text_of_quest"] = quest_getter.prepared_text_of_random_hard_quest
        self._SESSIONAL_DATA["correct_answer_of_quest"] = quest_getter.correct_answer_of_random_hard_quest
        self._TEXT_TO_SPEECH = quest_getter.answers_to_speech_of_random_hard_quest_as_str

    def _save_text_and_correct_answer_of_quest_in_session_data (self, difficulty_level: int) -> None:
        match difficulty_level:
            case DifficultyLevelsOfQuest.EASY.value:
                self._save_text_and_correct_answer_of_easy_quest_in_session_data ( )
            case DifficultyLevelsOfQuest.MEDIUM.value:
                self._save_text_and_correct_answer_of_medium_quest_in_session_data ( )
            case DifficultyLevelsOfQuest.HARD.value:
                self._save_text_and_correct_answer_of_hard_quest_in_session_data ( )
            case _:
                raise ValueError ("Указан неправильный уровень сложности!")

    def _say_that_user_can_change_their_difficulty_level_if_it_is_not_said_yet (self) -> None:
        if not self._SESSIONAL_DATA["was_said_that_user_can_change_difficulty_level"]:
            self._OUTPUT_TEXT += "В любой момент вы можете сменить уровень сложности, сказав: \"Хочу сменить сложность\";\n"
            self._OUTPUT_TEXT += "или выйти на главное меню, сказав: \"На главное меню\".\n"
            self._OUTPUT_TEXT += "Так же вы можете узнать количество правильно отвеченных вопросов, сказав: \"Покажи результаты\".\n"
            self._OUTPUT_TEXT += "Вот квест.\n\n"
            self._SESSIONAL_DATA["was_said_that_user_can_change_difficulty_level"] = True

    def _get_text_of_current_quest (self) -> str:
        return self._SESSIONAL_DATA["text_of_quest"]

    @property
    def _buttons_for_choosing_correct_answer (self) -> dict:
        return "Первое", "Второе", "Третье", "Изменить уровень сложности", "Узнать мои результаты", "На главное меню", "Пока!"


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

        elif self._has_all_words_in_text_in_lower ("уровень", "сложности") or \
             self._has_one_word_in_text_in_lower ("сложность"):
            self._SESSIONAL_DATA["choosing_right_answer_for_quest"] = False
            self._SESSIONAL_DATA["working_with_quest"] = True
            self._OUTPUT_TEXT = random.choice (("Хорошо.", "Отлично.")) + "\n"
            self._OUTPUT_TEXT += "Теперь просто скажите нужный уровень сложности."
            self._BUTTONS.add_buttons (*self._buttons_for_choosing_difficutly_level, hide_all = True)

        elif self._has_one_word_in_text_in_lower ("результат", "результаты"):
            self._show_results_of_quest_and_next_quest ( )

        elif self._user_wants_to_go_to_main_menu:
            self._go_to_main_menu ( )

        elif self._user_wants_to_end_session:
            self._end_the_session ( )

        else:
            self._OUTPUT_TEXT = get_text_that_says_there_is_no_answer_like_that ( )
            self._BUTTONS.add_buttons (*self._buttons_for_choosing_correct_answer, hide_all = True)

    def _correct_answer_of_quest_is_selected (self) -> None:
        self._OUTPUT_TEXT = get_text_that_says_answer_is_correct ( ) + "\n\n"
        current_difficulty_level = self._SESSIONAL_DATA["difficulty_level"]
        self._save_text_and_correct_answer_of_quest_in_session_data (current_difficulty_level)
        self._OUTPUT_TEXT += self._get_text_of_current_quest ( )
        self._SESSIONAL_DATA["number_of_correct_quest_answers"] += 1
        self._BUTTONS.add_buttons (*self._buttons_for_choosing_correct_answer, hide_all = True)

    def _show_results_of_quest_and_next_quest (self) -> None:
        correct_quest_answers = int (self._SESSIONAL_DATA["number_of_correct_quest_answers"])
        wrong_quest_answers = int (self._SESSIONAL_DATA["number_of_wrong_quest_answers"])
        if correct_quest_answers and wrong_quest_answers:
            self._OUTPUT_TEXT = f"Количество правильных ответов: {correct_quest_answers}.\n"
            self._OUTPUT_TEXT += f"Количество неправильных ответов: {wrong_quest_answers}.\n"
            python_knowledge = calculate_python_knowledge (correct_quest_answers, wrong_quest_answers)
            self._OUTPUT_TEXT += f"Ваше знание Python: {python_knowledge}%."
            self._make_all_sessional_data_false ( )
            self._SESSIONAL_DATA["viewing_quest_results"] = True
            self._BUTTONS.add_buttons ("Продолжить квест", "На главное меню", "Пока", hide_all = True)

        elif not correct_quest_answers and wrong_quest_answers:
            self._OUTPUT_TEXT = "Жаль, но у вас нет ни одного правильного ответа на квест."
            self._make_all_sessional_data_false ( )
            self._SESSIONAL_DATA["viewing_quest_results"] = True
            self._BUTTONS.add_buttons ("Продолжить квест", "На главное меню", "Пока", hide_all = True)

        elif correct_quest_answers and not wrong_quest_answers:
            self._OUTPUT_TEXT = "Все ваши ответы верны! Похоже, вы профессиональный программист!"
            self._make_all_sessional_data_false ( )
            self._SESSIONAL_DATA["viewing_quest_results"] = True
            self._BUTTONS.add_buttons ("Продолжить квест", "На главное меню", "Пока", hide_all = True)

        else:
            self._OUTPUT_TEXT = "Пока вы не ответили ни на один квест."
            self._make_all_sessional_data_false ( )
            self._BUTTONS.add_buttons_of_main_menu_in_text ( )


    def _wrong_answer_of_quest_is_selected (self) -> None:
        self._OUTPUT_TEXT = get_text_that_says_answer_is_wrong ( )
        self._SESSIONAL_DATA["number_of_wrong_quest_answers"] += 1
        self._BUTTONS.add_buttons (*self._buttons_for_choosing_correct_answer, hide_all = True)


    def _viewing_quest_results (self) -> None:
        if self._has_one_word_in_text_in_lower ("продолжить"):
            self._SESSIONAL_DATA["viewing_quest_results"] = False
            self._SESSIONAL_DATA["choosing_right_answer_for_quest"] = True
            current_difficulty_level = self._SESSIONAL_DATA["difficulty_level"]
            self._save_text_and_correct_answer_of_quest_in_session_data (current_difficulty_level)
            self._OUTPUT_TEXT = self._get_text_of_current_quest ( )
            self._BUTTONS.add_buttons (*self._buttons_for_choosing_correct_answer, hide_all = True)

        elif self._user_wants_to_go_to_main_menu:
            self._go_to_main_menu ( )

        elif self._user_wants_to_end_session:
            self._end_the_session ( )

        else:
            self._OUTPUT_TEXT = get_apology_text ( )
            self._BUTTONS.add_buttons ("Продолжить квест", "На главное меню", "Пока", hide_all = True)


    def _sending_report (self) -> None:
        # Доработать  # FIXME
        self._BUTTONS.add_buttons ("На главное меню", "Пока!", hide_all = True)
        if self._user_wants_to_go_to_main_menu:
            self._go_to_main_menu ( )
        elif self._user_wants_to_end_session:
            self._end_the_session ( )
        else:
            self._OUTPUT_TEXT = get_apology_text ( )


    def _consulting (self) -> None:
        # Доработать  # FIXME
        self._BUTTONS.add_buttons ("На главное меню", "Пока!", hide_all = True)
        if self._user_wants_to_go_to_main_menu:
            self._go_to_main_menu ( )
        elif self._user_wants_to_end_session:
            self._end_the_session ( )
        else:
            self._OUTPUT_TEXT = get_apology_text ( )


    def _has_all_words_in_text_in_lower (self, *words) -> bool:
        """Есть ли все слова в ответе пользователя?"""
        for word in words:
            if not word in self._WORDS_OF_TEXT_IN_LOWER:
                return False
        return True

    def _has_one_word_in_text_in_lower (self, *words) -> bool:
        """Есть ли хоть одно слово в ответе пользователя?"""
        for word in words:
            if word in self._WORDS_OF_TEXT_IN_LOWER:
                return True
        return False


    def _go_to_main_menu (self) -> None:
        self._OUTPUT_TEXT = get_text_that_says_user_is_just_in_main_menu ( )
        self._TEXT_TO_SPEECH = get_text_that_says_user_is_just_in_main_menu ( )
        self._TEXT_TO_SPEECH += get_main_commands_of_skill ( )
        self._BUTTONS.add_buttons_of_main_menu_in_text ( )
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
                "tts": self._TEXT_TO_SPEECH,
                "end_session": self._IS_END_SESSION,
                "buttons": self._BUTTONS.BUTTONS},
            "session_state": self._SESSIONAL_DATA,
            "user_state_update": self._INTERSESSIONAL_DATA
            }
        # Даже если self._TEXT_TO_SPEECH ничего не содержит (""),
        # то будет сказан текст, который написан в поле ["response"]["text"]



# Функция, вызываемая Яндексом для запуска скрипта Алисы (в коде вызывать её не нужно).
def main (request_from_alisa: dict, context) -> dict:
    handler_of_alisa = HandlerOfAlisa (request_from_alisa)
    return handler_of_alisa.get_response ( )