"""
Celery workers should be started from this module.
"""
from backend.app import CELERY, make_app, setup_db


setup_db()
app = make_app()
