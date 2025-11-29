import pandas as pd

def load_dataset(path):
    def normalize(df):
        df.columns = df.columns.str.strip().str.lower()
        return df

    if path.lower().endswith((".xlsx", ".xls")):
        return normalize(pd.read_excel(path))

    return normalize(pd.read_csv(path, encoding_errors="ignore"))
