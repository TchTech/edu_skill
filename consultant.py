from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import pymorphy3
morph = pymorphy3.MorphAnalyzer()

def index_of_max(lst):
    maxi = 0
    for i in range(len(lst)):
        if lst[i] > lst[maxi]:
            maxi = i
    return maxi
class ArtificialIntelligence:
    def __init__(self, name_of_file):
        with open(name_of_file, "r", encoding="utf-8") as f:
            doc = dict(json.load(f))
            self.base = []
            [self.base.extend(i) for i in [list(i.values()) for i in list(doc.values())]]
        self.vectorizer = TfidfVectorizer()
        self.docs_tfidf = self.vectorizer.fit_transform(self.base)
    def get_similarity(self, query):
        query = self.lemmatize(self.filter_of_query(query))
        query_tfidf = self.vectorizer.transform([query])
        return self.base[index_of_max(list(cosine_similarity(query_tfidf, self.docs_tfidf).flatten()))]
    def filter_of_query(self, query):
        stop_words = ["не", "без", "через", "у", "но", "о", "и", "как", "python", "а", "к", "в", "с", "за", "или", "либо", "же", "ж", "совсем", "ничуть", "отнюдь", "перед", "при", "про", "под", "по", "до", "чуть", "чуть-чуть"]
        return " ".join([i for i in query.split(" ") if not i in stop_words])
    def lemmatize(self, text):
        words = text.split() # разбиваем текст на слова
        res = list()
        for word in words:
            p = morph.parse(word)[0]
            res.append(p.normal_form)

        return " ".join(res)

# q = input()
# a = ArtificialIntelligence("lessons.json")
# print("Найдено:", a.get_similarity(q))
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
def output_format(text):
    a = text.split(" ** ")
    a[1] = str(a[1]).upper()
    text = " ".join(a)
    c = text.split("`")
    text = " ".join(c)
    return c
def tts_format(text):
    c = text.split("`")
    i = 2
    while i<len(c):
        c[i] = code_to_speech(c[i])
        i+=2
