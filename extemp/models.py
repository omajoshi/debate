from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.

class Tournament(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('extemp:tournament_detail', kwargs={'pk': self.pk})

class Event(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)


class Round(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

class Section(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

class Topic(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    code = models.IntegerField()
    question = models.CharField(max_length=200)

class TopicInstance(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
