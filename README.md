- [Web_Flask - новости с хабрахабр](#Web_Flask_новости_с_хабрахабр)
- [Установка на локальной машине](#Установка_на_локальной_машине)
- [Настройка](#Настройка)
- [Запуск](#Запуск)

## Web_Flask - новости с хабрахабр
Данный проект представляест собой приложение, собирающее новости по Python с https://habr.com/. 
Результаты складываются в базу данных sqlite. Данные выводятся с помощью Flask
приложения. 

Работу приложения можно посмотреть по ссылке: http://ovz1.smit-bb.pr46m.vps.myjino.ru/

## Установка на локальной машине
Создайте виртуальное окружение и активируйте его. Потом в виртуальном окружении
выполните:
```

pip install -r requirements.txt

```

## Настройка

Создайте файл config.py в директории webapp и добавьте туда следующие настройки:
```
from datetime import timedelta
import os

WEATHER_DEFAULT_CITY = 'Yekaterinburg,Russia' - Замените Yekaterinburg на свой город или оставьте так.

WEATHER_API_KEY = 'API ключ, который вы получили у worldweatheronline.com после регистрации'

WEATHER_URL = 'http://api.worldweatheronline.com/premium/v1/weather.ashx'

# Показывает обсалютный путь к файлу кофиг.
basedir = os.path.abspath(os.path.dirname(__file__))

# Указываем какой движок баз данных хотим использовать, в нашем случае это sqlite .
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')

# Ключ для шифрования, нужен для зашиты от подмены формы.
SECRET_KEY = 'Сгенерируйте свой ключ шифрования'

# На какое количество дней сайт запомнит пользователя.
REMEMBER_COOKIE_DURATION = timedelta(days=5)

# Если установлен в True, то Flask-SQLAlchemy будет отслеживать изменения объектов и посылать сигналы. По умолчанию
установлен в None, что включает отслеживание но выводит предупреждение.
SQLALCHEMY_TRACK_MODIFICATIONS = False

```

## Запуск

В активированном виртуальном окружении выполните для windows:
```
run
```
Запустится файл run.bat

Для Linux создайте файл run.sh со следующей командой:
```
export FLASK_APP=webapp && export FLASK_ENV=development && flask run
```
В активированном виртуальном окружении выполните:
```
./run.sh
```