"""
This module should contain the asynchronous tasks that power
this project
"""
from celery import Celery
from .config import Config
from .schemas import TaskResultSchema
from .scraping import fetch_page_text
from .nlp import get_frequent_tokens
from .models import URL, Token


CELERY = Celery(__name__, broker=Config.REDIS_HOST, backend=Config.REDIS_HOST)


@CELERY.task(bind=True)
def frequency_analysis(self, url: str) -> str:
    """
    Takes care of fetching a web page, extracting its tokens,
    and getting the frequency of its non-stopword tokens.
    Args:
        url: The URL of the web page to analyze.
    Returns:
        A collection that contains the tokens encountered on the
        web page, and their counts. JSON serialized.
    """
    print("Frequency Analysis Task")
    page_text = fetch_page_text(url)
    counts = get_frequent_tokens(page_text, 100)
    result = TaskResultSchema(many=True).dumps(counts).data
    print(result)
    store_in_db.delay(url, result)
    return result


@CELERY.task(bind=True)
def store_in_db(self, url: str, json_counts: str):
    """
    Takes care of updating the DB with the token counts obtained
    from a web page, if the web page has not been analyzed before.
    Args:
        url: the URL of the page analyzed
        json_counts: contains the tokens encountered and their frequencies
    """
    print("Store in DB Task")
    counts = TaskResultSchema(many=True).loads(json_counts).data
    enc = self.app.conf["encryptor"]
    if URL.get_by_hash(url, enc) is None:
        print(f"{url} is new")
        URL.new(url, enc)
        Token.batch_update(counts, enc)
        return
    print(f"{url} is not new")


@CELERY.task
def sentiment_analysis():
    print("Sentiment Analysis Task")
    raise NotImplementedError()
