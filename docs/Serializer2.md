# Serializer 2

#### Метод `create`

```python
from rest_framework import serializers
from .models import Women


class WomenSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    time_create = serializers.DateTimeField(read_only=True)
    time_update = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(default=True)
    cat_id = serializers.IntegerField()
    
    def create(self, validated_data):
        return Women.objects.create(**validated_data) 
```
`validated_data` = формируется при вызове метода *is_valid*

```python
class WomenApiView(APIView):
    def get(self, request): 
        model_women = Women.objects.all()
        data = {'posts': WomenSerializer(model_women, many=True).data}
        
        return Response(data)

    def post(self, request):
        serializator = WomenSerializer(data=request.data)
        serializator.is_valid(raise_exception=True) # формирует validated_data
        serializator.save() # сохраняет записи в БД, вызывает create

        data = {'post': serializator.data} 
        
        return Response(data)
```
### Метод update
```py
def update(self, instance, validated_data): 
    instance.title = validated_data.get("title", instance.title)
    instance.save()

    return instance
```
Здесь `instance` -> объект модели. Через **ORM** мы меняем значение на то, которое пришло в POST-запросе, а при исключении меняется на второй параметр
<br>

Во `views.py` мы добавим request.method PUT, который предназначен для обновления данных
```py
def put(self, request, *args, **kwargs):
    pass
```
Здесь kwargs будет pk в `urls.py`
```python
urlpatterns = [
    ...
    path('api/v1/womenlist/<int:pk>/', WomenApiView.as_view()),
]
```

Поэтому мы проверим pk в PUT-методе
```python
    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = Women.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = WomenSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {"post": serializer.data}
        
        return Response(data)
```
# Важно
Метод **save** вызывает метод **update** автоматически, когда указан аргумент `instance=instance`, если бы он не был указан, был бы вызван метод **create**
