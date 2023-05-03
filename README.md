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

##### Установить докер на вашу машину ([туториал](https://docs.docker.com/engine/install/))

Запуск приложения из докер контейнера:
```bash
cd infra
docker-compose up -d --build
```

После сборки образов и создания - запуска контейнеров приложения необходимо произвести миграции в БД, создание суперюзера и сбор статики:
```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input
```
Если все прошло успешно, попробуйте залогиниться в админ-панель django проекта по адресу:
http://localhost/admin/
Для того, чтобы наполнить БД записями выполните команды:
```bash
docker-compose exec backend python manage.py load_data
```
### Развернутый проект лежит по [адресу](http://51.250.103.76/)
### Данные для входа в админ-панель:
admin@mail.com , 12345

### Автор проекта:
студент когорты №17 Шевченко А.И

![work_flow](https://github.com/Ogyrecheg/foodgram-project-react/actions/workflows/foodgram_project_react_workflow.yml/badge.svg)