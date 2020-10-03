from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.

class EventInline(admin.TabularInline):
    model = Event

class RoundInline(admin.TabularInline):
    model = Round

class SectionInline(admin.TabularInline):
    model = Section

class TopicInstanceInline(admin.TabularInline):
    model = TopicInstance

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    inlines = [EventInline]

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [RoundInline]

@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    inlines = [SectionInline]

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    inlines = [TopicInstanceInline]

admin.site.register(Topic)
admin.site.register(TopicInstance)

@admin.register(RoundGroup)
class RoundGroupAdmin(admin.ModelAdmin):
    form = RoundGroupForm
    fields = ['tournament', 'name', 'rounds']
