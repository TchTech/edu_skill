from json_manager import get_main_commands_of_skill_as_list


class Buttons:
    """Класс для работы с кнопками Алисы."""
    def __init__ (self):
        self.BUTTONS = [ ]

    def add_buttons (self, *button_texts: str, hide_all: bool) -> None:
        """Добавляет новые кнопки."""
        for button_text in button_texts:
            self.BUTTONS.append ({"title": button_text, "hide": hide_all})

    def remove_all_buttons (self) -> None:
        """Удаляет все кнопки."""
        self.BUTTONS = [ ]

    def add_buttons_of_main_menu_in_text (self) -> None:
        """Добавляет команды навыка на главное меню в текст."""
        self.add_buttons (*get_main_commands_of_skill_as_list ( ), hide_all = False)


if __name__ == '__main__':
    buttons = Button ( )
    buttons.add_buttons ("test1", "test2", "test3", hide_all = True)
    print (buttons.BUTTONS)