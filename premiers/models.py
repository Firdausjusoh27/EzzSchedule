from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings


class EventDummy(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    time = models.TimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    def __str__(self):
        return self.id


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True, null=True)
    vip_name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    start_time = models.TimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    end_time = models.TimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    def __str__(self):
        return self.title


class MainPurpose(models.Model):
    main_item = models.CharField(max_length=200, null=True)
    main_weight = models.FloatField(null=True)
    image = models.ImageField(default='default.jpg', upload_to='MainPurpose_pics')
    description = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.main_item


class SubPurpose(models.Model):
    main_purpose = models.ForeignKey(MainPurpose, on_delete=models.CASCADE)
    sub_item = models.CharField(max_length=200, null=True)
    sub_weight = models.FloatField(null=True)
    image = models.ImageField(default='default.jpg', upload_to='SubPurpose_pics')
    description = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.sub_item


class Title(models.Model):
    title_item = models.CharField(max_length=200, null=True)
    title_weight = models.FloatField(null=True)

    def __str__(self):
        return self.title_item


class CompanyType(models.Model):
    company_item = models.CharField(max_length=200, null=True)
    company_weight = models.FloatField(null=True)

    def __str__(self):
        return self.company_item


class Position(models.Model):
    position_item = models.CharField(max_length=200, null=True)
    position_weight = models.FloatField(null=True)

    def __str__(self):
        return self.position_item


class Vip(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, default='')
    title = models.ForeignKey(Title, on_delete=models.CASCADE, null=True, default='')
    name = models.CharField(max_length=200, null=True)
    company = models.CharField(max_length=200, null=True)
    company_Type = models.ForeignKey(CompanyType, on_delete=models.CASCADE, null=True, default='')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, default='')
    email = models.EmailField()

    def __str__(self):
        return self.name


class PurposeDetail(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, default='')
    vip = models.ForeignKey(Vip, on_delete=models.CASCADE, blank=True, null=True)
    main_purpose = models.ForeignKey(MainPurpose, on_delete=models.CASCADE, blank=True, null=True)
    sub_purpose = models.ForeignKey(SubPurpose, on_delete=models.CASCADE, blank=True, null=True)
    fuzzy_weight = models.FloatField(null=True)

