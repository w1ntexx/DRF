# APIView 

`APIView` - Базовый класс для создания API-представлений

### Создание представления 
```python
from rest_framework.response import Response
from rest_framework.views import APIView


class WomenApiView(APIView):
    def get(self, request): # автоматически обрабатывает GET-запрос
        data = {'title': 'Angilina Jolie'} 
        return Response(data) # ответ в виде json

    def post(self, request):
        data = {'title': 'Jennifer Shrader Lawrence'}
        return Response(data)
```


### Маршрутизация
```python
urlpatterns = [
    ...
    path('api/v1/womenlist/', WomenApiView.as_view())
]
```
<br />

### Создадим API-запрос посложнее
```python
    def get(self, request): 
        bd_values = Women.objects.all.values() 
        data = {'posts': list(bd_values)}

        return Response(data)
```

### Ответ
<!-- <div style="max-height: 200px; overflow-y: auto;"> -->

```json
{
    "posts": [
        {
            "id": 1,
            "title": "Анджелина Джоли",
            "content": "",
            "time_create": "2024-02-21T03:55:26.463067Z",
            "time_update": "2024-02-21T03:55:26.463067Z",
            "is_published": true,
            "cat_id": 1
        },
            ...
}
```

### POST-запрос
```python
    ...
    def post(self, request)
        post_new = Women.objects.create(
            title=request.data['title'],
            content=request.data['content'],
            cat_id=request.data['cat_id']
        )
        # возвращает словарь данными, которые были добавлены
        data = {'post': model_to_dict(post_new)}
         
        return Response(data)
```

### Отправляем POST-запрос

```json
{
    "title": "Timofey",
    "content": "Timofey Makarov",
    "cat_id": 2
}
```

### Ответ
```json
{
    "post": {
        "id": 9,
        "title": "Timofey",
        "content": "Timofey Makarov",
        "is_published": true,
        "cat": 2
    }
}
```


## Важно
#### Для добавление записей в модели лучше использовать другой класс `ListApiView`, так как мы не обрабатываем ошибки, это лишь учебный пример о классе `APIView`