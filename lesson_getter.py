import json

# def output_format(text):
#     c = text.split("`")
#     text = " ".join(c)
#     return text

class LessonGetter:
	"""Класс для работы с уроками, курсом в целом."""
	def __init__ (self):
		self._load_all_lessons_from_file ( )
		self.themes = [lesson_theme for lesson_theme in self.all_lessons.keys()]

	def _load_all_lessons_from_file (self) -> None:
		with open (self._name_of_file_with_lessons, "r") as file_with_lessons:
			self.all_lessons: dict = json.load (file_with_lessons)

	@property
	def _name_of_file_with_lessons (self) -> str:
		return "lessons.json"


	def get_subtheme_names (self, theme: str) -> list[str]:
		"""Получить имена подтем указанной темы."""
		return [lesson_subtheme for lesson_subtheme in self.all_lessons[theme].keys()]

	def get_first_subtheme_name (self, theme: str) -> str:
		"""Получить имя первой подтемы указанной темы."""
		return self.get_subtheme_names (theme = theme)[0]

	def get_subtheme_text (self, theme: str, subtheme: str) -> str:
		"""Получить подтему указанной темы."""
		return subtheme + ": " + self.all_lessons[theme][subtheme]

	def get_name_of_next_theme (self, current_theme: str) -> str:
		"""Получить имя следующей темы."""
		index_of_current_theme = self.themes.index (current_theme)
		index_of_next_theme = index_of_current_theme + 1
		try:
			return self.themes[index_of_next_theme]
		except IndexError:
			return "" # Значит, эта тема последняя

	def get_name_of_next_subtheme (self, theme: str, subtheme: str) -> str:
		"""Получить имя следующей подтемы."""
		subthemes = self.get_subtheme_names (theme)
		index_current_subtheme = subthemes.index (subtheme)
		index_of_next_subtheme = index_current_subtheme + 1
		try:
			return subthemes[index_of_next_subtheme]
		except IndexError:
			return "" # Значит, эта подтема последняя