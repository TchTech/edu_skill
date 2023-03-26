import json
import random


with open ("texts_for_users.json", "r") as file:
    texts_for_users = json.load (file)



def get_text_for_new_user ( ) -> str:
    return texts_for_users["for_new_user"]


def get_hello_text ( ) -> str:
    return random.choice (texts_for_users["hello_text"])


def get_introduction_to_course ( ) -> str:
    return texts_for_users["introduction_to_course"]


def get_text_asking_if_user_has_forgotten_commands ( ) -> str:
    return random.choice (texts_for_users["if_user_has_forgotten_commands"])


def get_main_commands_of_skill_as_list ( ) -> list[str]:
    return texts_for_users["main_commands_of_skill"]


def get_main_commands_of_skill ( ) -> str:
    commands_of_skill = ""
    for command in texts_for_users["main_commands_of_skill"]:
        commands_of_skill += command + "\n"
    return commands_of_skill


def get_text_that_says_which_lesson_user_stopped (lesson_number: int) -> str:
    return random.choice (texts_for_users["you_stopped_at_lesson"]) + str (lesson_number)


def get_theme_of_lesson (lesson_number: int) -> str:
    return "ЗАТЫЧКА"
    #return lessons[str(lesson_number)]["theme"]


def get_lesson_text (lesson_number: int) -> str:
    return "Затычка..."


def get_text_that_says_which_task_user_stopped (task_number: int) -> str:
    return random.choice (texts_for_users["you_stopped_at_task"]) + str (task_number)


def get_text_that_says_answer_is_correct ( ) -> str:
    return random.choice (texts_for_users["correct_answer"])


def get_text_that_says_answer_is_wrong ( ) -> str:
    return random.choice (texts_for_users["wrong_answer"])


def get_text_that_says_there_is_no_answer_like_that ( ) -> str:
    return random.choice (texts_for_users["there_is_no_answer_like_that"])


def get_text_that_suggests_to_continue_or_change_difficulty_level ( ) -> str:
    return random.choice (texts_for_users["continue_or_change_difficulty_level"])


def get_apology_text ( ) -> str:
    return random.choice (texts_for_users["something_is_unclear"])
    # Выбирается одно случайное извинение от Алисы, если она что-то не поняла.


def get_farewell_text ( ) -> str:
    head_of_farewell: str = random.choice (texts_for_users["head_of_farewell"])
    body_of_farewell: str = random.choice (texts_for_users["body_of_farewell"])
    return head_of_farewell + body_of_farewell
    # Достаётся начало прощания, например: "До свидания";
    # а потом тело прощания, например: ", хорошего дня!"


def get_random_win_sound ( ) -> str:
    return random.choice (texts_for_users["win_sounds"])

def get_random_lose_sound ( ) -> str:
    return random.choice (texts_for_users["lose_sounds"])

def get_random_sound_of_looking_results ( ) -> str:
    return random.choice (texts_for_users["sound_of_looking_results"])

def get_introduction_sound ( ) -> str:
    return "<speaker audio=\"dialogs-upload/5cef3ba2-6ab9-4297-8e09-176c9297e1b1/d5cbb919-c5c1-4691-a8f5-ebdfdee3152d.opus\">"