# ModelSerializer
В обычном сериализаторе при создании/обновлении записи в модели, мы создавали методы create, update, но можно создать класс, наследуюемый от `serializers.ModelSerializer`

```python
from rest_framework import serializers
from .models import Women


class WomenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Women
        fields = ['title', 'content', 'cat'] 
```

> Мы указываем поля, поэтому не cat_id, а cat

# ListCreateAPIView 
Несколько упрощенней для `View`
* CreateAPIView - **создание** данных по __POST__-запросы;
* ListAPIView - чтение **списка** данных по __GET__-запросу;
* RetrieveAPIView - чтение **конкретных** данных (записи) по __GET__-запросу;
* DestroyAPIView - **удаление** данных (записи) по __GET__-запросу;
* UpdateAPIView - **изменение** записи по по __PUT__ или  __PATH__-запросу;
* ListCreateAPIView - для **чтения** (по __GET__-запросу) и создания списка данных (по __POST__-запросу);
* RetrieveUpdateAPIView - чтение и изменение **отдельной** записи (__GET__ И __POST__-запросы);
* RetrieveDestroyAPIView - чтение (__GET__-запрос) и удаление (__DELETE__-запрос) **отдельной** записи;
* RetrieveUpdateDestroyAPIView - чтение, изменение, и добавление *отдельной* записи

#### Views.py
```python
from rest_framework import generics 


class WomenAPIList(generics.ListCreateAPIView):
    '''Использует GET и POST-запросы'''
    queryset = Women.objects.all() 
    serializer_class = WomenSerializer

# ---- serializers.py ----- 

    urlpatterns = [
    ...
    path('api/v1/womenlist/', WomenAPIList.as_view()),
    path('api/v1/womenlist/<int:pk>/', WomenAPIList.as_view()),
]
```

Под капотом `ListCreateAPIView` 
```py
class ListCreateAPIView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        GenericAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```
Два миксина, которые описывают базовый функционал, один общий класс __GenericAPIView__ и GET, POST-запросы