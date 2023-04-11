# yamdb_final
# api_yamdb


![my workflow](https://github.com/rem-li/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)


## Ссылки на проект:

[Redoc](http://84.201.132.70/redoc/)

[Админка](http://84.201.132.70/admin/)


## Ссылки на проект:

[Redoc](http://84.201.132.70/redoc/)

[Админка](http://84.201.132.70/admin/)

## Описание проекта:

**api_yamdb** - проект для сбора отзывов на различные художественные произведения, разделенные на разные жанры и категории. Пользователи могут просматривать списки жанров, категорий и самих произведений, оставлять собственные отзывы и оценки к произведениям и комментировать отзывы других пользователей.

## Технологии

* Python 3.7
* Django 3.2
* Django Rest Framework 3.12.4
* Simple JWT
* SQLite3

## ENV-файл

```
DB_ENGINE=
DB_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=
DB_PORT=
```

## Как запустить проект в контейнере:

Запустить docker-compose:

```
docker-compose up -d
```

Выполнить миграции:

```
docker-compose exec web python manage.py migrate
```

Создать суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

Собрать статику:

```
docker-compose exec web python manage.py collectstatic --no-input
```

## Заполнить базу данными

```
docker-compose exec web python manage.py loaddata fixtures.json
```

## Примеры некоторых запросов API

Регистрация пользователя:
`POST /api/v1/auth/signup/`

Получение данных своей учетной записи:
`GET /api/v1/users/me/`

Добавление новой категории:
`POST /api/v1/categories/`

Удаление жанра:
`DELETE /api/v1/genres/{slug}`

Частичное обновление информации о произведении:
`PATCH /api/v1/titles/{titles_id}`

Получение списка всех отзывов:
`GET /api/v1/titles/{title_id}/reviews/`

Добавление комментария к отзыву:
`POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/`

## Авторы

[Алексей Геккин](https://github.com/AlexeyGekkin)

[Иван Германов](https://github.com/ivgermanov)

[Елизавета Веремьёва](https://github.com/rem-li)
