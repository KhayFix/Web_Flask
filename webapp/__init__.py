from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from webapp.db import db
from webapp.admin.views import blueprint as admin_blueprint
from webapp.news.views import blueprint as news_blueprint
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    # включаем работу с миграциями
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    # указываем название нашей функции def login()
    login_manager.login_view = "user.login"

    # Подключаем блюпринт пользователя и админа
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(user_blueprint)
    # Подключаем блюпринт с новостями
    app.register_blueprint(news_blueprint)

    # получает по id нужного пользователя
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
