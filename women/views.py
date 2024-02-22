from rest_framework import generics
from django.shortcuts import render
from .models import Women
from .srializers import WomenSerializer

# Create your views here.
class WomenApiView(generics.ListAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    