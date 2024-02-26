# [Permissions](https://www.django-rest-framework.org/api-guide/permissions/) (Ограничения доступа)

Маршрутизация ресурсов позволяет быстро объявить все общие маршруты для данного ресурсного контроллера. Вместо объявления отдельных маршрутов для вашего индекса... изобретательный маршрут объявляет их в одной строке кода.

Для начала внесем изменение в таблицу **Women**

```py
from django.contrib.auth.models import User

class Women(models.Model):
    ...
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        )
```

```bash
$ python manage.py makemigrations
$ Select an option: 1
>>> 1
$ python manage.py migrate
```

> Теперь все пользователи имеют **user_id = 1**

#### views.py

```py
class WomenApiList(generics.ListAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    

class WomenApiUpdate(generics.RetrieveUpdateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer


class WomenApiDestroy(generics.RetrieveDestroyAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
```

#### urls.py

```py
urlpatterns = [
    ...
    path('api/v1/women/', WomenApiList.as_view()),
    path('api/v1/women/<int:pk>/', WomenApiUpdate.as_view()),
    path('api/v1/womendelete/<int:pk>/', WomenApiDestroy.as_view()),
]
```

# Ограничения доступа
 
* AllowAny - полный доступ; 
* IsAuthenticated - только для авторизованных пользователей;
* IsAdminUser - только для администраторов;
* IsAuthenticatedOrReadOnly - только для авторизованных или всем, для чтения.

<br>

```py
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class WomenApiList(generics.ListCreateAPIView):
    ...
    permission_classes = (IsAuthenticatedOrReadOnly, )
```
<br>

Чтобы **скрыть** текщуего пользователя, в сериализаторе 

```py
class WomenSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Women
        fields = '__all__'
    
```

# CustomPermissions

Чтобы создать свои права доступа, нужен класс **BasePermission**

```py
class BasePermission(metaclass=BasePermissionMetaclass):
    def has_permission(self, request, view):
        '''Права доступа на уровне всего запроса от клиента'''
        return True

    def has_object_permission(self, request, view, obj):
        '''Права доступа на уровне отдельного объекта'''
        return True
```

<br>

в women/ создадим файл **permissions.py**

```py
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):   
        if request.method in permissions.SAFE_METHODS:  # если запрос безопасный (для чтения)
            return True                                 # предоставляем доступ
        
        # скопировал строчку с класса IsAdminUser   
        return bool(request.user and request.user.is_staff)
```


#### views.py

```py
from drfsite.women.permissions import IsAdminOrReadOnly

class WomenApiDestroy(generics.RetrieveDestroyAPIView):
    ...
    permission_classes = (IsAdminOrReadOnly, )
```

<br>

#### Добавим разрешение на изменение записи только пользователю

```py
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj): # obj , потому что работаем с записями
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
```

<br>

# Глобальные ограничение доступа

#### settings.py


```py
REST_FRAMEWORK = {
    ...
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated', # доступ к данным авторизованным
    ]
}
```
Но это поведение по умолчанию, и если будет настройка на страницу с правами доступа без регистрации, ты мы сможем зайти по этому url-адрессу