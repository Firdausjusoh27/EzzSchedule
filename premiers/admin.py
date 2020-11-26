from django.contrib import admin
from .models import Event, Appointment, MainPurpose, SubPurpose, Vip, CompanyType, Title, Position, PurposeItem


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time')


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'vip_name', 'date')


class MainPurposeAdmin(admin.ModelAdmin):
    list_display = ('main_item', 'main_weight')


class SubPurposeAdmin(admin.ModelAdmin):
    list_display = ('sub_item', 'main_purpose', 'sub_weight')


class VipProfileAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'company')


class CompanyTypeAdmin(admin.ModelAdmin):
    list_display = ('company_item', 'company_weight')


class PositionAdmin(admin.ModelAdmin):
    list_display = ('position_item', 'position_weight')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('title_item', 'title_weight')


class PurposeItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'main_purpose', 'sub_purpose')


admin.site.register(Event, EventAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(MainPurpose, MainPurposeAdmin)
admin.site.register(SubPurpose, SubPurposeAdmin)
admin.site.register(Vip, VipProfileAdmin)
admin.site.register(CompanyType, CompanyTypeAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(PurposeItem, PurposeItemAdmin)

