from django import forms
from django.forms import ModelForm

from . import models

class OrderTimingForm(ModelForm):
    class Meta:
        model = models.Order
        fields = ['delivery_date', 'delivery_time']
        widgets = {
            'delivery_date': forms.SelectDateWidget(),
            'delivery_time': forms.TimeInput(),
        }
