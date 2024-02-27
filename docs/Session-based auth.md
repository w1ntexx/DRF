# Авторизация и аутентификация

[Документация](https://www.django-rest-framework.org/api-guide/authentication/)

* Session-based authentication - аутентификация на основе сессий и cookies
* Token-based authentication - аутентификация на основе токенов
* JSON Web Token (JWT) authentication - аутентификация на основе JWT-токенов
* Django REST framework OAuth - авторизация через социальные сети

#### Session-based authentication 
При входе в аккаунт в базу данных заносится уникальный session_id, который хранится в cookies, после чего, чтобы зайти на страницу с правами доступа, которые есть на этом аккаунте, сервер ищет их в БД и сверяет session_id, если cookie обновился, пользователя нужно войти в аккаунт. Минус этого метода - жесткая привязка к устройству (браузеру)

#### urls.py

```py
urlpatterns = [
    path('api/v1/drf-auth', include('rest_framework.urls')),
    ...
]
```

Два url-маршрута
1. login api/v1/drf-auth/login
2. logout api/v1/drf-auth/logout