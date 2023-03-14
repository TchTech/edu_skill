import json


with open ("texts_for_users.json", "r") as file:
    texts_for_users = json.load (file)


def get_text_for_new_user ( ) -> str:
    return texts_for_users["for_new_user"]