import requests
from bs4 import BeautifulSoup


RETRIABLE = list(range(500, 600)) + [429]


class RetriableHTTPException(Exception):
    pass


def fetch_page_text(url: str) -> str:
    resp = requests.get(url)
    if resp.status_code in RETRIABLE:
        raise RetriableHTTPException

    soup = BeautifulSoup(resp.text)
    for script in soup("script"):
        script.extract()
    return soup.get_text()
