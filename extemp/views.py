from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import *
from django.forms import modelformset_factory, inlineformset_factory

from datetime import datetime
from django.utils import timezone

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin as LRM, UserPassesTestMixin as UPTM
from django.contrib.auth.decorators import login_required, user_passes_test
from random import sample

class LoginRequiredMixin(LRM):
    raise_exception = True

class AdminRequiredMixin(UPTM):
    raise_exception = True
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

def admin_test(user):
    if user.is_anonymous or not user.is_superuser:
        raise PermissionDenied

def open_test(user, round):
    if not(user.is_authenticated and user.is_superuser) and not round.open:
        raise PermissionDenied

def toggle_open_round(request, pk):
    admin_test(request.user)
    round = get_object_or_404(Round, pk=pk)
    round.open = not round.open
    round.save()
    return redirect(round.event.tournament)

def manage_sections(request, pk):
    admin_test(request.user)
    round = get_object_or_404(Round, pk=pk)
    SectionFormSet = inlineformset_factory(Round, Section, fields=['name'], extra=3, can_delete=True)
    if request.method == "POST":
        sectionformset = SectionFormSet(request.POST, instance=round)
        if sectionformset.is_valid():
            sections = sectionformset.save()
            for section in sections:
                for topic in round.topic_set.all():
                    section.topicinstance_set.create(topic=topic)
            return redirect('extemp:tournament_detail', pk=round.event.tournament.pk)
    else:
        sectionformset = SectionFormSet(instance=round)
    return render(request, 'extemp/manage_sections.html', context={'sectionformset': sectionformset, 'round': round})

def manage_topics(request, pk):
    admin_test(request.user)
    round = get_object_or_404(Round, pk=pk)
    if request.method == 'POST':
        for x in range(1, 31):
            if (c:=request.POST.get(f'code-{x}')) and (q:=request.POST.get(f'question-{x}')):
                t, created = round.topic_set.update_or_create(code=c, defaults={'question': q})
                if created:
                    for section in round.section_set.all():
                        section.topicinstance_set.create(topic=t)
            elif (p:=request.POST.get(f'pk-{x}')):
               Topic.objects.get(pk=p).delete()
        return redirect(round.event.tournament)
    topics = (* (round.topic_set.order_by('code')), *([] for x in range(30-round.topic_set.count())))
    return render(request, 'extemp/manage_topics.html', context={'round': round, 'topics': topics})


def bulk_add_topics(request, pk):
    admin_test(request.user)
    round = get_object_or_404(Round, pk=pk)
    if request.method == 'POST' and (c:=request.POST.get('topics')):
        round.topic_set.all().delete()
        lines = c.splitlines()
        for i, line in enumerate(lines):
            if line:
                t = round.topic_set.create(code=i+1, question=line)
                for section in round.section_set.all():
                    section.topicinstance_set.create(topic=t)
        return redirect('extemp:manage_topics', pk=round.pk)
    return render(request, 'extemp/bulk_add_topics.html', context={'round': round})


def draw_topics(request, pk):
    section = get_object_or_404(Section, pk=pk)
    open_test(request.user, section.round)
    if section.drawn_topics.exists():
        return redirect('extemp:select_topic', pk=pk)
    if request.method == 'POST' and (y:=request.POST.get('yes')) and (name:=request.POST.get('name')):
        topics = sample(list(section.unclaimed_topics()), 3)
        for topic in topics:
            topic.modified = datetime.now(tz=timezone.utc)
            topic.name = name
            topic.save()
        section.drawn_topics.add(*topics)
        return redirect('extemp:select_topic', pk=pk)
    return render(request, 'extemp/draw_topics.html', context={'section': section})

def select_topic(request, pk):
    section = get_object_or_404(Section, pk=pk)
    open_test(request.user, section.round)
    if not section.drawn_topics.exists():
        return redirect('extemp:draw_topics', pk=pk)
    topics = section.drawn_topics.all()
    if request.method == 'POST' and (t:=request.POST.get('topic')):
        topic_list = topics.filter(pk=t)
        if topic_list.exists():
            topic = topic_list.get()
            topic.index = section.running_index
            topic.available = False
            topic.save()
            section.running_index += 1
            section.save()
            section.drawn_topics.clear()
            # return redirect(topic)
            return render(request, 'extemp/topicinstance_detail.html', context={'topicinstance': topic})
    return render(request, 'extemp/select_topic.html', context={'topics': topics, 'section': section})

class ActivationRequiredMixin:
    pass

class TournamentCreate(AdminRequiredMixin, CreateView):
    model = Tournament
    fields = ["name"]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TournamentDetail(AdminRequiredMixin, DetailView):
    model = Tournament

class TournamentList(AdminRequiredMixin, ListView):
    model = Tournament

class SectionDetail(AdminRequiredMixin, DetailView):
    model = Section

class SectionDetailProduction(DetailView):
    model = Section
    template_name = 'extemp/section_detail_production.html'

class TopicDetail(AdminRequiredMixin, DetailView):
    model = TopicInstance
