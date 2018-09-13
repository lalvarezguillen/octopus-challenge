import re
from typing import Iterator, Dict, Union, List
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords


ENGLISH_STOPWORDS = stopwords.words("english")
WORD_PATTERN = re.compile("[a-zA-Z]")


def is_word(text: str) -> bool:
    return bool(re.findall(WORD_PATTERN, text))


def tokenize_text(text: str) -> Iterator[str]:
    for token in word_tokenize(text.lower()):
        if is_word(token) and token not in ENGLISH_STOPWORDS:
            yield token


TokenCount = Dict[str, Union[str, int]]


def get_frequent_tokens(text: str, top_n: int) -> List[TokenCount]:
    counter: Dict[str, int] = Counter()
    for token in tokenize_text(text):
        counter[token] += 1
    counts = [
        {"token": token, "frequency": count} for token, count in counter.items()
    ]
    counts.sort(key=lambda elem: elem["frequency"], reverse=True)
    return counts[:top_n]

