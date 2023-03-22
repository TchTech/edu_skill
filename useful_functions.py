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
    hello_text += get_main_commands_of_skill ( )
    return hello_text


def get_text_that_says_user_is_just_in_main_menu ( ) -> str:
    return "Вы на главном меню!\nМои основные команды:\n" + get_main_commands_of_skill ( )
