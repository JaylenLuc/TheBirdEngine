from django.http import JsonResponse
from rest_framework import generics
from app.models import Data
from .serializer import DataSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.append( r'C:\Users\Jaylen\Desktop\TheBirdEngine\engine_logic')
from tokenizer import Tokenizer


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
            print(request.data)
            ranked_res_ascending = Tokenizer.process_query(request.data)
            print("RESULTANTS:: ",ranked_res_ascending)
            return JsonResponse(ranked_res_ascending, safe=False)
    

class DataUpdateView(generics.UpdateAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer


 