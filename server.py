from flask import Flask, render_template
from news_parser import get_python_news
from weather import weather_by_city


app = Flask(__name__)


@app.route('/')
def index():
    title = "Новости Python"
    weather = weather_by_city('Yekaterinburg,Russia')
    news = get_python_news()
    return render_template('index.html', page_title=title, weather=weather, news_lists=news)


if __name__ == "__main__":
    app.run(debug=True)
