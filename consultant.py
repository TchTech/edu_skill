from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json


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
            a = [list(i.values()) for i in list(doc.values())]
            print(a)
            [self.base.extend(i) for i in a]
        self.vectorizer = TfidfVectorizer()
        self.docs_tfidf = self.vectorizer.fit_transform(self.base)

    def get_similarity(self, query):
        query = self.filter_of_query(query)
        query_tfidf = self.vectorizer.transform([query])
        a = list(cosine_similarity(query_tfidf, self.docs_tfidf).flatten())
        return [self.base[index_of_max(a)], max(a)]

    def filter_of_query(self, query):
        stop_words = ["не", "без", "через", "у", "но", "о", "и", "как", "python", "а", "к", "в", "с", "за", "или", "либо", "же", "ж", "совсем", "ничуть", "отнюдь", "перед", "при", "про", "под", "по", "до", "чуть", "чуть-чуть"]
        return " ".join([i for i in query.split(" ") if not i in stop_words])