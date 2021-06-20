from celery import Celery
from os import path
import sys

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
RBMPQ_PORT = config.get('credentials', 'RBMPQ_PORT')
print(RBMPQ_PORT)
RBMPQ_USER = config.get('credentials', 'RBMPQ_USER')
RBMPQ_PASS = config.get('credentials', 'RBMPQ_PASS')
RBMPQ_HOST = config.get('credentials', 'RBMPQ_HOST')


BROKER_CONN_URI = f"amqp://{RBMPQ_USER}:{RBMPQ_PASS}@{RBMPQ_HOST}:{RBMPQ_PORT}"
celery_app = Celery('svc_ml', broker=BROKER_CONN_URI)
