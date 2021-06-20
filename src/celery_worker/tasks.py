from .worker import celery_app
from celery.utils.log import get_task_logger
from os import path
import sys

PROJECT_PATH = path.join(
    path.dirname(path.abspath(__file__)),
    path.pardir
)

### import custom lib
sys.path.append(PROJECT_PATH)

from db_scripts.insert2db import dbwrite

# Create logger - enable to display messages on task logger
celery_log = get_task_logger(__name__)

@celery_app.task(name='insert2db')
def worker2db():
    celery_log.info(f"Celery task: insert2db edo!")
    dbwrite()
    celery_log.info(f"Celery task: insert2db completed!")
    return 'OK'

@celery_app.task(name='test')
def reverse():
    text = 'Jay'
    return text[::-1]