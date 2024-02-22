from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Women
from .srializers import WomenSerializer


class WomenApiView(APIView):
    def get(self, request): 
        bd_values = Women.objects.all().values()
        data = {'posts': list(bd_values)}
        
        return Response(data)

    def post(self, request):
        post_new = Women.objects.create(
            title=request.data['title'],
            content=request.data['content'],
            cat_id=request.data['cat_id']
        )
        data = {'post': model_to_dict(post_new)} 
        
        return Response(data)
        

    
# class WomenApiView(generics.ListAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer

    
    