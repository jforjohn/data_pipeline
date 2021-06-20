from os import path
import pandas as pd
import sys
from celery.utils.log import get_task_logger

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
    
    df = pd.read_csv(metadata_path, sep=',', header = 'infer',error_bad_lines = False)
    celery_log.info(df)
