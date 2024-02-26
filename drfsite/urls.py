from django.contrib import admin
from django.urls import include, path

from women.views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'women', WomenViewSet, basename='women')
print(router.urls)  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)), # http://127.0.0.1:8000/api/v1/women/
]
