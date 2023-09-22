from rest_framework import generics
from app.models import Data
from .serializer import DataSerializer

class DataListView(generics.ListAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

class DataDetailView(generics.RetrieveAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

class DataCreateView(generics.CreateAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

class DataUpdateView(generics.UpdateAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer