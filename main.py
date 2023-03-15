from json_manager import *


class HandlerOfAlisa:
    def __init__ (self, request: dict):
        self._VERSION: str = request["version"]
        self._TEXT_IN_LOWER: str = request["request"]["command"]
        self._ORIGINAL_TEXT: str = request["request"]["original_utterance"]
        self._WORDS_OF_TEXT_IN_LOWER: list = request["request"]["nlu"]["tokens"]
        self._IS_FIRST_MESSAGE: bool = request["session"]["new"]
        self._IS_END_SESSION: bool = False
        self._SESSION_DATA: dict = request["state"]["session"]
        self._INTERSESSIONAL_DATA: dict = request["state"]["user"] # Межсессионные данные
        self._create_intersessional_data_if_necessary ( )
        self._prepare_correct_answer ( )

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

    def _prepare_correct_answer (self) -> None:
        if self._IS_NEW_USER:
            self._NEW_TEXT = get_text_for_new_user ( )
            self._IS_NEW_USER = False
            self._INTERSESSIONAL_DATA["new_user"] = False
        
        elif self._IS_FIRST_MESSAGE:
            self._NEW_TEXT = get_hello_text ( ) + "\n"
            self._NEW_TEXT += get_text_asking_if_user_has_forgotten_commands ( ) + "\n"
            self._NEW_TEXT += get_main_commands_of_skill ( )

        # Пока навык разрабатывается
        elif self._has_all_words_in_text_in_lower ("сбрось", "настройки"):
            self._IS_NEW_USER = True
            self._INTERSESSIONAL_DATA["new_user"] = True
            self._INTERSESSIONAL_DATA["last_lesson"] = 0
            self._INTERSESSIONAL_DATA["last_task"] = 0
            self._NEW_TEXT = "Настройки сброшены."
        
        elif self._has_one_word_in_text_in_lower (
            "курс", "курса", "курсу", "курсе", "курсом"):
            last_lesson: int = self._INTERSESSIONAL_DATA["last_lesson"]
            self._NEW_TEXT = get_text_that_says_which_lesson_user_stopped (last_lesson) + "\n"
            self._NEW_TEXT += "Его тема: " + get_theme_of_lesson (last_lesson) + "\n"
            self._NEW_TEXT += "Хотите перейти к следующему уроку?"
            # FIXME
        
        elif self._has_one_word_in_text_in_lower (
            "пока", "пака", "прощай", "свидания", "пора", "чао"):
            self._NEW_TEXT = get_farewell_text ( )
            self._IS_END_SESSION = True

        else:
            self._NEW_TEXT = get_apology_text ( )

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
            "response": {"text": self._NEW_TEXT, "end_session": self._IS_END_SESSION},
            "session_state": self._SESSION_DATA,
            "user_state_update": self._INTERSESSIONAL_DATA
            }



# Функция, вызываемая Яндексом для запуска скрипта Алисы (в коде вызывать её не нужно).
def main (request_from_alisa: dict, context) -> dict:
    handler_of_alisa = HandlerOfAlisa (request_from_alisa)
    return handler_of_alisa.get_response ( )