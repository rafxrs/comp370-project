import yaml

def build_full_text(df):
    df["full_text"] = (df["title"].astype(str) + " " + df["opening"].astype(str)).str.strip()
    df = df.dropna(subset=["full_text"])
    return df

def normalize_coding(df):
    df["coding"] = (
        df["coding"]
        .astype(str)
        .str.strip()
        .str.replace("–", "-", regex=False)
        .str.replace("—", "-", regex=False)
        .str.lower()
    )
    return df

def load_stopwords(path):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return set(data.get("stopwords", []))
