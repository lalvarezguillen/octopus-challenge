from celery import Celery
from .config import REDIS_HOST
from .schemas import TaskResultSchema
from .http import fetch_page_text
from .nlp import get_frequent_tokens


CELERY = Celery("octopus", broker=REDIS_HOST, backend=REDIS_HOST)


@CELERY.task
def frequency_analysis(url: str) -> str:
    print("Frequency Analysis Task")
    page_text = fetch_page_text(url)
    counts = get_frequent_tokens(page_text, 100)
    result = TaskResultSchema(many=True).dumps(counts).data
    print(result)
    store_in_db.delay(url, result)
    return result


@CELERY.task
def store_in_db(url: str, counts: str):
    pass


@CELERY.task
def sentiment_analysis():
    print("Sentiment Analysis Task")
    pass
