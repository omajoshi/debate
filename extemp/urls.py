from django.urls import path
from .views import *

app_name = 'extemp'
urlpatterns = [
    path('create/', TournamentCreate.as_view(), name='tournament_create'),
    path('<int:pk>/', TournamentDetail.as_view(), name='tournament_detail'),
    path('', TournamentList.as_view(), name='tournament_list'),
]
