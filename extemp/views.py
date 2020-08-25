from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import *


def create_view(request):
    pass


def view_available_topics():
    pass


def create_topic(request):
    for section in topic.round.section_set.all():
        TopicInstance.objects.create(topic=topic, section=section)



def draw(request):
    return HttpResponse("drawn?")
    # return render(request, '', {})

class ActivationRequiredMixin:
    pass

class TournamentCreate(ActivationRequiredMixin, CreateView):
    model = Tournament
    fields = ["name"]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class TournamentDetail(DetailView):
    model = Tournament

class TournamentList(ListView):
    model = Tournament
