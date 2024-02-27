# Token-based authentication

Токен это уникальный идентификатор (ключа) для идентификации пользователя. Причем токен не привязан ни к домену, ни к браузеру, главное указать его в заголовке запроса

В DRF есть два подхода 
1. [**Djoser**](https://djoser.readthedocs.io/en/latest/getting_started.html) - обычная аутентификация токенами
2. **Simple JWT** - JWT токены

Рассмотрим [1](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)


# Djoser

```py
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
]
```

```bash
$ python manage.py migrate
```

```py
urlpatterns = [
    ...
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')), # авторизация по токенам
]
```

```py
REST_FRAMEWORK = {
    ...    
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication', # разрешаю по токенам
        'rest_framework.authentication.BasicAuthentication',  
        'rest_framework.authentication.SessionAuthentication', # по умолчанию REST ставит его 
    ]
}
```
<br>
Переходим по http://127.0.0.1:8000/api/v1/auth/

Ответ

```json
{
    "users": "http://127.0.0.1:8000/api/v1/auth/users/"
}
```

Поддерживаемые действия в Djoser - [Base Endpoints](https://djoser.readthedocs.io/en/latest/base_endpoints.html)

Создадим пользователя

# User Create

В приложение POSTMAN по http://127.0.0.1:8000/api/v1/auth/users/ делаем **POST**-запрос

в ***Body*** выбираем form-data

| Key      | Value                  |
|----------|------------------------|
| username | seconduser             |
| password | afwafafwuser123        |
| email    | seconduser@mail.com    |

<br>

JSON-ответ

```json
{
    "email": "seconduser@mail.com",
    "username": "seconduser",
    "id": 2
}
```

Теперь наш User List выглядит так

```json
[
    {
        "email": "root@site.ru",
        "id": 1,
        "username": "root"
    },
    {
        "email": "seconduser@mail.com",
        "id": 2,
        "username": "seconduser"
    }
]
```

Сделаем тоже самое , без указание почты, но по auth-token, по адрессу http://127.0.0.1:8000/auth/token/login

Json-ответ

```json
{
    "auth_token": "7a4f4411f3e272bf7d9bc9f82f6681d559412004"
}
```

При GET-запросе на страницу, у которой permission **IsAuthenticated**

```json
{
    "detail": "Учетные данные не были предоставлены."
}
```

В Headers пропишем key **Authorization**.
Его ключ предпологает Токен, которые пишется в формате
<br>

Token 7a4f4411f3e272bf7d9bc9f82f6681d559412004

Теперь при **GET**-запросе на страницу получаем нужный ответ


# View auth

Чтобы конкретизировать авторизацию через токен в функции представления 

```py
from rest_framework.authentication import TokenAuthentication


class WomenApiUpdate(generics.RetrieveUpdateAPIView):
    ...
    authentication_classes = (TokenAuthentication,)
```

# Важно

Если мы указали авторизацию по токенам, то теперь по сессиям мы уже доступа не имеем.