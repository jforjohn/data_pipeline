from fastapi import APIRouter
from .models import Task, Result, FilterData
from celery.result import AsyncResult
from fastapi.responses import JSONResponse
from os import path
import sys

PROJECT_PATH = path.join(
    path.dirname(path.abspath(__file__)),
    path.pardir
)

### import custom lib
sys.path.append(PROJECT_PATH)

from celery_worker.tasks import worker2db, worker2query, worker2transform

router = APIRouter()

@router.get('/')
def touch():
    return 'API is running'

@router.post('/insert2db', response_model=Task, status_code=202)
async def insert2db():
    task_id = worker2db.delay()
    return {'task_id': str(task_id), 'status': 'Processing'}

@router.post('/query', response_model=Task, status_code=202)
async def queryData(filters:FilterData):
    # remove NA filters
    filters = dict(filter(
        lambda item: item[1] is not None, dict(filters).items()
        ))
    task_id = worker2query.delay(filters)
    return {'task_id': str(task_id), 'status': 'Processing'}

@router.post('/transformedquery', response_model=Task, status_code=202)
async def transformedQueryData(filters:FilterData):
    # remove NA filters
    filters = dict(filter(
        lambda item: item[1] is not None, dict(filters).items()
        ))
    task_id = worker2transform.delay(filters)
    return {'task_id': str(task_id), 'status': 'Processing'}

@router.get('/result/{task_id}', response_model=Result, status_code=200,
            responses={202: {'model': Task, 'description': 'Accepted: Not Ready'}})
async def fetch_result(task_id):
    # Fetch result for task_id
    task = AsyncResult(task_id)
    if not task.ready():
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': 'Processing'})
    result = task.get()
    return {'task_id': task_id, 'status': str(result)}