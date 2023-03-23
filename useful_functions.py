from json_manager import *


def create_sessional_data (sessional_data: dict) -> dict:
    if sessional_data == { }: # То есть это первое сообщение
        return {"working_with_course": False,
                "working_with_quest": False,
                "choosing_right_answer_for_quest": False,
                "choosing_between_repeating_and_changing_difficulty_level": False,
                "text_of_quest": "",
                "correct_answer_of_quest": 0,
                "difficulty_level": 0,
                "number_of_correct_quest_answers": 0,
                "number_of_wrong_quest_answers": 0,
                "viewing_quest_results": False,
                "was_said_that_user_can_change_difficulty_level": False,
                "working_with_tasks": False,
                "sending_report": False,
                "consulting": False
                }
    else: # Значит, сообщение уже не первое
        return sessional_data


def create_intersessional_data (intersessional_data: dict) -> dict:
    if not "new_user" in intersessional_data.keys() or intersessional_data["new_user"]:
        return {
            "new_user": True,
            "last_lesson": 0,
            "last_task": 0
            }
    else:
        return intersessional_data


def get_user_greeting ( ) -> str:
    hello_text = get_hello_text ( ) + "\n"
    hello_text += get_text_asking_if_user_has_forgotten_commands ( ) + "\n"
    #hello_text += get_main_commands_of_skill ( )
    return hello_text


def get_text_that_says_user_is_just_in_main_menu ( ) -> str:
    return "Вы на главном меню!\nМои основные команды:"


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