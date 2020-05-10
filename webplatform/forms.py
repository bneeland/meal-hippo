from django import forms
from django.forms import ModelForm
from django.utils import timezone
import datetime
from datetime import time, timedelta

from . import models

class OrderTimingForm(ModelForm):
    class Meta:
        model = models.Order
        fields = ['delivery_date', 'delivery_time']
        DATE_CHOICES = (
            ('', ''),
            (datetime.date(2019, 4, 13), '2019-04-13'),
            (datetime.date(2019, 4, 14), '2019-04-14'),
            (datetime.date(2019, 4, 15), '2019-04-15'),
        )
        widgets = {
            'delivery_date': forms.Select(attrs={'type': 'date'}, choices=DATE_CHOICES),
            'delivery_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class OrderDeliveryForm(ModelForm):
    class Meta:
        model = models.UserDeliveryDetail
        fields = ['phone', 'address', 'instructions', 'is_subscribed']
        widgets = {
          'address': forms.Textarea(attrs={'rows':4}),
          'instructions': forms.Textarea(attrs={'rows':4}),
        }
