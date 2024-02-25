# [Viewsets](https://www.django-rest-framework.org/api-guide/viewsets/)
Во **views.py** повторяется код 
```py
class WomenAPIList(generics.ListCreateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer


class WomenAPIUpdate(generics.UpdateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer        
  
    
class WomenAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
```

Для решения этой проблемы были придуманы **viewsets**, и так как у нас все три класса связаны с моделью мы будем использовать **[ModelViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset)**

```python
# ---- views.py -----
from rest_framework import viewsets


class WomenViewSet(viewsets.ModelViewSet):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer

# ---- urls.py -----
    urlpatterns = [
    ...
    path('api/v1/womenlist/', WomenViewSet.as_view({'get': 'list'})),
    path('api/v1/womenlist/<int:pk>/', WomenViewSet.as_view({'put': 'update'})),
]
```

В словаре мы пишем, какой именно запрос будет обрабатываться и его обработка в виде значения. Все представления указаны в [Viewset actions](https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions)


Но это не лучший способ использования Viewsets, поэтому на уровне фреймворка были созданы [Routers](https://www.django-rest-framework.org/api-guide/routers/)

# Routers

Воспользуемся [Simple Router](https://www.django-rest-framework.org/api-guide/routers/#simplerouter)

```python
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'women', WomenViewSet) # app, Viewset

urlpatterns = [
    ...
    path('api/v1/', include(router.urls)), # http://127.0.0.1:8000/api/v1/women/
]

```

При регистрации роутера формируется urls, набор маршрутов из WomenViewSet
<br>
И теперь методы, которые доступны `Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS`

Если мы хотим не менять записи, а только читать есть другой Viewset 

```python
class WomenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
```