# UpdateAPIView  
Функционал `WomenAPIList` не имеет __PUT__-запроса, для этого нужно уноследовать от других классов, такие как **UpdateAPIView** и **RetrieveUpdateDestroyAPIView**

```python
class WomenAPIUpdate(generics.UpdateApiView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer    
```

> в UpdateApiView можно использовать только PUT, PATH-запросы

queryset - **ленивый вопрос**, выполняется, как только нужны какие-то определенные данные

```python
urlpatterns = [
    ...
    path('api/v1/womenlist/<int:pk>/', WomenAPIUpdate.as_view()),
]
```

# RetrieveUpdateDestroyAPIView
**RetrieveUpdateDestroyAPIView** - выполняет функционал **CRUD**


```python
class RetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   GenericAPIView):
    ...
```

Запросы поддерживаемые **RetrieveUpdateDestroyAPIView**
* GET
* PUT
* PATH
* DELETE

#### views.py
```python
class WomenAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
```

#### urls.py
```python
urlpatterns = [
    ...
    path('api/v1/womendetail/<int:pk>/', WomenAPIDetailView.as_view()),
]
```

# Default [Render](https://www.django-rest-framework.org/api-guide/renderers/)

**settings.py**

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDER_CLASSES': [
        'rest_framework.renderers.JSONRender',
        'rest_framework.renderers.BrowsableAPIRender', # отвечает за отображение JSON-файла 
    ]
}
```

> Если мы поставим вторую строчку в комментарий, то отображение будет в виде **ссырых** данных JSON-формата