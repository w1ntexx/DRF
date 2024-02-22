from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Women
from .serializers import WomenSerializer


class WomenApiView(APIView):
    def get(self, request): 
        model_women = Women.objects.all()
        data = {'posts': WomenSerializer(model_women, many=True).data}
        
        return Response(data)

    def post(self, request):
        serializator = WomenSerializer(data=request.data)
        serializator.is_valid(raise_exception=True)
        
        post_new = Women.objects.create(
            title=request.data['title'],
            content=request.data['content'],
            cat_id=request.data['cat_id']
        )
        data = {'post': WomenSerializer(post_new).data} 
        
        return Response(data)
        
    
    