import requests
from bs4 import BeautifulSoup


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


def get_python_news():
    try:
        html = get_html("https://www.python.org/blogs/")
        if html:
            soup = BeautifulSoup(html, "html.parser")
            all_news = soup.find('ul', class_='list-recent-posts')
            all_news = all_news.findAll('li')
            result_news = []
            for news in all_news:
                title = news.find('a').text  # получили текст из тега <a>
                url = news.find('a')['href']  # получаем ссылку, к атрибутам обращаемся как к элементам словаря
                published = news.find('time').text  # тут получаем дату публикации нашей новости
                result_news.append({
                    "title": title,
                    "url": url,
                    "published": published,
                })
            return result_news
        return False
    except AttributeError:
        print("Объект не найден")
    return False
    # all_news = soup.findAll('ul')# возвращает все ul теги
    # all_news = soup.find('ul')# возвращает первые ul теги




# код для скачивания html страницы
# if html:
#     with open("python.org.html", "w", encoding="utf-8") as f:
#         f.write(html)
