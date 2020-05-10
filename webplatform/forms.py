from django import forms
from django.forms import ModelForm
from django.utils import timezone
import datetime
from django.utils import timezone
from datetime import timedelta

from . import models

class OrderTimingForm(ModelForm):
    class Meta:
        model = models.Order
        fields = ['delivery_date', 'delivery_time']

        cutoff_days = 2
        number_of_dates = 5
        sunday = timezone.localtime(timezone.now()).date() + datetime.timedelta(cutoff_days)
        while sunday.weekday() != 6:
            sunday += datetime.timedelta(1)
        DATE_CHOICES = (
        )
        for i in range(number_of_dates):
            next_date_as_date = sunday + datetime.timedelta(i*7)
            next_date_as_str = next_date_as_date.strftime("%A, %B %-d")
            DATE_CHOICE = ((next_date_as_date, next_date_as_str),)
            DATE_CHOICES += DATE_CHOICE

        widgets = {
            'delivery_date': forms.Select(choices=DATE_CHOICES),
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
