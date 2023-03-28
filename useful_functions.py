from json_manager import *


def create_sessional_data (sessional_data: dict) -> dict:
    if sessional_data == { }: # То есть это первое сообщение
        return {
                "state": "in_main_menu",
                "last_output_text": "",
                "last_text_to_speech": "",
                "last_buttons": [ ],
                "last_card": { },
                "text_of_quest": "",
                "correct_answer_of_quest": 0,
                "difficulty_level_of_quest": 0,
                "number_of_correct_quest_answers": 0,
                "number_of_wrong_quest_answers": 0,
                "was_said_that_user_can_change_difficulty_level_in_quest": False,

                "title_of_task": "",
                "text_of_task": "",
                "difficulty_level_of_task": 0,
                "solve_of_task": "",
                "code_of_task": ""
                }
        # Все состояния: in_main_menu, working_with_course, choosing_course_theme, start_next_lesson_or_not,
        # working_with_quest, choosing_right_answer_for_quest, choosing_between_repeating_and_changing_difficulty_level,
        # viewing_quest_results, working_with_tasks, sending_report, consulting.
    else: # Значит, сообщение уже не первое
        return sessional_data


def create_intersessional_data (intersessional_data: dict) -> dict:
    if not "new_user" in intersessional_data.keys() or intersessional_data["new_user"]:
        return {
            "new_user": True,
            "current_lesson": "",
            "current_sublesson": ""
            }
    else:
        return intersessional_data


def get_user_greeting ( ) -> str:
    hello_text = get_hello_text ( ) + "\n"
    hello_text += get_text_asking_if_user_has_forgotten_commands ( ) + "\n"
    #hello_text += get_main_commands_of_skill ( )
    return hello_text


def get_text_that_says_user_is_just_in_main_menu ( ) -> str:
    return "Вы на главном меню!"

def get_text_that_says_what_skill_can_do ( ) -> str:
    return "Давайте расскажу, Я - ваш личный эксперт в области Python. Хотите отдохнуть и послушать курс? или потренироваться на практике в задачах и квесте? А может получить оценку своих знаний теории? Я всегда готова вам помочь! Может вы хотите получить консультацию от моего гениального интеллекта либо узнать как пофиксить ошибку? Тут я тоже могу подсказать. Так чем бы вы хотели заняться?"


def create_buttons (*button_texts: str) -> list[dict]:
    ready_buttons = [ ]
    for text_of_button in button_texts:
        ready_buttons.append ({"title": text_of_button, "hide": True})
    return ready_buttons

def create_buttons_in_text (*button_texts: str) -> list[dict]:
    ready_buttons = [ ]
    for text_of_button in button_texts:
        ready_buttons.append ({"title": text_of_button, "hide": False})
    return ready_buttons


def create_buttons_of_main_menu ( ) -> list:
    return create_buttons (*get_main_commands_of_skill_as_list ( ))

def create_buttons_of_main_menu_in_text ( ) -> list:
    return create_buttons_in_text (*get_main_commands_of_skill_as_list ( ))


def calculate_python_knowledge (number_of_correct_answers: int,
                                number_of_wrong_answers: int) -> float:
    if number_of_correct_answers == number_of_wrong_answers:
        python_knowledge = 50 # 50% знания Python
    else:
        python_knowledge = number_of_correct_answers / (number_of_correct_answers + number_of_wrong_answers) * 100

    return round (python_knowledge, 1)


def code_to_speech(code: str) -> str:
    """Переводит код в слова и выводит готовый текст в пронумерованном столбце."""
    REPLACEMENTS: dict = _get_replacements ( )
    
    PAUSE = "sil <[250]>"
    lines = code.split("\n")
    formatted_lines = [ ]
    for i, line in enumerate(lines, start=1):
        formatted_line = line
        for key in REPLACEMENTS.keys():
            formatted_line = formatted_line.replace(key, REPLACEMENTS[key])
        formatted_lines.append(f"{PAUSE} строка {i} {PAUSE} {formatted_line}")
    return "\n".join(formatted_lines) + PAUSE

def _get_replacements ( ) -> dict:
    """Возвращает словарь с заменами символов на слова."""
    return {
        ")": " скобка закрывается ",
        "(": " скобка открывается ",
        "*": " звёздочка ",
        "'": " кавычки ",
        '"': " кавычки ",
        "{": " фигурная скобка открывается ",
        "}": " фигурная скобка закрывается ",
        ":": " двоеточие ",
        "!": " восклицательный знак ",
        ".": " точка ",
        ",": " запятая ",
        "[": " квадратная скобка открывается ",
        "]": " квадратная скобка закрывается ",
        "||": " две вертикальные линии (операция или) ",
        ">": " больше ",
        "<": " меньше ",
        "/": " разделить ",
        "-": " минус ",
        "+": " плюс ",
        "%": " процент ",
        "@": " собачка ",
        "&": " амперсанд "
    }


def make_big_win_picture (title: str, description: str = "") -> dict:
    return {
        "type": "BigImage",
        "image_id": get_random_win_picture ( ),
        "title": title,
        "description": description
    }

def make_big_level_up_picture (title: str, description: str = "") -> dict:
    return {
        "type": "BigImage",
        "image_id": get_random_level_up_picture ( ),
        "title": title,
        "description": description
    }

def make_big_looking_results_picture (title: str, description: str = "") -> dict:
    return {
        "type": "BigImage",
        "image_id": get_random_looking_results_pictures ( ),
        "title": title,
        "description": description
    }

def make_big_farewell_picture (title: str, description: str = "") -> dict:
    return {
        "type": "BigImage",
        "image_id": get_random_farewell_picture ( ),
        "title": title,
        "description": description
    }