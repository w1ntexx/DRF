from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Women, Category
from .serializers import WomenSerializer


class WomenViewSet(viewsets.ModelViewSet):
    # queryset = Women.objects.all()
    serializer_class = WomenSerializer
    
    def get_queryset(self):
        pk = self.kwargs.get("pk")
        
        if not pk:
            return Women.objects.all()[:3]
        #   метод quryset должен возвращать список, поэтому filter
        return Women.objects.filter(pk=pk) 
    
    @action(methods=['get'], detail=True) 
    def category(self, request, pk=None):
        cats = Category.objects.get(pk=pk)
        return Response({'cats': cats.name})

