from datetime import datetime
from random import sample

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin as LRM, UserPassesTestMixin as UPTM
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.forms import modelformset_factory, inlineformset_factory, ModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .models import *
from .forms import *


class LoginRequiredMixin(LRM):
    raise_exception = True


class AdminRequiredMixin(UPTM):
    raise_exception = True
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser


def admin_test(user):
    if user.is_anonymous or not user.is_superuser:
        raise PermissionDenied


def open_test(user, section):
    if not(user.is_authenticated and user.is_superuser) and not section.open:
        raise PermissionDenied


def current_test(user, section):
    if not(user.is_authenticated and user.is_superuser) and not section.round.current:
        raise PermissionDenied


def open_current_rounds(request, pk):
    admin_test(request.user)
    tournament = get_object_or_404(Tournament, pk=pk)
    for round in tournament.get_current_rounds():
        for section in round.section_set.all():
            section.open = True
            section.save()
    return redirect(tournament)


def close_current_rounds(request, pk):
    admin_test(request.user)
    tournament = get_object_or_404(Tournament, pk=pk)
    for round in tournament.get_current_rounds():
        for section in round.section_set.all():
            section.open = False
            section.save()
    return redirect(tournament)


def get_current_urls(request, pk):
    admin_test(request.user)
    tournament = get_object_or_404(Tournament, pk=pk)
    return render(request, 'extemp/get_current_urls.html', context={'tournament': tournament})


"""
def open_roundgroup(request, pk):
    admin_test(request.user)
    roundgroup = get_object_or_404(RoundGroup, pk=pk)
    for round in roundgroup.rounds.all():
        for section in round.section_set.all():
            section.open = True
            section.save()
    return redirect('extemp:manage_roundgroups', pk=roundgroup.tournament.pk)


def close_roundgroup(request, pk):
    admin_test(request.user)
    roundgroup = get_object_or_404(RoundGroup, pk=pk)
    for round in roundgroup.rounds.all():
        for section in round.section_set.all():
            section.open = False
            section.save()
    return redirect('extemp:manage_roundgroups', pk=roundgroup.tournament.pk)
"""


def set_current_round(request, pk):
    admin_test(request.user)
    round = get_object_or_404(Round, pk=pk)
    round.event.round_set.update(current=False)
    round.current = True
    round.save()
    return redirect(round.event.tournament)


def remove_current_round(request, pk):
    admin_test(request.user)
    round = get_object_or_404(Round, pk=pk)
    round.current = False
    round.save()
    return redirect(round.event.tournament)


def open_round(request, pk):
    admin_test(request.user)
    round = get_object_or_404(Round, pk=pk)
    for section in round.section_set.all():
        section.open = True
        section.save()
    return redirect(round.event.tournament)


def close_round(request, pk):
    admin_test(request.user)
    round = get_object_or_404(Round, pk=pk)
    for section in round.section_set.all():
        section.open = False
        section.save()
    return redirect(round.event.tournament)


def open_section(request, pk):
    admin_test(request.user)
    section = get_object_or_404(Section, pk=pk)
    section.open = True
    section.save()
    return redirect(section)


def close_section(request, pk):
    admin_test(request.user)
    section = get_object_or_404(Section, pk=pk)
    section.open = False
    section.save()
    return redirect(section)


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


"""
def manage_roundgroups(request, pk):
    admin_test(request.user)
    tournament = get_object_or_404(Tournament, pk=pk)
    RoundGroupFormSet = inlineformset_factory(Tournament, RoundGroup, form=RoundGroupForm, extra=3, can_delete=True)
    if request.method == "POST":
        roundgroupformset = RoundGroupFormSet(request.POST, instance=tournament)
        if roundgroupformset.is_valid():
            roundgroupformset.save()
            return redirect(tournament)
    else:
        roundgroupformset = RoundGroupFormSet(instance=tournament)
    return render(request, 'extemp/manage_roundgroups.html', context={'roundgroupformset': roundgroupformset, 'tournament': tournament})
"""

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
    topics = round.topic_set.order_by('code')
    topics_add = ([] for x in range(30-round.topic_set.count()))
    return render(request, 'extemp/manage_topics.html', context={'round': round, 'topics': topics, 'topics_add': topics_add})


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
    topics = round.topic_set.order_by('code')
    return render(request, 'extemp/bulk_add_topics.html', context={'round': round, 'topics': topics})


def draw_topics(request, pk):
    section = get_object_or_404(Section, pk=pk)
    current_test(request.user, section)
    if section.drawn_topics.exists():
        return redirect('extemp:select_topic', pk=pk)
    if request.method == 'POST' and (y:=request.POST.get('yes')) and (name:=request.POST.get('name')) and section.open:
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
    open_test(request.user, section)
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
            section.open = False
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
        form.instance.save()
        return redirect(form.instance.get_set_tournament_details_url())


def set_tournament_details(request, pk):
    admin_test(request.user)
    tournament = get_object_or_404(Tournament, pk=pk)
    choices = Round.ROUND_NAMES
    if request.method == "POST":
        keys = {x:{} for x in range(6)}
        for key in request.POST.keys():
            val = request.POST.get(key)
            if val is None or key == "csrfmiddlewaretoken":
                continue
            a, b = key.split("-")
            keys[int(a)][b] = val
        for row in keys.keys():
            name = keys[row]["name"]
            code = keys[row]["code"]
            if not name or not code:
                continue
            e, created = tournament.event_set.get_or_create(name=name, code=code)
            for choice, fullname in choices:
                if keys[row].get(choice):
                    e.round_set.get_or_create(name=choice)

        return redirect(tournament.get_absolute_url())
    return render(request, "extemp/set_tournament_details.html", context={"tournament": tournament, "choices": choices})


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