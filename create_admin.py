from getpass import getpass
import sys

from webapp import create_app
from webapp.model import db, User

app = create_app()

with app.app_context():
    username = input("Введите имя: ")

    if User.query.filter(User.username == username).count():
        print("Пользователь с таким именем уже существут")
        sys.exit(0)

    password1 = getpass("Введите пароль")
    password2 = getpass("Повторите пароль")

    if not password1 == password2:
        print("Пароли не одинаковые")
        sys.exit(0)
    # обращение к классу User, при создании пользователя
    new_user = User(username=username, role='admin')
    # добавление пароля, пароль хешируется в классе User.
    new_user.set_password(password1)
    # добавление в базу данныех
    db.session.add(new_user)
    # сохраение в базу данных
    db.session.commit()
    print("Создан пользователь с id= {}".format(new_user.id))
