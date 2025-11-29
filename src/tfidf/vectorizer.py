from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def compute_global_tfidf(texts, custom_stopwords, min_df=2, max_df=0.95):
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 1),
        min_df=min_df,
        max_df=max_df
    )

    matrix = vectorizer.fit_transform(texts)
    terms = vectorizer.get_feature_names_out()

    mask = np.array([t not in custom_stopwords for t in terms])
    filtered_terms = terms[mask]
    filtered_matrix = matrix[:, mask]

    return filtered_matrix, filtered_terms
