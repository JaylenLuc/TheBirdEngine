from django.urls import path, include

from .views import DataDetailView, DataListView, DataCreateView, DataUpdateView

urlpatterns = [

    path('',DataListView.as_view()),
    path('<pk>', DataDetailView.as_view()),
    path('<pk>/update/', DataUpdateView.as_view()),
    path('create/', DataCreateView.as_view()),
    

]