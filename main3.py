import random

from json_manager import *
from useful_functions import *
from quest_getter import QuestGetter
from lesson_getter import LessonGetter
from task_getter import TaskGetter
from buttons import Buttons
from enums import *
from consultant import ArtificialIntelligence

from typing import Literal


class HandlerOfAlisa:
    def __init__ (self, request: dict):
        self._VERSION: str = request["version"]
        self._TEXT_IN_LOWER: str = request["request"]["command"]
        self._ORIGINAL_TEXT: str = request["request"]["original_utterance"]
        self._WORDS_OF_TEXT_IN_LOWER: list = request["request"]["nlu"]["tokens"]
        self._IS_FIRST_MESSAGE: bool = request["session"]["new"]
        self._IS_END_SESSION: bool = False
        # Заранее создаются сессионные и межсессионные данные
        self._SESSIONAL_DATA: dict = create_sessional_data (request["state"]["session"])
        self._INTERSESSIONAL_DATA: dict = create_intersessional_data (request["state"]["user"])
        self._TEXT_TO_SPEECH = ""
        self._BUTTONS = Buttons ( )
        self._working_with_user ( )


    def _working_with_user (self) -> None:
        """Во время запуска навыка Алиса получает пустой текстовый запрос,
           на который она тут же отвечает. Этот ответ мы воспринимаем
           как первое сообщение (хотя оно уже по факту второе, но это неважно).
        """
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
        if self._SESSIONAL_DATA["state"] == "in_main_menu":
            return True
        else:
            return False


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
            self._SESSIONAL_DATA["state"] = "working_with_course"
            self._OUTPUT_TEXT = "Вы находитесь в меню Курса.\n"
            self._OUTPUT_TEXT += "Здесь вы можете посмотреть список тем и выбрать любую,\n"
            self._OUTPUT_TEXT += "можете продолжить последнюю или переслушать текущую."
            self._BUTTONS.add_buttons (*self._commands_of_course, hide_all = False)

        elif self._has_one_word_in_text_in_lower (
                "задачка", "задачки", "задачку", "задачке", "задачкой",
                "задача", "задачи", "задачу", "задаче", "задачей",
                "задачек", "задачкам", "задачками", "задачках"):
            # FIXME
            self._SESSIONAL_DATA["state"] = "working_with_tasks"
            self._OUTPUT_TEXT = "Какой уровень сложности вы хотите выбрать?\n"
            self._TEXT_TO_SPEECH = self._OUTPUT_TEXT
            self._TEXT_TO_SPEECH += ", ".join (self._difficulty_levels_of_course)
            self._BUTTONS.add_buttons (*self._difficulty_levels_of_course, hide_all = False)
            self._BUTTONS.add_buttons ("Узнать мои результаты", "На главное меню", "Пока", hide_all = True)
        elif self._has_one_word_in_text_in_lower(
            "консультант", "консультанту", "консультанта", "консультанты", "консультанте", "консультация", "консультацию", "консультации", "консультацией", "консультантом"
        ):
            self._SESSIONAL_DATA["state"] = "consulting"
            self._OUTPUT_TEXT = "Я готова подобрать вам справку по теме вашей проблемы. С чем вам помочь?\n"
        elif self._has_one_word_in_text_in_lower (
                "квест", "квеста", "квесту", "квестом", "квесте",
                "квесты", "квестов", "квестам", "квестами", "квестах"):
            self._SESSIONAL_DATA["state"] = "working_with_quest"
            self._OUTPUT_TEXT = "Какой уровень сложности вы хотите выбрать?\n"
            self._TEXT_TO_SPEECH = self._OUTPUT_TEXT
            self._TEXT_TO_SPEECH += ", ".join (self._difficulty_levels_of_quest)
            self._BUTTONS.add_buttons (*self._difficulty_levels_of_quest, hide_all = False)
            self._BUTTONS.add_buttons ("Узнать мои результаты", "На главное меню", "Пока", hide_all = True)

        elif self._has_one_word_in_text_in_lower (
                "пожаловаться", "жалоба", "жалобу", "отчёт", "отчет"):
            self._SESSIONAL_DATA["state"] = "sending_report"
            self._OUTPUT_TEXT = "Я не знаю, на какую почту отправлять жалобу...\n"
            self._OUTPUT_TEXT += "Может, на главное меню?"
            self._BUTTONS.add_buttons ("На главное меню", "Пока!", hide_all = True)

        elif self._has_one_word_in_text_in_lower (
                "консультант", "консультанта", "консультанту", "консультантом", "консультанте"
                "консультация", "консультации", "консультацию", "консультацией", "проконсультируй"):
            self._SESSIONAL_DATA["state"] = "consulting"
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
    def _commands_of_course (self) -> tuple[str]:
        return "Посмотреть список тем", "Текущая тема", "Продолжить последнюю", "Переслушать текущую", "На главное меню", "Пока!"

    @property
    def _difficulty_levels_of_quest (self) -> tuple[str, str, str, str]:
        return "Лёгкий", "Средний", "Высокий", "Случайный"

    @property
    def _difficulty_levels_of_course (self) -> tuple[str, str, str, str, str]:
        return "Лёгкий", "Средний", "Высокий", "Очень высокий", "Случайный"


    def _working_with_user_outside_main_menu (self) -> None:
        match self._SESSIONAL_DATA["state"]:
            case "working_with_course":
                self._working_with_course ( )
            case "choosing_course_theme":
                self._choosing_course_theme ( )
            case "start_next_lesson_or_not":
                self._start_next_lesson_or_not ( )
            case "working_with_tasks":
                self._working_with_tasks ( )
            case "choosing_right_answer_for_task":
                self._choosing_right_answer_for_task ( )
            case "working_with_quest":
                self._working_with_quest ( )
            case "choosing_right_answer_for_quest":
                self._choosing_right_answer_for_quest ( )
            case "viewing_quest_results":
                self._viewing_quest_results ( )
            case "sending_report":
                self._sending_report ( )
            case "consulting":
                self._consulting ( )


    def _working_with_course (self) -> None:
        lesson_getter = LessonGetter ( )
        current_lesson_theme = self._INTERSESSIONAL_DATA["current_lesson"]
        current_lesson_subtheme = self._INTERSESSIONAL_DATA["current_sublesson"]

        if self._has_one_word_in_text_in_lower ("список", "списка", "списку", "списком", "списке") or \
                self._has_one_word_in_text_in_lower ("списки", "списка", "спискам", "списками", "списках"):
            self._SESSIONAL_DATA["state"] = "choosing_course_theme"
            self._OUTPUT_TEXT = "Список тем уроков:"
            self._TEXT_TO_SPEECH = self._OUTPUT_TEXT
            for lesson_theme in lesson_getter.themes:
                self._BUTTONS.add_buttons (lesson_theme, hide_all = False)
                self._TEXT_TO_SPEECH += lesson_theme + "\n"
            self._BUTTONS.add_buttons ("Назад", "На главное меню", "Выход", hide_all = True)

        elif self._has_one_word_in_text_in_lower ("продолжить", "дальше", "далее"):
            if current_lesson_theme:
                next_subtheme = lesson_getter.get_name_of_next_subtheme (theme = current_lesson_theme,
                                                                         subtheme = current_lesson_subtheme)
            else:
                next_subtheme = None

            if next_subtheme:
                self._INTERSESSIONAL_DATA["current_sublesson"] = next_subtheme
                self._OUTPUT_TEXT = lesson_getter.get_subtheme_text (theme = current_lesson_theme,
                                                                     subtheme = next_subtheme)
                self._BUTTONS.add_buttons ("Продолжить", "Переслушать", "Список тем",
                                           "На главное меню", "Пока", hide_all = True)
            elif not next_subtheme and current_lesson_subtheme:
                self._OUTPUT_TEXT = "Поздравляю! Вы прошли целый урок.\n"
                self._OUTPUT_TEXT += "Следующий - это " + lesson_getter.get_name_of_next_theme (current_lesson_theme) + "\n"
                self._OUTPUT_TEXT += "Хотите продолжить?"
                self._SESSIONAL_DATA["state"] = "start_next_lesson_or_not"
                self._BUTTONS.add_buttons ("Да, хочу!", "Нет, позже.", hide_all = False)
                self._BUTTONS.add_buttons ("На главное меню", "Пока", hide_all = True)

            else:
                self._user_has_not_listened_to_any_lesson ( )

        elif self._has_all_words_in_text_in_lower ("переслушать"):
            if current_lesson_theme:
                self._OUTPUT_TEXT = lesson_getter.get_subtheme_text (theme = current_lesson_theme,
                                                                     subtheme = current_lesson_subtheme)
                self._OUTPUT_TEXT += "\nСкажите: \"Продолжить\", чтобы продолжить."
                self._BUTTONS.add_buttons ("Продолжить", "Переслушать", "Список тем", "Текущая тема",
                                           "На главное меню", "Пока", hide_all = True)
            else:
                self._user_has_not_listened_to_any_lesson ( )

        elif self._has_one_word_in_text_in_lower ("текущая", "текущую"):
            if current_lesson_theme:
                self._OUTPUT_TEXT = "Текущая тема урока: " + current_lesson_theme + "\n"
                self._OUTPUT_TEXT += "Подтема: " + current_lesson_subtheme
                self._BUTTONS.add_buttons ("Продолжить", "Переслушать", "На главное меню", "Пока", hide_all = True)
            else:
                self._user_has_not_listened_to_any_lesson ( )

        elif self._user_wants_to_go_to_main_menu:
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


    def _user_has_not_listened_to_any_lesson (self) -> None:
        self._OUTPUT_TEXT = "Вы ещё не прошли ни одного урока.\n"
        self._OUTPUT_TEXT += "Скажите: \"Покажи список тем\", чтобы начать изучать курс."
        self._BUTTONS.add_buttons ("Покажи список тем", "На главное меню", "Выход", hide_all = True)


    def _choosing_course_theme (self) -> None:
        if self._has_one_word_in_text_in_lower ("1", "введение"):
            self._start_next_lesson_and_sublesson (1)

        elif self._has_one_word_in_text_in_lower ("2", "устанока"):
            self._start_next_lesson_and_sublesson (2)

        elif self._has_one_word_in_text_in_lower ("3", "основы"):
            self._start_next_lesson_and_sublesson (3)

        elif self._has_one_word_in_text_in_lower ("4", "операторы", "выражения"):
            self._start_next_lesson_and_sublesson (4)

        elif self._has_one_word_in_text_in_lower ("5", "поток", "команд"):
            self._start_next_lesson_and_sublesson (5)

        elif self._has_one_word_in_text_in_lower ("назад", "обратно"):
            self._SESSIONAL_DATA["state"] = "working_with_course"
            self._OUTPUT_TEXT = "Вы находитесь в меню Курса.\n"
            self._OUTPUT_TEXT += "Здесь вы можете посмотреть список тем и выбрать любую,\n"
            self._OUTPUT_TEXT += "можете продолжить последнюю или переслушать текущую."
            self._BUTTONS.add_buttons (*self._commands_of_course, hide_all = False)
            self._BUTTONS.add_buttons ("Покажи список тем", "На главное меню", "Выход", hide_all = True)

        elif self._user_wants_to_go_to_main_menu:
            self._go_to_main_menu ( )

        elif self._user_wants_to_end_session:
            self._end_the_session ( )

        else:
            self._OUTPUT_TEXT = get_apology_text ( )

    def _start_next_lesson_and_sublesson (self, theme_number: Literal[1, 2, 3, 4, 5]) -> None:
        lesson_getter = LessonGetter ( )
        theme_number = theme_number - 1 # Первый урок под номером 0, а не 1
        self._SESSIONAL_DATA["state"] = "working_with_course"
        self._INTERSESSIONAL_DATA["current_lesson"] = (name_of_current_theme := lesson_getter.themes[theme_number]) # Морожовый, он самый)
        self._INTERSESSIONAL_DATA["current_sublesson"] = (name_of_current_subtheme := lesson_getter.get_first_subtheme_name (name_of_current_theme))
        self._OUTPUT_TEXT = random.choice (("Хорошо, ", "Отлично, ", "Прекрасно, ")) + "тогда начнём?" + "\n\n"
        self._OUTPUT_TEXT += "Предисловие первого занятия:\n"
        self._OUTPUT_TEXT += lesson_getter.get_subtheme_text (theme = name_of_current_theme,
                                                              subtheme = name_of_current_subtheme)
        self._TEXT_TO_SPEECH = self._OUTPUT_TEXT
        self._BUTTONS.add_buttons ("Далее", "Переслушать", "На главное меню", "Пока", hide_all = True)


    def _start_next_lesson_or_not (self) -> None:
        old_lesson_theme = self._INTERSESSIONAL_DATA["current_lesson"]
        lesson_getter = LessonGetter ( )
        next_lesson_theme = lesson_getter.get_name_of_next_theme (old_lesson_theme)
        first_lesson_subtheme = lesson_getter.get_first_subtheme_name (next_lesson_theme)
        self._INTERSESSIONAL_DATA["current_lesson"] = next_lesson_theme
        self._INTERSESSIONAL_DATA["current_sublesson"] = first_lesson_subtheme

        if self._has_one_word_in_text_in_lower ("да", "конечно", "дальше", "далее"):
            self._SESSIONAL_DATA["state"] = "working_with_course"
            self._OUTPUT_TEXT = lesson_getter.get_subtheme_text (theme = next_lesson_theme,
                                                                 subtheme = first_lesson_subtheme)
            self._BUTTONS.add_buttons ("Далее", "Переслушать", "На главное меню", "Пока", hide_all = True)

        elif self._has_one_word_in_text_in_lower ("не", "нет", "позже", "потом"):
            self._SESSIONAL_DATA["state"] = "working_with_course"
            self._OUTPUT_TEXT = "Как хотите. В любой момент скажите просто скажите: \"Продолжить\"."
            self._BUTTONS.add_buttons (*self._commands_of_course, hide_all = False)

        elif self._user_wants_to_go_to_main_menu:
            self._go_to_main_menu ( )

        elif self._user_wants_to_end_session:
            self._end_the_session ( )

        else:
            self._OUTPUT_TEXT = get_apology_text ( )
            self._BUTTONS.add_buttons ("Да, хочу!", "Нет, позже.", hide_all = True)


    def _working_with_tasks (self) -> None:
        if self._has_one_word_in_text_in_lower (
                "лёгкий", "лёгкого", "лёгкому", "лёгким", "лёгком",
                "легкий", "легкого", "легкому", "легким", "легком"):
            self._OUTPUT_TEXT = random.choice (("Хорошо, ", "Отлично, ", "Прекрасно, ")) + "тогда начнём?\n"
            self._SESSIONAL_DATA["difficulty_level_of_task"] = DifficultyLevels.EASY.value
            self._SESSIONAL_DATA["state"] = "choosing_between_solve_and_code"

        elif self._has_one_word_in_text_in_lower (
                "средний", "среднего", "среднему", "среднем",
                "средняя", "средней", "среднюю"):
            self._OUTPUT_TEXT = random.choice (("Хорошо, ", "Отлично, ", "Прекрасно, ")) + "тогда начнём?\n"
            self._SESSIONAL_DATA["difficulty_level_of_task"] = DifficultyLevels.MEDIUM.value
            self._SESSIONAL_DATA["state"] = "choosing_between_solve_and_code"

        elif self._has_one_word_in_text_in_lower (  
                "высокий", "высокого", "высокому", "высоким", "высоком",
                "сложный", "сложного", "сложному", "сложным", "сложном"):
            self._OUTPUT_TEXT = random.choice (("Хорошо, ", "Отлично, ", "Прекрасно, ")) + "тогда начнём?\n"
            self._SESSIONAL_DATA["difficulty_level_of_task"] = DifficultyLevels.HARD.value
            self._SESSIONAL_DATA["state"] = "choosing_between_solve_and_code"

        elif self._has_one_word_in_text_in_lower (
                "случайный", "случайного", "случайному", "случайным", "случайном",
                "случайная", "случайной", "случайную",
                "рандом", "рандома", "рандому", "рандомом", "рандоме",
                "рандомный", "рандомного", "рандомному", "рандомном",
                "рандомная", "рандомной", "рандомную"):
            self._OUTPUT_TEXT = random.choice (("Хорошо, ", "Отлично, ", "Прекрасно, ")) + "\n"
            self._SESSIONAL_DATA["difficulty_level_of_task"] = DifficultyLevels.get_random_difficulty_level_for_task ( )
            self._SESSIONAL_DATA["state"] = "choosing_between_solve_and_code"

        elif self._has_one_word_in_text_in_lower ("результат", "результаты"):
            pass

        elif self._user_wants_to_go_to_main_menu:
            self._go_to_main_menu ( )

        elif self._user_wants_to_end_session:
            self._end_the_session ( )

        else:
            self._OUTPUT_TEXT = get_apology_text ( )
            self._BUTTONS.add_buttons ("На главное меню", "Пока!", hide_all = True)


    def _choosing_right_answer_for_task (self) -> None:
        # FIXME
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
            self._SESSIONAL_DATA["difficulty_level_of_quest"] = DifficultyLevels.EASY.value
            self._save_text_and_correct_answer_of_easy_quest_in_session_data ( )
            self._show_quest ( )

        elif self._has_one_word_in_text_in_lower (
                "средний", "среднего", "среднему", "среднем",
                "средняя", "средней", "среднюю"):
            self._SESSIONAL_DATA["difficulty_level_of_quest"] = DifficultyLevels.MEDIUM.value
            self._save_text_and_correct_answer_of_medium_quest_in_session_data ( )
            self._show_quest ( )

        elif self._has_one_word_in_text_in_lower (  
                "высокий", "высокого", "высокому", "высоким", "высоком",
                "сложный", "сложного", "сложному", "сложным", "сложном"):
            self._SESSIONAL_DATA["difficulty_level_of_quest"] = DifficultyLevels.HARD.value
            self._save_text_and_correct_answer_of_hard_quest_in_session_data ( )
            self._show_quest ( )

        elif self._has_one_word_in_text_in_lower (
                "случайный", "случайного", "случайному", "случайным", "случайном",
                "случайная", "случайной", "случайную",
                "рандом", "рандома", "рандому", "рандомом", "рандоме",
                "рандомный", "рандомного", "рандомному", "рандомном",
                "рандомная", "рандомной", "рандомную"):
            difficulty_level = DifficultyLevels.get_random_difficulty_level_for_quest ( )
            self._SESSIONAL_DATA["difficulty_level_of_quest"] = difficulty_level
            self._save_text_and_correct_answer_of_quest_in_session_data (difficulty_level)
            self._show_quest ( )

        elif self._has_one_word_in_text_in_lower ("результат", "результаты"):
            self._show_results_of_quest_and_next_quest ( )

        elif self._user_wants_to_go_to_main_menu:
            self._go_to_main_menu ( )

        elif self._user_wants_to_end_session:
            self._end_the_session ( )

        else:
            self._OUTPUT_TEXT = get_apology_text ( )
            self._BUTTONS.add_buttons (*self._buttons_for_choosing_difficutly_level, hide_all = True)

    @property
    def _buttons_for_choosing_difficutly_level (self) -> dict:
        return "Лёгкий", "Средний", "Высокий", "Случайный", "Узнать мои результаты", "На главное меню", "Пока!"

    def _save_text_and_correct_answer_of_easy_quest_in_session_data (self) -> None:
        quest_getter = QuestGetter ( )
        quest_getter.save_random_easy_quest ( )
        self._SESSIONAL_DATA["text_of_quest"] = quest_getter.prepared_text_of_random_easy_quest
        self._SESSIONAL_DATA["correct_answer_of_quest"] = quest_getter.correct_answer_of_random_easy_quest
        #self._TEXT_TO_SPEECH = quest_getter.answers_to_speech_of_random_easy_quest_as_str

    def _save_text_and_correct_answer_of_medium_quest_in_session_data (self) -> None:
        quest_getter = QuestGetter ( )
        quest_getter.save_random_medium_quest ( )
        self._SESSIONAL_DATA["text_of_quest"] = quest_getter.prepared_text_of_random_medium_quest
        self._SESSIONAL_DATA["correct_answer_of_quest"] = quest_getter.correct_answer_of_random_medium_quest
        #self._TEXT_TO_SPEECH = quest_getter.answers_to_speech_of_random_medium_quest_as_str

    def _save_text_and_correct_answer_of_hard_quest_in_session_data (self) -> None:
        quest_getter = QuestGetter ( )
        quest_getter.save_random_hard_quest ( )
        self._SESSIONAL_DATA["text_of_quest"] = quest_getter.prepared_text_of_random_hard_quest
        self._SESSIONAL_DATA["correct_answer_of_quest"] = quest_getter.correct_answer_of_random_hard_quest
        #self._TEXT_TO_SPEECH = quest_getter.answers_to_speech_of_random_hard_quest_as_str

    def _save_text_and_correct_answer_of_quest_in_session_data (self, difficulty_level: int) -> None:
        match difficulty_level:
            case DifficultyLevels.EASY.value:
                self._save_text_and_correct_answer_of_easy_quest_in_session_data ( )
            case DifficultyLevels.MEDIUM.value:
                self._save_text_and_correct_answer_of_medium_quest_in_session_data ( )
            case DifficultyLevels.HARD.value:
                self._save_text_and_correct_answer_of_hard_quest_in_session_data ( )
            case _:
                raise ValueError ("Указан неправильный уровень сложности!")

    def _say_that_user_can_change_their_difficulty_level_of_quest_if_it_is_not_said_yet (self) -> None:
        if not self._SESSIONAL_DATA["was_said_that_user_can_change_difficulty_level_in_quest"]:
            text = [
            "В любой момент вы можете сменить уровень сложности, сказав: \"Хочу сменить сложность\";\n",
            "или выйти на главное меню, сказав: \"На главное меню\".\n",
            "Так же вы можете узнать количество правильно отвеченных вопросов, сказав: \"Покажи результаты\".\n",
            "Вот квест.\n\n"
            ]
            self._OUTPUT_TEXT += "".join (text)
            self._SESSIONAL_DATA["was_said_that_user_can_change_difficulty_level_in_quest"] = True

    def _get_text_of_current_quest (self) -> str:
        return self._SESSIONAL_DATA["text_of_quest"]

    @property
    def _buttons_for_choosing_correct_answer (self) -> dict:
        return "Первое", "Второе", "Третье", "Изменить уровень сложности", "Узнать мои результаты", "На главное меню", "Пока!"

    def _show_quest (self) -> None:
        self._SESSIONAL_DATA["state"] = "choosing_right_answer_for_quest"
        self._OUTPUT_TEXT = random.choice (("Хорошо.", "Отлично.", "Прекрасно.")) + "\n\n"
        self._say_that_user_can_change_their_difficulty_level_of_quest_if_it_is_not_said_yet ( )
        self._OUTPUT_TEXT += self._get_text_of_current_quest ( )
        self._BUTTONS.add_buttons (*self._buttons_for_choosing_correct_answer, hide_all = True)


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
            self._SESSIONAL_DATA["state"] = "working_with_quest"
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
        text_that_says_answer_is_correct = get_text_that_says_answer_is_correct ( ) + "\n\n"
        self._OUTPUT_TEXT = text_that_says_answer_is_correct
        self._TEXT_TO_SPEECH = text_that_says_answer_is_correct
        current_difficulty_level = self._SESSIONAL_DATA["difficulty_level_of_quest"]
        self._save_text_and_correct_answer_of_quest_in_session_data (current_difficulty_level)
        self._OUTPUT_TEXT += self._get_text_of_current_quest ( )
        self._TEXT_TO_SPEECH += self._get_text_of_current_quest ( )
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
            self._SESSIONAL_DATA["state"] = "viewing_quest_results"
            self._BUTTONS.add_buttons ("Продолжить квест", "На главное меню", "Пока", hide_all = True)

        elif not correct_quest_answers and wrong_quest_answers:
            self._OUTPUT_TEXT = "Жаль, но у вас нет ни одного правильного ответа на квест."
            self._SESSIONAL_DATA["state"] = "viewing_quest_results"
            self._BUTTONS.add_buttons ("Продолжить квест", "На главное меню", "Пока", hide_all = True)

        elif correct_quest_answers and not wrong_quest_answers:
            self._OUTPUT_TEXT = "Все ваши ответы верны! Похоже, вы профессиональный программист!"
            self._SESSIONAL_DATA["state"] = "viewing_quest_results"
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
            self._SESSIONAL_DATA["state"] = "choosing_right_answer_for_quest"
            current_difficulty_level = self._SESSIONAL_DATA["difficulty_level_of_quest"]
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
        # self._WORDS_OF_TEXT_IN_LOWER


    def _consulting (self) -> None:
        # Доработать  # FIXME

        ai = ArtificialIntelligence("lessons.json")

        self._BUTTONS.add_buttons ("На главное меню", "Пока!", hide_all = True)
        self._OUTPUT_TEXT = "Итак, я нашла что-то, что может вам помочь, послушайте: " + ai.get_similarity(" ".join(self._WORDS_OF_TEXT_IN_LOWER))


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
        self._SESSIONAL_DATA["state"] = "in_main_menu"
        self._BUTTONS.add_buttons_of_main_menu_in_text ( )


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