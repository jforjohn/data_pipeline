from .worker import celery_app
from celery.utils.log import get_task_logger
from .db_scripts import dbwrite, dbsimplequery
from .create_results import save_results

# Create logger - enable to display messages on task logger
celery_log = get_task_logger(__name__)

@celery_app.task(name='insert2db')
def worker2db():
    celery_log.info(f"Celery task: insert2db started!")
    ret = dbwrite()
    celery_log.info(f"Celery task: insert2db completed!")
    return ret

@celery_app.task(name='dbsimplequery')
def worker2query(filters, transformations=False, cur_taskid=None):
    celery_log.info(f"Celery task: simple query started!")
    if cur_taskid is None:
        cur_taskid = worker2query.request.id
    df, config = dbsimplequery(filters)
    ret = save_results(df, config, 
                       cur_taskid,
                       transformations)
    celery_log.info(f"Celery task: simple query completed!")
    return ret

@celery_app.task(name='dbquerytransform')
def worker2transform(filters):
    cur_taskid = worker2transform.request.id
    ret = worker2query(filters, transformations=True, cur_taskid=cur_taskid)
    return ret

@celery_app.task(name='test')
def reverse():
    text = 'Jay'
    return text[::-1]