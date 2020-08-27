from django.contrib import admin
from .models import *
# Register your models here.

class EventInline(admin.TabularInline):
    model = Event

class RoundInline(admin.TabularInline):
    model = Round

class SectionInline(admin.TabularInline):
    model = Section

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    inlines = [EventInline]

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [RoundInline]

@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    inlines = [SectionInline]


admin.site.register(Section)
admin.site.register(Topic)
admin.site.register(TopicInstance)
