"""
This module should contain code to handle the web scraping
that this project will need.
"""
import logging
import requests
from bs4 import BeautifulSoup


RETRIABLE = list(range(500, 600)) + [429]
SUCCESS = list(range(200, 300))


class RetriableHTTPError(Exception):
    """
    An http request failed, but it's worth retrying.
    """


class HTTPError(Exception):
    """
    An http request failed, and it shouldn't be retried.
    """


def fetch_page_text(url: str) -> str:
    """
    Fetches a web page, and extracts its actual content (no css,
    js or HTML)
    Args:
        url: The URL of the page to scrape
    Returns:
        The clean content of the website.
    """
    resp = requests.get(url)
    logging.info(resp.status_code)
    if resp.status_code in RETRIABLE:
        raise RetriableHTTPError

    if resp.status_code in SUCCESS:
        soup = BeautifulSoup(resp.text, "html.parser")
        for script in soup("script"):
            script.extract()
        return soup.get_text()

    raise HTTPError
