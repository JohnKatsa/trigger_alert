from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class diff_checker:
    
    def tf_idf(self, new_document, old_document):
        vectorizer = TfidfVectorizer()
        t = vectorizer.fit_transform([old_document, new_document])
        return t
        
    def cosine(self, t):
        return cosine_similarity(t)[0][1]