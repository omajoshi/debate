from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import *


def create_view(request):
    pass


def view_available_topics():
    pass

def manage_sections(request, pk):
    return


def manage_topics(request, pk):
    round = get_object_or_404(Round, pk=pk)
    if request.method == 'POST':
        for x in range(1, 21):
            if (c:=request.POST.get(f'code-{x}')) and (q:=request.POST.get(f'question-{x}')):
                t, created = round.topic_set.update_or_create(code=c, defaults={'question': q})
                if created:
                    for section in round.section_set.all():
                        section.topicinstance_set.create(topic=t)
            elif (p:=request.POST.get(f'pk-{x}')):
               Topic.objects.get(pk=p).delete()
        return redirect(round.event.tournament)
    topics = (* (round.topic_set.order_by('code')), *([] for x in range(20-round.topic_set.count())))
    return render(request, 'extemp/manage_topics.html', context={'round': round, 'topics': topics})


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

class SectionDetail(DetailView):
    model = Section
