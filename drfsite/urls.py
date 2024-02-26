from django.contrib import admin
from django.urls import path, include 

from women.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/women/', WomenApiList.as_view()),
    path('api/v1/women/<int:pk>/', WomenApiUpdate.as_view()),
    path('api/v1/womendelete/<int:pk>/', WomenApiDestroy.as_view()),
]
