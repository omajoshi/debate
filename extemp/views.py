from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import *

from django.contrib.auth.mixins import LoginRequiredMixin 

from random import sample

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


def draw_topics(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if section.drawn_topics.exists():
        topics = section.drawn_topics.all()
    else:
        topics = sample(list(section.unclaimed_topics()), 3)
        section.drawn_topics.add(*topics)
    if request.method == 'POST' and (t:=request.POST.get('topic')):
        topic_list = section.topicinstance_set.filter(pk=t)
        if topic_list.exists():
            topic = topic_list.get()
            topic.index = section.running_index
            topic.available = False
            topic.save()
            section.running_index += 1
            section.save()
        return redirect(section)
    return render(request, 'extemp/draw_topics.html', context={'topics': topics, 'section': section})

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
