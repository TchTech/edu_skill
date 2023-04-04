import json


class LessonGetter:
    """Класс для работы с уроками Курса.
       В конструкторе принимает тему урока и тему его подурока.
    """
    def __init__ (self, lesson_theme: str, sublesson_theme: str):
        self.current_lesson_theme = lesson_theme
        self.current_sublesson_theme = sublesson_theme
        self._check_current_lesson_theme_and_current_sublesson_theme_in_init ( )
        self._read_file_with_lessons ( )
        self._set_initial_lesson_values_if_necessary ( )
        self._check_sublesson_is_in_lesson ( )

    def _read_file_with_lessons (self) -> None:
        with open (self._name_of_file_with_lessons, "r", encoding = "utf8") as file_with_lessons:
            self.all_lessons: dict = json.load (file_with_lessons)
            self.lesson_themes = tuple (self.all_lessons.keys())
            self._find_sublesson_themes ( )

    @property
    def _name_of_file_with_lessons (self) -> str:
        return "lessons.json"

    def _find_sublesson_themes (self) -> None:
        self.all_sublesson_themes = { }
        for lesson_theme in self.lesson_themes:
            self.all_sublesson_themes[lesson_theme] = tuple (self.all_lessons[lesson_theme].keys())

    def _check_current_lesson_theme_and_current_sublesson_theme_in_init (self) -> None:
        if not self.current_lesson_theme and self.current_sublesson_theme:
            raise ValueError (f"Не указано имя урока в конструкторе класса {__class__.__name__}!")
        elif self.current_lesson_theme and not self.current_sublesson_theme:
            raise ValueError (f"Не указано имя подурока в конструкторе класса {__class__.__name__}!")

    def _set_initial_lesson_values_if_necessary (self) -> None:
        # Если не указаны тема урока и тема его подурока, то
        if not self.current_lesson_theme and not self.current_sublesson_theme:
            # Поставить тему первого урока и тему первого его подурока
            self.current_lesson_theme = self.lesson_themes[0]
            self.current_sublesson_theme = self._get_first_sublesson_theme ( )

    def _get_first_sublesson_theme (self) -> str:
        return self.all_sublesson_themes[self.current_lesson_theme][0]

    def _check_sublesson_is_in_lesson (self) -> None:
        if not self.current_sublesson_theme in self.all_sublesson_themes[self.current_lesson_theme]:
            raise ValueError ("Нет такого подурока в текущем уроке: " +
                             f"\"{self.current_sublesson_theme}\" не принадлежит \"{self.current_lesson_theme}\"!")


    @property
    def text_of_current_sublesson (self) -> str:
        """Текст текущего подурока."""
        return self.all_lessons[self.current_lesson_theme][self.current_sublesson_theme]["text"]

    @property
    def use_function_to_read_code (self) -> bool:
        """Нужно ли использовать функцию для чтения кода."""
        return self.all_lessons[self.current_lesson_theme][self.current_sublesson_theme]["use_function_to_read_code"]


    def move_to_next_sublesson (self) -> None:
        """Перейти к следующему подуроку.
           Если его нет, то current_sublesson_theme будет равен None.
           В случае чего будет возвращена ошибка ValueError с пояснением проблемы.
        """
        sublesson_themes_of_current_lesson = tuple (self.all_sublesson_themes[self.current_lesson_theme])
        self._check_current_sublesson_theme ( )
        index_of_current_sublesson_theme = sublesson_themes_of_current_lesson.index (self.current_sublesson_theme)
        # Если тема текущего подурока не последняя, то
        if self.current_sublesson_theme != sublesson_themes_of_current_lesson[-1]:
            self.current_sublesson_theme = sublesson_themes_of_current_lesson[index_of_current_sublesson_theme + 1]
        else:
            self.current_sublesson_theme = None # Значит, следующей темы подурока нет

    def move_to_next_lesson (self) -> None:
        """Перейти к следующему уроку.
           Если его нет, то current_lesson_theme и current_sublesson_theme будут равны None.
           В случае чего будет возвращена ошибка ValueError с пояснением проблемы.
        """
        self._check_current_lesson_theme ( )
        index_of_current_lesson_theme = self.lesson_themes.index(self.current_lesson_theme)
        # Если тема текущего урока не последняя, то
        if self.current_lesson_theme != self.lesson_themes[-1]:
            self.current_lesson_theme = self.lesson_themes[index_of_current_lesson_theme + 1]
            self.current_sublesson_theme = self._get_first_sublesson_theme ( )
        else:
            self.current_lesson_theme = "" # Значит, все уроки пройдены
            self.current_sublesson_theme = ""

    def move_to_lesson (self, lesson_theme: str) -> None:
        """Перейти к указанному уроку, если он есть.
           Иначе выдать ошибку ValueError."""
        if lesson_theme in self.lesson_themes: self.current_lesson_theme = lesson_theme
        else: raise ValueError ("Нельзя перейти к несуществующему уроку!")
        self.current_sublesson_theme = self._get_first_sublesson_theme ( )


    def _check_current_sublesson_theme (self) -> None:
        if self.current_sublesson_theme is None:
            raise ValueError ("Это последний подурок! Перейти к следующему нельзя!")

    def _check_current_lesson_theme (self) -> None:
        if self.current_lesson_theme is None:
            raise ValueError ("Это последний урок! Перейти к следующему нельзя!")



if __name__ == '__main__':
    lesson_getter = LessonGetter ("", "") # Так должно быть в первый раз
    print ("Все уроки с подуроками:")
    print (lesson_getter.all_sublesson_themes)
    print ( )
    print ("Текущий урок:", lesson_getter.current_lesson_theme)
    print ("Текущий подурок:", lesson_getter.current_sublesson_theme)