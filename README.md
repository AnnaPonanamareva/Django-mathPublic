# Азбука математики

Учебный проект: веб-приложение на Django - тренажёр по математике для практики вычислений и решения задач.
Доступные режимы:
- тесты
- задания
- карточки

## Запуск
1. Клонировать репозиторий или скачать архив с репозиторием
2. В командной строке/терминале:
- перейти в директорию Django-mathPublic-main
- Создать виртуальное окружение
python -m venv venv
- Активировать окружение
venv\Scripts\activate
- Установить зависимости
pip install -r requirements.txt.
Если файла requirements.txt нет:
pip install django
- Применить миграции:<br>
python manage.py migrate<br>
python manage.py seed_trainer<br>
python manage.py runserver;
- Запустить сервер
python manage.py runserver
- Открыть в браузере
http://127.0.0.1:8000

## Адреса
главная страница: `http://127.0.0.1:8000/`

