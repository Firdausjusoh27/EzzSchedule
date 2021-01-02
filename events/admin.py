from __future__ import unicode_literals
from django.contrib import admin
from .models import Event, Slot


class EventAdmin(admin.ModelAdmin):
    list_display = ['day', 'start_time', 'end_time', 'notes']


class SlotEvent(admin.ModelAdmin):
    list_display = ['name', 'start_time', 'end_time']


admin.site.register(Event, EventAdmin)
admin.site.register(Slot, SlotEvent)

