# live_site

Live_Site - это сервис для управления недвижимостью. Он предоставляет API для добавления, редактирования и получения информации о недвижимости, а также для обмена сообщениями между пользователями.

# Требования

Для запуска и разработки проекта требуется следующее:

1. Python 3.7 или выше
2. Django 3.2 или выше
3. SQLite 3

# Установка

1. Клонируйте репозиторий:
git clone https://github.com/Xteonena/Live_Site.git
2.Перейдите в директорию проекта:
cd Live_Site
3.Создайте и активируйте виртуальное окружение:
python -m venv venv
source venv/bin/activate
4. Установите зависимости:
pip install -r requirements.txt
5. Примените миграции базы данных:
python manage.py migrate

# Запуск
Для запуска сервера разработки выполните следующую команду:
python manage.py runserver

Сервер будет доступен по адресу http://localhost:8000/.

# API

API предоставляет следующие конечные точки:
/api/properties/ - список всех недвижимостей
/api/properties/{property_id}/ - информация о конкретной недвижимости
/api/properties/create/ - создание новой недвижимости
/api/properties/{property_id}/update/ - обновление информации о недвижимости
/api/properties/{property_id}/delete/ - удаление недвижимости
/api/messages/ - список всех сообщений
/api/messages/create/ - создание нового сообщения
