# broker_url = "redis://localhost:6379/1"
# result_backend = "redis://localhost:6379/2"

# task_serializer = "json"
# result_serializer = "json"
# accept_content = ["json"]
# timezone = "UTC"
# enable_utc = True

# import celery
# from celery.schedules import crontab
# from tasks import update_inactive_users, daily_user_reminders, generate_monthly_report, export_book_requests_to_csv

# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(
#         crontab(minute="*/1"), update_inactive_users.s(), name="update inactive users"
#     )
#     sender.add_periodic_task(
#         crontab(hour=18, minute=0), daily_user_reminders.s(), name="daily reminder"
#     )
#     sender.add_periodic_task(
#         crontab(day_of_month=1, hour=0, minute=0), generate_monthly_report.s(), name="monthly report"
#     )

class Config:
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'kunalg2022@gmail.com'
    MAIL_PASSWORD = 'Kunal@2004'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

from celery import Celery
import celery
from flask import Flask
import os

def make_celery(app: Flask) -> Celery:
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery


from celery.schedules import crontab

celery.conf.beat_schedule = {
    'send-monthly-report': {
        'task': 'path.to.send_monthly_activity_report',
        'schedule': crontab(day_of_month=1, hour=0, minute=0),  # Run on the first day of every month
    },
}

