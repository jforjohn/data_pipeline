from os import path
import pandas as pd
import sys
from celery.utils.log import get_task_logger
from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError

# Create logger - enable to display messages on task logger
celery_log = get_task_logger(__name__)

PROJECT_PATH = path.join(
    path.dirname(path.abspath(__file__)),
    path.pardir
)

### import custom lib
sys.path.append(PROJECT_PATH)
from utils.config_loader import load

# use default value for config file
config = load()

# TODO: fix invalid literal for int() with base 10 for integer env vars
DB_PORT = config.get('credentials', 'DB_PORT')
DB_USER = config.get('credentials', 'DB_USER')
DB_PASS = config.get('credentials', 'DB_PASSWORD')
DB_NAME = config.get('credentials', 'DB_NAME')
DB_HOST = config.get('credentials', 'DB_HOST')
# db engine
# api_ml_postgres
engine = create_engine(
    f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )

def dbwrite():
    """
    This function just writes the csv file in the data.
    We could parameterize it but it's not needed for now
    """
    data_folder = config.get('data', 'folder')
    metadata = config.get('data', 'metadata')
    images = config.get('data', 'images')
    metadata_path = path.join(data_folder, metadata)
    celery_log.info(metadata_path)
    images_path = path.join(data_folder, images)
    
    df = pd.read_csv(metadata_path,
                     sep=',',
                     header = 'infer',
                     error_bad_lines = False)
    df['url'] = df['id'].map(
        lambda x: path.join(images_path, f'{str(x)}.jpg')
        )
    df.set_index('id', inplace=True)
    try:
        df.to_sql('styles_data', engine, if_exists='replace',index=True)
    except DatabaseError as e:
        celery_log.error(f'No connection to DB: {e}')
        return 'Not ok'
    return 'ok'

def dbsimplequery(filters):
    """
    Simple conjunctive query
    :param filters: dict 
    """
    where_cond = [f"{k}='{v}'" for k,v in filters.items()]
    where_sql = (' and ').join(where_cond)
    if where_sql:
        where_sql = 'where ' + where_sql
    query = f'select * from "styles_data" {where_sql}'
    df = pd.read_sql_query(query, con=engine)
    df.drop_duplicates(inplace=True)
    return df, config
