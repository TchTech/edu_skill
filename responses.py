# Класс содержащий различные виды ответов для Алисы
class Responses:

    # Инициализатор для всовывания конца сессии и версии в атрибуты класса
    def __init__(self, version: str):
        self.version = version

    # Обыкновенный ответ в виде текста
    def simply_response(self, response_text: str, response_speak: str, buttons: dict):
        # Тело ответа
        response = {
            "response": {
                "text": response_text,
                "tts": response_speak,
                "end_session": False,
                "buttons": buttons
            },
            "version": self.version
        }

        return response

    # Прощальный ответ
    def bye_response(self, response_text: str, response_speak: str):
        # Тело ответа
        response = {
            "response": {
                "text": response_text,
                "tts": response_speak,
                "end_session": True
            },
            "version": self.version
        }

        return response

    # Ответ в виде карточки
    def card_response(self, image_id: str, title_card: str, response_text: str, response_speak: str, buttons: dict):
        # Тело ответа
        response = {
            "response": {
                "text": response_text,
                "tts": response_speak,  # Алиса будет это говорить
                "end_session": False,
                # Кнопка которая и станет первой командой пользователя с подсчётом ценности продукта (например, чая) при первом запуске навыка и команда "Помощь" если пользователь уже пользовался навыком
                "buttons": buttons,

                # Карточка - блок с картинкой, далее заголовком и текстом
                "card": {
                    "type": "BigImage",
                    # Алиса будет это отображать сверху карточки (Картинка)
                    "image_id": image_id,
                    # Это текст заголовка (под картинкой)
                    "title": title_card,
                    # Это текст карточки (под заголовком)
                    "description": response_text,
                }
            },
            "version": self.version
        }

        return
