# Описание
Cоциальная сеть со вкусными рецептами!
Приложение позволяет публиковать свои рецепты,
смотреть рецепты других пользователей,
подписываться на других авторов, добавлять рецепты в избранное и в
список покупок, а также распечатывать список ингредиентов из понравившихся рецептов.

## Запуск проекта:
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

**Технологии:**
- Python
- Django
- PostgreSQl
- DRF
- GitHub, GitActions
- Nginx
- Gunicorn
- Docker

### Автор проекта:
студент когорты №17 [Шевченко Александр](https://github.com/Ogyrecheg)

![work_flow](https://github.com/Ogyrecheg/foodgram-project-react/actions/workflows/foodgram_project_react_workflow.yml/badge.svg)
