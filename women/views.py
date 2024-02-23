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
        serializer = WomenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'post': serializer.data} 
        
        return Response(data)
    
    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = Women.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = WomenSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {"post": serializer.data}
        
        return Response(data)