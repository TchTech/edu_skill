from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

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

        return res

# q = input()
# a = ArtificialIntelligence("lessons.json")
# print("Найдено:", a.get_similarity(q))