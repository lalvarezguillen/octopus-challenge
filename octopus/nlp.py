"""
This module contains code to handle the Natural Language
Processing needs of this project.
"""
import re
from typing import Iterator, Dict, Union, List
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords


ENGLISH_STOPWORDS = stopwords.words("english")
WORD_PATTERN = re.compile("[a-zA-Z]")


def is_word(token: str) -> bool:
    """
    Checks whether a token looks like a word, in a rather
    naive fashion. It just checks whether the token contains
    at least a letter

    Args:
        token: The token to check
    Returns:
        Whether the token looks like a word.
    """
    return bool(re.findall(WORD_PATTERN, token))


def tokenize_text(text: str) -> Iterator[str]:
    """
    Extracts the non-stopword tokens of a text.
    Args:
        text: the text to tokenize
    Returns:
        A collection that contains the tokens of the text.
    """
    for token in word_tokenize(text.lower()):
        if is_word(token) and token not in ENGLISH_STOPWORDS:
            yield token


TokenCount = Dict[str, Union[str, int]]


def get_frequent_tokens(text: str, top_n: int) -> List[TokenCount]:
    """
    Extracts the top_n most frequent words of a text, excluding English
    stopwords; with their counts.
    Args:
        text: The text to process
        top_n: The number of top most frequent words to extract.
    Returns:
        A collection of the frequent tokens and their frequencies.
    """
    counter: Dict[str, int] = Counter()
    for token in tokenize_text(text):
        counter[token] += 1
    counts = [
        {"token": token, "frequency": count} for token, count in counter.items()
    ]
    counts.sort(key=lambda elem: elem["frequency"], reverse=True)
    return counts[:top_n]
