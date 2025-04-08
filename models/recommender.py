import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class AssessmentRecommender:
    def __init__(self):
        self.data = pd.read_csv('data/assessments.csv')
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.data['Description'])

    def get_recommendations(self, query, top_n=5):
        query_vec = self.vectorizer.transform([query])
        similarity = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        top_indices = similarity.argsort()[-top_n:][::-1]

        results = []
        for idx in top_indices:
            title = self.data.iloc[idx]['Title']
            desc = self.data.iloc[idx]['Description']
            url = self.data.iloc[idx]['URL']
            results.append((title, desc, url))
        return results
