from webapp import create_app
from webapp.news.parsers import python_org_news
from webapp.news.parsers import habr

"""Ручной запуск сбора данных с сайтов,
 для атоматического можно использовать Celery"""

app = create_app()

with app.app_context():
    habr.get_news_snippets()
    python_org_news.get_news_content()
    habr.get_news_content()
