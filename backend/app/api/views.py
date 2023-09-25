from rest_framework import generics
from app.models import Data
from .serializer import DataSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response



class DataListView(generics.ListAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

class DataDetailView(generics.RetrieveAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer


class DataCreateView(generics.CreateAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer
    
    def post(self, request):
        """ call ranker function in engine logic and return top N results in json form"""
        if request.method == 'POST':
            print("plz")
            return JsonResponse({"response": 'got post request'}, safe=False)
    
    

class DataUpdateView(generics.UpdateAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer


 