# Foodgram!
### Cоциальная сеть со вкусными рецептами!

Приложение позволяет публиковать свои рецепты,
смотреть рецепты других пользователей,
подписываться на других авторов, добавлять рецепты в избранное и в
список покупок, а также распечатывать список ингредиентов из понравившихся рецептов.

В рамках проекта использовались следующие технологии:
##### Python 3.7
##### Django 2.2.16
##### PostgreSQl 13.0
##### DRF 3.12.4
##### GitHub, GitActions
##### Nginx 1.21.3
##### Gunicorn 20.0.4
##### Docker 20.10.22

## Как развернуть проект на локальной машине:
Скопируйте проект из репозитория:
```bash 
git clone https://github.com/Ogyrecheg/foodgram-project-react.git
```
Перейти в дерикторию скачанного проекта.
Создать и активировать virtual enviroment:
```bash
py -3.7 -m venv -venv
source venv/scripts/activate
```
При активированном virtual env скачать необходимые зависимости проекта:
```bash
(venv) pip install -r api_yamdb/requirements.txt
```
##### Установить докер на вашу машину ([туториал](https://docs.docker.com/engine/install/))
### Настройка переменных окружения:

 В корневой папке проекта необходимо создать файл .env и указать в нем переменные окружения.

#### Пример:
```SECRET_KEY='g+s^((1bj2n33!8e8xrjag+@gdlf3@a2u*8%w1*0uc$*a%&d1!'``` - ключ от джанго проекта
 
```DB_ENGINE=django.db.backends.postgresql``` - указываем, что работаем с postgresql

```DB_NAME=postgres``` - имя базы данных

```POSTGRES_USER=postgres``` - логин для подключения к базе данных

```POSTGRES_PASSWORD=postgres``` - пароль для подключения к БД (установите свой)

```DB_HOST=db``` - название сервиса (контейнера)

```DB_PORT=5432``` - порт для подключения к БД


Запуск приложения из докер контейнера:
```bash
cd infra
docker-compose up -d --build
```

После сборки образов и создания - запуска контейнеров приложения необходимо произвести миграции в БД, создание суперюзера и сбор статики:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```
Если все прошло успешно, попробуйте залогиниться в админ-панель django проекта по адресу:
http://localhost/admin/
Для того, чтобы наполнить БД записями выполните команды:
```bash
python manage.py load_data
```
### Развернутый проект лежит по [адресу](http://51.250.103.76/admin/login/?next=/admin/)

### Автор проекта:
студент когорты №17 Шевченко А.И

![work_flow](https://github.com/Ogyrecheg/foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg)


