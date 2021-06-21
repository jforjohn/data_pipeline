from pydantic import BaseModel, create_model
from typing import Optional 
class Task(BaseModel):
    # Celery task representation
    task_id: str
    status: str
class Result(BaseModel):
    # Celery task result
    task_id: str
    status: str
class FilterData(BaseModel):
    gender: Optional[str]
    masterCategory: Optional[str]
    subCategory: Optional[str]
    articleType: Optional[str]
    season: Optional[str]
    year: Optional[int]
    usage: Optional[str]
