from celery import Celery


def get_celery_instance():
    app = Celery(
        'fastapi_celery',
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/0',
    )
    app.conf.update(
        task_serializer='json',
        result_backend='redis://localhost:6379/',
    )
    # app.autodiscover_tasks('api.workers.upload')
    return app
