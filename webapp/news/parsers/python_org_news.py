from datetime import datetime

from bs4 import BeautifulSoup

from webapp.news.parsers.utils import get_html, save_news
from webapp.db import db
from webapp.news.models import News


# Парсер страницы https://www.python.org
def get_python_news():
    html = get_html("https://www.python.org/blogs/")
    if html:
        soup = BeautifulSoup(html, "html.parser")
        all_news = soup.find('ul', class_='list-recent-posts')
        all_news = all_news.findAll('li')
        for news in all_news:
            title = news.find('a').text
            url = news.find('a')['href']
            published = news.find('time')['datetime']
            try:
                published = datetime.strptime(published, '%Y-%m-%d')
            except ValueError:
                published = datetime.now()
            save_news(title, url, published)


def get_news_content():
    news_without_text = News.query.filter(News.text.is_(None))
    for news in news_without_text:
        html = get_html(news.url)
        try:
            if html:
                soup = BeautifulSoup(html, "html.parser")
                # Для получения именно html используем .decode_contents() а не .text
                news_text = soup.find('div', class_='entry-content').decode_contents()
                if news_text:
                    news.text = news_text
                    db.session.add(news)
                    db.session.commit()
        except AttributeError:
            print("Данных <div class='entry-content' нет на странице")


if __name__ == "__main__":
    get_news_content()
