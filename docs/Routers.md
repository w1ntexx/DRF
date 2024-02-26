# Router

#### DefaultRouter
```py
router = routers.DefaultRouter()
router.register(r'women', WomenViewSet)

router.urls = ['api/v1/women/', 'api/v1/women/pk/', 'api/v1/']
```

Только в **DefaultRouter** есть url-маршрут `'api/v1/'`, если мы перейдем на него получим

```json
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "women": "http://127.0.0.1:8000/api/v1/women/"
}
```

В **SimpleRouter** urls-маршрты имеют свои имена, поэтому если мы попробуем зайти на `'api/v1/'`, получим **404**

Установка префикса
```py
router.register(r'women', WomenViewSet, basename='prefix')
```

>eсли у нас не используется quryset, то этот параметр обязателен

<br>

Если маршрутов не достаточно, то используем декоратор **@action**

# Декоратор @action

Например мы можем выводить список статей из модели Women, а список Категорий нет, чтобы это сделать 

```py
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Women, Category
from .serializers import WomenSerializer


class WomenViewSet(viewsets.ModelViewSet):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    
    @action(methods=['get'], detail=False) # detail - одна запись, False, потому что список
    def category(self, request):
        cats = Category.objects.all()
        return Response({'cats': [c.name for c in cats]})
```

Теперь чтобы нам перейти на метод, который мы добавили, нужно указать маршрут http://127.0.0.1:8000/api/v1/women/category/, **category** берется из названия метода получаем ответ

```json
{
    "cats": [
        "Актрисы",
        "Певицы"
    ]
}
```

# Важно

#### Ошибка при http://127.0.0.1:8000/api/v1/women/1/category/

Все потому, что это одна запись, а у нас `detail=False`, если укажем True, то ошибка пропадет, но появится другая, что мы не определили параметр pk, исправление 

```py
def category(self, request, pk=None):
```

Ошибка пропала, но записи выводятся не так, как хотелось

```py
    @action(methods=['get'], detail=True) # одну запись
    def category(self, request, pk=None): 
        cats = Category.objects.get(pk=pk) 
        return Response({'cats': cats.name}) # одна запись не итерируется 
```

А если мы хотим возвратить только первые 3 записи?

### get_queryset Viewset

```py
class WomenViewSet(viewsets.ModelViewSet):
    # queryset = Women.objects.all() 
    serializer_class = WomenSerializer
    
    def get_queryset(self):
        return Women.objects.all()[:3]
```
Когда мы убираем queryset, нужно в **urls.py** указать **basename**
```py
router.register(r'women', WomenViewSet, basename='women')
```

Но теперь при http://127.0.0.1:8000/api/v1/women/1/ ошибка 

```py
    def get_queryset(self):
        pk = self.kwargs.get("pk")
        
        if not pk:
            return Women.objects.all()[:3]
        #   метод quryset должен возвращать список, поэтому filter
        return Women.objects.filter(pk=pk) 
```
