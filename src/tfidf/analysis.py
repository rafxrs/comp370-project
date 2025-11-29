import pandas as pd

def compute_category_tfidf(df, matrix, terms):
    results = {}

    for coding_value, group in df.groupby("coding"):
        row_ids = group.index.tolist()
        if len(row_ids) < 2:
            continue

        submatrix = matrix[row_ids, :]
        avg_scores = submatrix.mean(axis=0).A1

        tfidf_df = pd.DataFrame({
            "term": terms,
            "score": avg_scores
        }).sort_values("score", ascending=False)

        results[coding_value] = tfidf_df

    return results
