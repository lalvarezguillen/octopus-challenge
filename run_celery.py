"""
Celery workers should be started from this module.
"""
from octopus.app import CELERY, make_app


app = make_app()
