from django.urls import path
from .views import *

app_name = 'extemp'
urlpatterns = [
    path('tournament/create/', TournamentCreate.as_view(), name='tournament_create'),
    path('tournament/<int:pk>/', TournamentDetail.as_view(), name='tournament_detail'),
    path('round/<int:pk>/update/', round_update, name='round_update'),
    path('round/<int:pk>/admin/bulk', bulk_add_topics, name='bulk_add_topics'),
    path('round/<int:pk>/admin/', manage_topics, name='manage_topics'),
    path('topic/<int:pk>/', TopicDetail.as_view(), name='topic_detail'),
    path('section/<int:pk>/draw/select/', select_topic, name='select_topic'),
    path('section/<int:pk>/draw/', draw_topics, name='draw_topics'),
    path('section/<int:pk>/secret/', SectionDetail.as_view(), name='section_detail_secret'),
    path('section/<int:pk>/', SectionDetailProduction.as_view(), name='section_detail'),
    path('', TournamentList.as_view(), name='tournament_list'),
]
