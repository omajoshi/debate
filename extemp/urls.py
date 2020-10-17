from django.conf.urls.static import static
from django.urls import path

from .views import *


app_name = 'extemp'
urlpatterns = [
    path('tournament/create/', TournamentCreate.as_view(), name='tournament_create'),
    # path('tournament/<int:pk>/roundgroups/', manage_roundgroups, name='manage_roundgroups'),
    path('tournament/<int:pk>/details/', set_tournament_details, name='set_tournament_details'),
    path('tournament/<int:pk>/open/', open_current_rounds, name='open_current_rounds'),
    path('tournament/<int:pk>/close/', close_current_rounds, name='close_current_rounds'),
    path('tournament/<int:pk>/urls/', get_current_urls, name='get_current_urls'),
    path('tournament/<int:pk>/', TournamentDetail.as_view(), name='tournament_detail'),
    path('round/<int:pk>/sections/', manage_sections, name='manage_sections'),
    path('round/<int:pk>/current/', set_current_round, name='set_current_round'),
    path('round/<int:pk>/remove/', remove_current_round, name='remove_current_round'),
    path('round/<int:pk>/open/', open_round, name='open_round'),
    path('round/<int:pk>/close/', close_round, name='close_round'),
    path('round/<int:pk>/admin/manual/', manage_topics, name='manage_topics'),
    path('round/<int:pk>/admin/', bulk_add_topics, name='bulk_add_topics'),
    path('topic/<int:pk>/', TopicDetail.as_view(), name='topic_detail'),
    path('section/<int:pk>/draw/select/', select_topic, name='select_topic'),
    path('section/<int:pk>/draw/', draw_topics, name='draw_topics'),
    path('section/<int:pk>/open/', open_section, name='open_section'),
    path('section/<int:pk>/close/', close_section, name='close_section'),
    path('section/<int:pk>/secret/', SectionDetail.as_view(), name='section_detail_secret'),
    path('section/<int:pk>/', SectionDetailProduction.as_view(), name='section_detail'),
    # path('roundgroup/<int:pk>/open/', open_roundgroup, name='open_roundgroup'),
    # path('roundgroup/<int:pk>/close/', close_roundgroup, name='close_roundgroup'),
    path('', TournamentList.as_view(), name='tournament_list'),
]
