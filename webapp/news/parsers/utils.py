import requests

from webapp.db import db
from webapp.news.models import News


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/79.0.3945.117 Safari/537.36'
    }
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


def save_news(title, url, published, author_published=None):
    news_exists = News.query.filter(News.url == url).count()
    print(news_exists)
    if not news_exists:
        news_news = News(title=title, url=url, published=published, author_published=author_published)
        db.session.add(news_news)
        db.session.commit()
