# from celery import Celery
# from flask import Flask
# from config import Config  # Ensure you have your Flask app's config here

# def make_celery(app: Flask) -> Celery:
#     celery = Celery(
#         app.import_name,
#         backend=Config.CELERY_RESULT_BACKEND,
#         broker=Config.CELERY_BROKER_URL
#     )
#     celery.conf.update(app.config)
#     return celery

# app = Flask(__name__)
# app.config.from_object(Config)
# celery = make_celery(app)

# from celery import Celery, Task
# from flask import Flask
# from config import Config

# def make_celery(app: Flask) -> Celery:
#     celery = Celery(
#         app.import_name,
#         backend=Config.CELERY_RESULT_BACKEND,
#         broker=Config.CELERY_BROKER_URL
#     )
#     celery.conf.update(app.config)
#     return celery

# app = Flask(__name__)
# app.config.from_object(Config)
# celery = make_celery(app)

from celery import Celery, Task
from flask import Flask

def make_celery(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object('celeryconfig')
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    Celery.conf.update(app.config)
    return celery_app
