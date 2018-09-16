"""
This module should contain the asynchronous tasks that power
this project
"""
from typing import List, Optional
import logging
import requests
from celery import Celery
from .config import Config
from .schemas import TaskResultSchema
from .scraping import fetch_page_text, RetriableHTTPError, HTTPError
from .nlp import get_frequent_tokens, TokenCount
from .models import URL, Token
from .helpers import retry


CELERY = Celery(__name__, broker=Config.REDIS_HOST, backend=Config.REDIS_HOST)

# Errors worth retrying when trying to fetch a website
HTTPErrors = (
    RetriableHTTPError,
    requests.ConnectionError,
    requests.ConnectTimeout,
)


@CELERY.task(bind=True)
def frequency_analysis(self, url: str) -> Optional[List[TokenCount]]:
    """
    Takes care of fetching a web page, extracting its tokens,
    and getting the frequency of its non-stopword tokens.
    Args:
        url: The URL of the web page to analyze.
    Returns:
        A collection that contains the tokens encountered on the
        web page, and their counts.
    """
    logging.info("Frequency Analysis Task")
    page_text = retry(lambda: fetch_page_text(url), HTTPErrors, times=2)
    counts = get_frequent_tokens(page_text, 100)
    logging.debug(counts)
    store_in_db.delay(url, counts)
    return counts


@CELERY.task(bind=True)
def store_in_db(self, url: str, counts: List[TokenCount]):
    """
    Takes care of updating the DB with the token counts obtained
    from a web page, if the web page has not been analyzed before.
    Args:
        url: the URL of the page analyzed
        counts: contains the tokens encountered and their frequencies
    """
    logging.info("Store in DB Task")
    enc = self.app.conf["encryptor"]
    if URL.get_by_hash(url, enc) is None:
        logging.debug(f"{url} is new")
        URL.new(url, enc)
        Token.batch_update(counts, enc)
        return
    logging.debug(f"{url} is not new")


@CELERY.task
def sentiment_analysis():
    logging.info("Sentiment Analysis Task")
    raise NotImplementedError()
