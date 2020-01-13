from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from webapp.db import db


# класс пользователя который использует множественное наследоване
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # проверка пользователя на права админа
    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return '<User name={}; id={}>'.format(self.username, self.id)