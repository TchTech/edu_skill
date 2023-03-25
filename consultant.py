from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import json
def index_of_max(lst):
    maxi = 0
    for i in range(len(lst)):
        if lst[i] > lst[maxi]:
            maxi = i
    return maxi
class ArtificialIntelligence:
    def __init__(self, name_of_file):
        russian_stopwords = stopwords.words("russian")
        with open(name_of_file, "r", encoding="utf-8") as f:
            doc = dict(json.load(f))
            self.base = []
            [self.base.extend(i) for i in [list(i.values()) for i in list(doc.values())]]
        self.vectorizer = TfidfVectorizer(stop_words=russian_stopwords)
        self.docs_tfidf = self.vectorizer.fit_transform(b)
    def get_similarity(self, query):
        query_tfidf = self.vectorizer.transform([query])
        return self.base[index_of_max(list(cosine_similarity(query_tfidf, self.docs_tfidf).flatten()))]

# q = input()
# a = ArtificialIntelligence("course.json")
# print("Найдено:", a.get_similarity(q))