import pandas as pd

def load_dataset(path):
    path = str(path)

    def normalize(df):
        df.columns = df.columns.str.strip().str.lower()
        return df

    # Excel support
    if path.lower().endswith((".xlsx", ".xls")):
        return normalize(pd.read_excel(path))

    # TSV support
    return normalize(pd.read_csv(path, sep="\t", encoding_errors="ignore"))
