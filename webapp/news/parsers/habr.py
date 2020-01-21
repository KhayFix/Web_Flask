from datetime import datetime, timedelta
import locale
import platform

from bs4 import BeautifulSoup

from webapp.news.parsers.utils import get_html, save_news

# выставляем русскоязычную локаль для распознования даты
if platform.system() == 'Windows':
    locale.setlocale(locale.LC_ALL, "russian")
else:
    locale.setlocale(locale.LC_TIME, "ru_RU")


def parse_habr_date(date_str: str):
    """Функция обрабатывает строку даты публикации статьи
     и приводит к формату %Y-%m-%d %H:%M"""

    name_of_months = {'января': 'январь', 'февраля': 'февраль', 'марта': 'март', 'апреля': 'апрель',
                      'мая': 'май', 'июня': 'июнь', 'июля': 'июль', 'августа': 'август', 'сентября': 'сентябрь',
                      'октября': 'октябрь', 'ноября': 'ноябрь', 'декабря': 'декабрь'}

    if 'сегодня' in date_str:
        today = datetime.now()
        date_str = date_str.replace('сегодня', today.strftime('%d %B %Y'))
    elif 'вчера' in date_str:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = date_str.replace('вчера', yesterday.strftime('%d %B %Y'))
    else:
        # Т.к. на Хабре дата в в формате строки "19 января 2020 в 19:17" datetime не работет с окончаниями месяцев,
        # нужно января -:- привести к виду -:- январь.
        date_str = date_str.lower().split()
        if date_str[1] in name_of_months:
            date_str[1] = name_of_months.get(date_str[1])
            date_str = ' '.join(date_str)
    try:
        return datetime.strptime(date_str, '%d %B %Y в %H:%M')
    except ValueError:
        return datetime.now()


# Парсер страницы https://habr.com/
def get_habr_snippets():
    html = get_html("https://habr.com/ru/search/?target_type=posts&q=python&order_by=date")
    if html:
        soup = BeautifulSoup(html, "html.parser")
        all_news = soup.find('ul', class_='content-list_posts')
        all_news = all_news.findAll('li', class_='content-list__item_post')
        for news in all_news:
            title = news.find('a', class_='post__title_link').text
            url = news.find('a', class_='post__title_link')['href']
            published = news.find('span', class_='post__time').text
            published = parse_habr_date(published)
            author_published = news.find('a', class_='post__user-info')['href']

            save_news(title, url, published)


if __name__ == "__main__":
    get_habr_snippets()
