from django.forms import ModelForm
from .models import Vip, PurposeItem


class VipForm(ModelForm):
    class Meta:
        model = Vip
        fields = '__all__'
        exclude = ('user',)


class PurposeForm(ModelForm):
    class Meta:
        model = PurposeItem
        fields = '__all__'
