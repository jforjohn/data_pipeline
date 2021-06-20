from celery import Celery

BROKER_CONN_URI = f"amqp://guest:guest@api_ml_rabbitmq:5672"
celery_app = Celery('hello', broker=BROKER_CONN_URI)
