"""
Celery workers should be started from this module.
"""
from backend.app import CELERY, make_app

app = make_app()
