import sys

sys.path.insert(0, '/app')

from foodgram.celery import app as celery_app

__all__ = ('celery_app',)