from json_manager import *
from useful_functions import *
from enums import *


class HandlerOfAlisa:
    def __init__ (self, request: dict):
        self._VERSION: str = request["version"]
        self._TEXT_IN_LOWER: str = request["request"]["command"]
        self._ORIGINAL_TEXT: str = request["request"]["original_utterance"]
        self._WORDS_OF_TEXT_IN_LOWER: list = request["request"]["nlu"]["tokens"]
        self._OUTPUT_TEXT = ""
        self._IS_FIRST_MESSAGE: bool = request["session"]["new"]
        self._IS_END_SESSION: bool = False
        self._SESSIONAL_DATA: dict = request["state"]["session"]
        self._INTERSESSIONAL_DATA: dict = request["state"]["user"] # Межсессионные данные
        self._BUTTONS = [ ]
        self._buttons_of_main_menu = create_buttons (*get_main_commands_of_skill_as_list ( ))
        self._create_intersessional_data_if_necessary ( )
        self._working_with_user ( )

    def _create_intersessional_data_if_necessary (self) -> None:
        # Я думаю, что у нового пользователя межсессионные данные пусты,
        # поэтому создаю их, если это необходимо
        if "new_user" in self._INTERSESSIONAL_DATA.keys ( ):
            self._IS_NEW_USER: bool = self._INTERSESSIONAL_DATA["new_user"]
        else:
            self._IS_NEW_USER = True
            self._INTERSESSIONAL_DATA["new_user"] = True
            self._INTERSESSIONAL_DATA["last_lesson"] = 0
            self._INTERSESSIONAL_DATA["last_task"] = 0

    def _working_with_user (self) -> None:
        if "user_should_choose_something" in self._SESSIONAL_DATA.keys():
            if self._SESSIONAL_DATA["user_should_choose_something"]:
                self._interception_of_attention ( )
            else:
                self._choosing_function_in_main_menu ( )
        else:
            self._choosing_function_in_main_menu ( )
    
    def _interception_of_attention (self) -> None:
        if "choosing_lesson" in self._SESSIONAL_DATA.keys():
            self._do_something_if_choosing_lesson_is_true ( )
        
        if "choosing_task" in self._SESSIONAL_DATA.keys():
            pass  # FIXME

        if "choosing_right_answer_for_quest" in self._SESSIONAL_DATA.keys():
            self._do_something_if_choosing_right_answer_for_quest ( )

        if "quest_difficulty_selection" in self._SESSIONAL_DATA.keys():
            self._do_something_if_quest_difficulty_selection_is_true ( )

    def _do_something_if_choosing_lesson_is_true (self) -> None:
        if self._SESSIONAL_DATA["choosing_lesson"]:
            if self._has_one_word_in_text_in_lower ("далее", "дальше", "следующий", "продолжи"):
                self._INTERSESSIONAL_DATA["last_lesson"] += 1
                lesson_number = self._INTERSESSIONAL_DATA["last_lesson"]
                self._OUTPUT_TEXT = "Тема урока: " + get_theme_of_lesson (lesson_number) + "\n"
                self._OUTPUT_TEXT += get_lesson_text (lesson_number)
                self._BUTTONS = create_buttons ("Далее.", "Повтор.", "На главное меню.", "Выйти.")

            elif self._has_one_word_in_text_in_lower ("повтор", "повтори"):
                self._OUTPUT_TEXT = "Хорошо.\n" + get_lesson_text (
                    self._INTERSESSIONAL_DATA["last_lesson"])
                self._BUTTONS = create_buttons ("Далее.", "Повтор.", "На главное меню.", "Выйти.")

            elif self._has_all_words_in_text_in_lower ("на", "главное", "меню"):
                self._user_is_in_main_menu ( )

            elif self._has_one_word_in_text_in_lower ("выключись", "выход", "выйти"):
                self._OUTPUT_TEXT = get_farewell_text ( )
                self._IS_END_SESSION = True

            else:
                self._OUTPUT_TEXT = get_apology_text ( )

    def _do_something_if_quest_difficulty_selection_is_true (self) -> None:
        if self._SESSIONAL_DATA["quest_difficulty_selection"]:
            # Переделать все уровни сложности в квестах!!!
            if self._has_one_word_in_text_in_lower ("лёгкий", "лёгкого", "лёгкому", "лёгким", "лёгком"):
                difficulty_level = DifficultyLevelsOfCourse.EASY.value
                is_difficulty_level = True

            elif self._has_one_word_in_text_in_lower ("средний", "среднего", "среднему", "среднем", "средним"):
                difficulty_level = DifficultyLevelsOfCourse.MEDIUM.value
                is_difficulty_level = True

            elif self._has_one_word_in_text_in_lower ("сложный", "сложного", "сложному", "сложным", "сложном"):
                difficulty_level = DifficultyLevelsOfCourse.HARD.value
                is_difficulty_level = True

            elif self._has_one_word_in_text_in_lower ("рандом", "рандома", "рандому", "рандомом", "рандоме"):
                difficulty_level = DifficultyLevelsOfCourse.RANDOM.value
                is_difficulty_level = True

            elif self._has_all_words_in_text_in_lower ("на", "главное", "меню"):
                self._user_is_in_main_menu ( )

            elif self._has_one_word_in_text_in_lower ("выключись", "выход", "выйти"):
                self._OUTPUT_TEXT = get_farewell_text ( )
                self._IS_END_SESSION = True

            else:
                self._OUTPUT_TEXT = get_apology_text ( )

            if is_difficulty_level:
                self._SESSIONAL_DATA["choosing_right_answer_for_quest"] = True
                self._BUTTONS = create_buttons ("а", "б", "в")
                self._SESSIONAL_DATA["difficulty_level_of_quest"] = difficulty_level
                self._SESSIONAL_DATA["quest_difficulty_selection"] = False
                self._SESSIONAL_DATA["random_text_and_correct_answer_of_quest"] = get_random_quest_text_and_currect_answer_of_correct_level (difficulty_level)
                self._OUTPUT_TEXT = self._SESSIONAL_DATA["random_text_and_correct_answer_of_quest"][0]

    def _do_something_if_choosing_right_answer_for_quest (self) -> None:
        if self._SESSIONAL_DATA["choosing_right_answer_for_quest"]:
            if self._has_one_word_in_text_in_lower ("а"):
                self._BUTTONS = create_buttons ("а", "б", "в")
                if self._SESSIONAL_DATA["random_text_and_correct_answer_of_quest"][1] == 0:
                    self._OUTPUT_TEXT = "Верно!"
                    self._user_is_in_main_menu ( ) # FIXME
                else:
                    self._OUTPUT_TEXT = "К сожалению, это неправильный ответ.\n"

            elif self._has_one_word_in_text_in_lower ("б"):
                self._BUTTONS = create_buttons ("а", "б", "в")
                if self._SESSIONAL_DATA["random_text_and_correct_answer_of_quest"][1] == 1:
                    self._OUTPUT_TEXT = "Верно!"
                    self._user_is_in_main_menu ( ) # FIXME
                else:
                    self._OUTPUT_TEXT = "К сожалению, это неправильный ответ.\n"

            elif self._has_one_word_in_text_in_lower ("в"):
                self._BUTTONS = create_buttons ("а", "б", "в")
                if self._SESSIONAL_DATA["random_text_and_correct_answer_of_quest"][1] == 2:
                    self._OUTPUT_TEXT = "Верно!"
                    self._user_is_in_main_menu ( ) # FIXME
                else:
                    self._OUTPUT_TEXT = "К сожалению, это неправильный ответ.\n"

            elif self._has_all_words_in_text_in_lower ("на", "главное", "меню"):
                self._user_is_in_main_menu ( )

            elif self._has_one_word_in_text_in_lower ("выключись", "выход", "выйти"):
                self._OUTPUT_TEXT = get_farewell_text ( )
                self._IS_END_SESSION = True

            else:
                self._OUTPUT_TEXT = "Такого варианта ответа нет!"

    def _user_is_in_main_menu (self) -> None:
        self._OUTPUT_TEXT = "Вы на главном меню!\nМои основные команды:\n"
        self._OUTPUT_TEXT += get_main_commands_of_skill ( )
        self._SESSIONAL_DATA["user_should_choose_something"] = False
        self._SESSIONAL_DATA["quest_difficulty_selection"] = False
        self._SESSIONAL_DATA["choosing_lesson"] = False
        self._SESSIONAL_DATA["choosing_task"] = False
        self._BUTTONS = self._buttons_of_main_menu


    def _choosing_function_in_main_menu (self) -> None:
        if self._IS_NEW_USER:
            self._OUTPUT_TEXT = get_text_for_new_user ( )
            self._IS_NEW_USER = False
            self._INTERSESSIONAL_DATA["new_user"] = False
            self._BUTTONS = self._buttons_of_main_menu
        
        elif self._IS_FIRST_MESSAGE:
            self._OUTPUT_TEXT = get_hello_text ( ) + "\n"
            self._OUTPUT_TEXT += get_text_asking_if_user_has_forgotten_commands ( ) + "\n"
            self._OUTPUT_TEXT += get_main_commands_of_skill ( )
            self._BUTTONS = self._buttons_of_main_menu
            self._SESSIONAL_DATA["user_should_choose_something"] = False
            self._SESSIONAL_DATA["quest_difficulty_selection"] = False
            self._SESSIONAL_DATA["choosing_answer_of_quest"] = False
            self._SESSIONAL_DATA["choosing_lesson"] = False
            self._SESSIONAL_DATA["choosing_taskho"] = False

        # Пока навык разрабатывается
        elif self._has_all_words_in_text_in_lower ("сбрось", "настройки") or\
             self._has_all_words_in_text_in_lower ("сбросить", "настройки"):
            self._IS_NEW_USER = True
            self._INTERSESSIONAL_DATA["new_user"] = True
            self._INTERSESSIONAL_DATA["last_lesson"] = 0
            self._INTERSESSIONAL_DATA["last_task"] = 0
            self._OUTPUT_TEXT = "Настройки сброшены."
        
        elif self._has_one_word_in_text_in_lower (
            "курс", "курса", "курсу", "курсе", "курсом"):
            last_lesson: int = self._INTERSESSIONAL_DATA["last_lesson"]
            if last_lesson != 0:
                self._OUTPUT_TEXT = get_text_that_says_which_lesson_user_stopped (last_lesson) + "\n"
                self._OUTPUT_TEXT += "Его тема: " + get_theme_of_lesson (last_lesson) + "\n"
                self._OUTPUT_TEXT += "Если хотите перейти к следующему уроку, то скажите: \"Далее\".\n"
                self._OUTPUT_TEXT += "Если хотите выйти на главное меню, скажите: \"На главное меню\".\n"
                self._OUTPUT_TEXT += "Также вы можете прослушать урок ещё раз, сказав: \"Повтор\"."
            else:
                self._OUTPUT_TEXT = get_introduction_to_course ( )

            self._BUTTONS = create_buttons ("Далее.", "На главное меню.", "Повтор.")
            self._SESSIONAL_DATA["user_should_choose_something"] = True
            self._SESSIONAL_DATA["choosing_lesson"] = True
            # FIXME

        elif self._has_all_words_in_text_in_lower ("продолжи", "курс"):
            self._OUTPUT_TEXT = "Хорошо!\n"
            last_lesson: int = self._INTERSESSIONAL_DATA["last_lesson"]
            next_lesson = last_lesson + 1
            self._OUTPUT_TEXT += "Тема урока: " + get_theme_of_lesson (next_lesson) + "\n"
            self._OUTPUT_TEXT += "ЗАТЫЧКА: показан текст следующего урока."

        elif self._has_one_word_in_text_in_lower (
            "квест", "квеста", "квесту", "квесте", "квесту"):
            self._OUTPUT_TEXT = "Отличный выбор!\nЗдесь вы можете потренироваться в коротких вопросах.\n"
            self._OUTPUT_TEXT += "Есть 3 уровня сложности: лёгкий, средний и сложный\n."
            self._OUTPUT_TEXT += "Также есть \"Рандом\"."
            self._BUTTONS = create_buttons ("Лёгкий.", "Средний.", "Сложный.", "Рандом", "На главное меню.", "Выйти.")
            self._SESSIONAL_DATA["user_should_choose_something"] = True
            self._SESSIONAL_DATA["quest_difficulty_selection"] = True

        elif self._has_one_word_in_text_in_lower (
            "пока", "пака", "прощай", "свидания", "пора", "чао", "выход", "выйти", "отбой"):
            self._OUTPUT_TEXT = get_farewell_text ( )
            self._IS_END_SESSION = True

        else:
            self._OUTPUT_TEXT = get_apology_text ( )
    

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