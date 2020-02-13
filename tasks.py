from celery import Celery
from celery.schedules import crontab

from webapp import create_app
from webapp.news.parsers.python_org_news import get_python_news
from webapp.news.parsers import habr

flask_app = create_app()
celery_app = Celery('tasks', broker='redis://localhost:6379/0')


@celery_app.task
def add_habr_snippets():
    with flask_app.app_context():
        habr.get_news_snippets()


@celery_app.task
def add_habr_content():
    with flask_app.app_context():
        habr.get_news_content()


@celery_app.task
def add_python_news():
    with flask_app.app_context():
        get_python_news()


# запуск по расписанию
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/5'), add_habr_snippets.s())
    sender.add_periodic_task(crontab(minute='*/6'), add_habr_content.s())
    sender.add_periodic_task(crontab(minute='*/7'), add_python_news.s())