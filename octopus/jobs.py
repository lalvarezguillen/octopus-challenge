from celery import Celery
from .config import REDIS_HOST
from .schemas import TaskResultSchea


CELERY = Celery("octopus", broker=REDIS_HOST, backend=REDIS_HOST)


@CELERY.task
def frequency_analysis(url: str) -> str:
    print("Frequency Analysis Task")
    dummy_data = [
        {"token": "token1", "frequency": 5},
        {"token": "token2", "frequency": 3},
    ]
    result = TaskResultSchea(many=True).dumps(dummy_data).data
    print(result)
    return result


@CELERY.task
def sentiment_analysis():
    print("Sentiment Analysis Task")
    pass
