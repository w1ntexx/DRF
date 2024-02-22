# Serializer
> 
Роль **[Сериализатора](https://www.django-rest-framework.org/api-guide/serializers/)** выполнять конвертирование произвольных объектов языка Python в формат `JSON` в том числе модели фреймворка ***Django*** и наборы ***Queryset***, и наоборот из `JSON` в соответствующие объекты языка Python

Создадим файл __serializers.py__ в папке приложения


```python
import io

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers

class WomenModel:
    def __init__(self, title, content):
        self.title = title
        self.content = content

class WomenSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()

def encode():
    model = WomenModel('Angelina Jolie', 'Content: Angelina Jolie')
    model_sr = WomenSerializer(model)
    json = JSONRenderer().render(model_sr.data)
```

> Важно отметить, что локальный свойства в классе должны быть точно такие же, как в сериализаторе

<br>

Мы создаем функцию `encode`, которая прнимимает model, а именно объект класса с параметрами `title` и `content`, которые мы передаем в сериализатор `WomenSerializer`, который в свою очередь обрабатывает данные в словарь во вложенном классе `Meta`, у которого есть объект `data`. Её мы и рендерим с помощью `JSONRenderer`

<br/>


```python
model_sr = {'title': 'Angelina Jolie', 'content': 'Content: Angelina Jolie'}  # dict
json = b'{"title": "Angelina Jolie", "content": "Content: Angelina Jolie"}' # битовая строка json
```

<br />

__decode__
```python
import io
from rest_framework.parsers import JSONParser


def decode():
    # имитируем поступления запроса от клиента
    stream = io.BytesIO(json)
    
    data = JSONParser().parse()
    # чтобы декодировать, нам нужно явно указывать параметр data
    serializer = WomenSerializer(data=data)    
    serializer.is_valid()
    result = serialize.validated_data
```

Результат
```python
result = OrderDict([('title', 'Angelina Jolie'), ('content', 'Content': 'Angelina Jolie')])
```

Сериализатор для `WomenApiView`

```python
# ---- serializers.py ----- 
from rest_framework import serializers

class WomenSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()

    # read_only, потому что они обязательные, но заполняются автоматически
    time_create = serializers.DateTimeField(read_only)
    time_update = serializers.DateTimeField(read_only)
    is_published = serializers.BooleanField(default=True)

    # в модели cat, но тут cat_id потому что в json именно оно будет фигурировать
    cat_id = serializers.IntegerField() 
```


```python
# ---- views.py -----
class WomenApiView(APIView):
    def get(self, request): 
        # в классе Women есть свойства, которые и берет на себя сериализатор
        model_women = Women.objects.all()
        data = {'posts': WomenSerializer(model_women, many=True).data}
        
        return Response(data) 

    def post(self, request):
        # при неправильном POST-запросе формирует исключение 
        serializator = WomenSerializer(data=request.data)
        serializator.is_valid(raise_exception=True)

        post_new = Women.objects.create(
            title=request.data['title'],
            content=request.data['content'],
            cat_id=request.data['cat_id']
        )
        # здесь объект, поэтому many=False
        data = {'post': WomenSerializer(post_new).data} 
        
        return Response(data)
           
```
Если неправильно заполнить POST-запрос, например не указать поле `title`, то json файл будет выглядеть так
```json
{
    "title": [
        "Обязательное поле."
    ]
}
```


