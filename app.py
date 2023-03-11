import requests
import json
import csv
from responses import Responses
from csv_manager import CSV
from flask import Flask, request

# Создание экземпляра Flask
app = Flask(__name__)

# Инициализация глобальных переменных
version = "1.0"
list_lessons = ["введение", "комментарии", "переменные"]

db = CSV("users.csv")

with open("lessons.json", "r", encoding="utf-8") as f:
    lessons = json.load(f)

max_index = len(lessons) - 1

with open("buttons.json", "r", encoding="utf-8") as f:
    buttons = json.load(f)


# Создание вебхука
@app.route("/", methods=["POST"])
def webhook():
    global version

    data = request.json

    response = Responses(version=version)

    # Проверка наличия пользователя в базе данных и добавление его, если он новый
    if not db.check(data["session"]["user"]["user_id"]):
        db.write({
            "id": data["session"]["user"]["user_id"],
            "lesson": 0,
            "stage": 0
        })
    
    user_info = db.read(data["session"]["user"]["user_id"])
    user_lesson = int(user_info["lesson"])
    user_lesson_str = list_lessons[int(user_info["lesson"])]
    user_stage = int(user_info["stage"])

    # Обработка первого запроса пользователя
    if data["session"]["new"]:
        return response.simply_response("Добро пожаловать!", "Добро пожаловать!", buttons["главное меню"])

    # Обработка запроса на выход на главное меню
    elif data["request"]["command"] in ["на главное меню"]:
        return response.simply_response("Главное меню", "Главное меню", buttons["главное меню"])

    # Обработка запроса на выбор урока.
    elif data["request"]["command"] == "начать изучение":
        return response.simply_response("Выберите урок", "Выберите урок", buttons["изучение"])
    
    # Обработка запроса на продолжение чтения урока.
    elif data["request"]["command"] == "продолжить изучение":
        text = "В прошлый раз вы остановились на " + str(user_stage) + " стадии " + str(user_lesson) + " урока:\n"
        text += lessons[user_lesson_str]["text"][user_stage]
        return response.simply_response(text, text, buttons["урок"])

    # Обработка запроса на выбор конкретного урока.
    elif data["request"]["command"] in list_lessons:
        text = lessons[data["request"]["command"]]["text"][0]

        db.write({
            "id": user_info["id"],
            "lesson": lessons[data["request"]["command"]]["index"],
            "stage": 0,
        })

        return response.simply_response(text, text, buttons["урок"])

    # Обработка запроса на переход к следующей стадии урока.
    elif data["request"]["command"] in ["дальше"]:
        if user_stage == (lessons[user_lesson_str]["max_index"] -1):
            text = lessons[user_lesson_str]["text"][user_stage + 1]

            db.write({
                "id": user_info["id"],
                "lesson": user_info["lesson"],
                "stage": user_stage + 1,
            })

            if user_lesson == max_index:
                return response.simply_response(text, text, buttons["конец обучения"])
            else:
                return response.simply_response(text, text, buttons["конец урока"])

        else:
            text = lessons[user_lesson_str]["text"][user_stage + 1]

            db.write({
                "id": user_info["id"],
                "lesson": user_info["lesson"],
                "stage": user_stage + 1,
            })

            return response.simply_response(text, text, buttons["урок"])

    # Обработка запроса на переход к следующему уроку.
    elif data["request"]["command"] in ["следующий урок"]:
        
        text = lessons[list_lessons[user_lesson + 1]]["text"][0]

        db.write({
            "id": user_info["id"],
            "lesson": user_lesson + 1,
            "stage": 0
        })

        return response.simply_response(text, text, buttons["урок"])
    
    else:
        return response.simply_response("Извините, я Вас не понял", "Извините, я Вас не понял", buttons["главное меню"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

#Elon was here