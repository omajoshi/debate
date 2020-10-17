from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.

class Tournament(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('extemp:tournament_detail', kwargs={'pk': self.pk})

    def get_set_tournament_details_url(self):
        return reverse('extemp:tournament_set_tournament_details', kwargs={'pk': self.pk})

    def get_current_rounds(self):
        return Round.objects.filter(event__tournament=self.pk, current=True).order_by('event_id')

    def __str__(self):
        return f'Tournament: {self.name}'

class Event(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.name} ({self.code}), {self.tournament}'


class Round(models.Model):
    ROUND_NAMES = (
        ("1", "Round 1",),
        ("2", "Round 2",),
        ("3", "Round 3",),
        ("4", "Round 4",),
        ("5", "Round 5",),
        ("6", "Round 6",),
        ("7", "Round 7",),
        ("8", "Round 8",),
        ("9", "Round 9",),
        ("d", "Doubles",),
        ("o", "Octas",),
        ("q", "Quarters",),
        ("s", "Semis",),
        ("f", "Finals",),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=1, choices=ROUND_NAMES)
    current = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.event.name}, {self.get_name_display()}'


class RoundGroup(models.Model):
    name = models.CharField(max_length=50)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    rounds = models.ManyToManyField(Round, blank=True)

    def __str__(self):
        return f'{self.name}'

class Section(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    running_index = models.IntegerField(default=1)
    drawn_topics = models.ManyToManyField('TopicInstance', blank=True, related_name='sections_drawn')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='sections_in')
    open = models.BooleanField(default=False)

    def claimed_topics(self):
        return self.topicinstance_set.filter(available=False).order_by('index')

    def unclaimed_topics(self):
        return self.topicinstance_set.filter(available=True).order_by('topic__code')

    def __str__(self):
        return f'{self.round} Section {self.name}'

    def get_absolute_url(self):
        return reverse('extemp:section_detail', kwargs={'pk': self.pk})

    def draw_url(self):
        return reverse('extemp:draw_topics', kwargs={'pk': self.pk})


class Topic(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    code = models.IntegerField()
    question = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.round}-{self.code} - {self.question}'

class TopicInstance(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    index = models.IntegerField(null=True, blank=True)
    modified = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'Section {self.section.name}, {self.topic}'

    def get_absolute_url(self):
        return reverse('extemp:topic_detail', kwargs={'pk': self.pk})
