import pandas as pd

def build_summary_table(results_dict, top_n):
    codings = list(results_dict.keys())
    data = {coding: [] for coding in codings}

    for coding, df in results_dict.items():
        formatted = [f"{row.term} ({row.score:.4f})" for row in df.head(top_n).itertuples()]
        while len(formatted) < top_n:
            formatted.append("")
        data[coding] = formatted

    summary_df = pd.DataFrame(data)
    summary_df.index = summary_df.index + 1
    summary_df.index.name = "rank"
    return summary_df
