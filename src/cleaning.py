import re

BOILERPLATE_PATTERNS = [
    r"Create your free profile.*?article",  # NBC login junk
    r"Create your free profile.*?video",    # NBC video junk
    r"Copied",                               # random NBC label
    r"Duration \d+:\d+",                     # CBC video UI text
]


def remove_boilerplate(text: str) -> str:
    """Remove known useless boilerplate patterns."""
    if not text:
        return text
    
    cleaned = text
    for pattern in BOILERPLATE_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE | re.DOTALL)
    return cleaned


def normalize_whitespace(text: str) -> str:
    """Flatten newlines and collapse repeated spaces."""
    if not text:
        return text
    text = text.replace("\n", " ")      # remove newlines
    text = re.sub(r"\s+", " ", text)    # collapse multi-spaces
    return text.strip()


def clean_text(text: str) -> str:
    """Full cleaning pipeline."""
    if not text:
        return text
    text = remove_boilerplate(text)
    text = normalize_whitespace(text)
    return text
