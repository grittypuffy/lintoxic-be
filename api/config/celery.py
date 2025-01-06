from celery import Celery
from api.helpers.singleton import singleton


def get_celery_instance():
    app = Celery(
        'fastapi_celery',
        broker='redis://localhost:6379/',  # Redis as the broker
        backend='redis://localhost:6379/',  # Redis as the backend for storing results
    )
    app.conf.update(
        task_serializer='json',  # Serialize task data
        result_backend='redis://localhost:6379/',  # Store results in Redis
    )
    app.autodiscover_tasks('tasks')
    return app
