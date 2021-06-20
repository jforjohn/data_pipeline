from fastapi import APIRouter
#from .models import 
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

from celery_worker.tasks import worker2db

router = APIRouter()

@router.get('/')
def touch():
    return 'API is running'

'''@router.get('/health')
def health_check():
    content = {'Server status': 'Ok', 'DB connection': 'Ok'}

    # check DB connection and get the latest ML pipeline version
    try:
        ml_pipeline_version = get_latest_ml_pipeline_version()
    except Exception:
        content['DB connection'] = 'DB unavailable'
        return JSONResponse(content=content)'''

@router.post('/insert2db')
async def insert2db():
    task_id = worker2db.delay()
    return str(task_id)

