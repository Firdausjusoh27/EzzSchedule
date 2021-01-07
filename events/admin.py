from __future__ import unicode_literals
from django.contrib import admin
from .models import Event, Slot, iSlot


class EventAdmin(admin.ModelAdmin):
    list_display = ['day', 'start_time', 'end_time', 'notes']


class SlotEvent(admin.ModelAdmin):
    list_display = ['name', 'start_time', 'end_time']


class iSlotAdmin(admin.ModelAdmin):
    list_display = ['purpose_id', 'date', 'slot']


admin.site.register(Event, EventAdmin)
admin.site.register(Slot, SlotEvent)
admin.site.register(iSlot, iSlotAdmin)

