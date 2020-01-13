from flask import Flask, render_template
from flask_login import LoginManager, current_user, login_required

from webapp.user.views import blueprint as user_blueprint
from webapp.model import db, News
from webapp.user.models import User
from webapp.weather import weather_by_city


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    # указываем название нашей функции def login()
    login_manager.login_view = "user.login"
    # Подключаем блюпринт
    app.register_blueprint(user_blueprint)

    # получает по id нужного пользователя
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    def index():
        title = "Новости Python"
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news = News.query.order_by(News.published.desc()).all()
        return render_template('index.html', page_title=title, weather=weather, news_lists=news)

    @app.route('/admin')
    @login_required
    def admin_index():
        if current_user.is_admin:
            return 'Привет Админ'
        else:
            return 'Ты не админ'

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
