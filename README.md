# data_pipeline

Structure of the project
```
├── README.md
├── backend-rabbitmq
│   ├── data
│   ├── etc
│   └── logs
├── data
│   ├── images
│   ├── output
|   |        └── <task id>
|   |                └── imageXXX.jpg
|   |                └── metadata.csv
│   └── styles.csv
|── db (...)
├── docker
│   ├── api_Dockerfile
│   ├── celery_Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── rbmq
│   ├── data
│   ├── etc
│   └── logs
└── src
    ├── TestAPIquery.ipynb
    ├── __init__.py
    ├── __pycache__
    ├── api
    ├── celery_worker
    ├── config.ini
    ├── db_scripts
    └── utils
```

This project implements an asynchronous API (FastAPI) with the help of Celery to submit jobs in the background. Like that you can process many requests in parallel. For the case of large requests RabbitMQ handles themm well and for ie 1M of images we should be able to load the metadata in in memory (from csv) and celery will handle the process and storage of images one by one.

Currently RabbitMQ is used to submit jobs and take the results. For better scaling we could consider the use of Redis as well for backend.

# How to use
Being in the home directory of the project just run
```
docker-compose up
```

The following services will launch:
* API (FastAPI): 
  * listens to port 8080 which is exposed
  * mounts the src folder
* Worker (Celery):
  * mounts the data & the src folder
* Broker (RabbitMQ)
  * listens to port 5672 which is exposed
  * logs and data are mounted locally in folder rbmq
* DB (Postgres)
  * listens to port 5432 which is exposed
* PgAdmin
  * listens to port 5342 which is exposed
  
**NOTE**: all services use the `.env` file to set environment variables which are used also in the `config.ini` which is used to configure the pipeline.

In `.env` we store service credentials eg `DB_USER`, `DB_PORT` which are also used though this file between the containers

In `config.ini` you can configure at the moment where your data is located and where the output folder is.

For the sake of simplicity we store the results locally and in the folder indicated in `config.ini` in folders using the name of task_id. 

In Jupyter Notebook (`src/TestAPIquery.ipynb`) we test the queries and how we can use the response to access the data.

To start playing around the API you can go to `http:<IP>:8080/api/v1/svc_ml/docs` where you can see all the endpoints, their arguments and their methods to be called.

TODOs:
- apply model predict
- take tests from jupyter and create some integration tests
- unit tests for API
- gather metrics
- imrpove logging outside of worker as well
- make it as a package with setuptools
