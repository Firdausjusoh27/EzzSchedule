from django.forms import ModelForm
from .models import Vip


class VipForm(ModelForm):
    class Meta:
        model = Vip
        fields = '__all__'
