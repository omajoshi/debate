from django.urls import path
from .views import *

app_name = 'extemp'
urlpatterns = [
    path('tournament/create/', TournamentCreate.as_view(), name='tournament_create'),
    path('tournament/<int:pk>/', TournamentDetail.as_view(), name='tournament_detail'),
    path('round/<int:pk>/sections', manage_sections, name='manage_sections'),
    path('round/<int:pk>/topics', manage_topics, name='manage_topics'),
    # path('round/<int:pk>/', SectionDetail.as_view(), name='section_detail2'),
    path('section/<int:pk>/', SectionDetail.as_view(), name='section_detail'),
    path('', TournamentList.as_view(), name='tournament_list'),
]
