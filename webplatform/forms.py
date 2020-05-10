from django import forms
from django.forms import ModelForm
from django.utils import timezone
import datetime
from django.utils import timezone
from datetime import timedelta, time

from . import models

class OrderTimingForm(ModelForm):
    class Meta:
        model = models.Order
        fields = ['delivery_date', 'delivery_time']

        # Date dropdown menu choices
        cutoff_days = 2
        number_of_dates = 5
        sunday = timezone.localtime(timezone.now()).date() + datetime.timedelta(cutoff_days)
        while sunday.weekday() != 6:
            sunday += datetime.timedelta(1)
        DATE_CHOICES = (('', 'Select a date'),)
        for d in range(number_of_dates):
            next_date_as_date = sunday + datetime.timedelta(d*7)
            next_date_as_str = next_date_as_date.strftime("%A, %B %-d")
            DATE_CHOICE = ((next_date_as_date, next_date_as_str),)
            DATE_CHOICES += DATE_CHOICE

        # Time dropdown menu choices
        start_time = 0 # 0 is noon
        end_time = 9
        TIME_CHOICES = (('', 'Select a time'),)
        for t in range(start_time, end_time + 1):
            # :00
            next_time_as_time = time(t+12, 00)
            next_time_as_time__end = time(t+12, 30)
            next_time_as_str = next_time_as_time.strftime("%-I:%M %p")
            next_time_as_str__end = next_time_as_time__end.strftime("%-I:%M %p")
            next_timespan_as_str = f"{next_time_as_str} - {next_time_as_str__end}"
            TIME_CHOICE = (
                ((next_time_as_time, next_timespan_as_str),)
            )
            TIME_CHOICES += TIME_CHOICE
            # :30
            next_time_as_time = time(t+12, 30)
            next_time_as_time__end = time(t+12+1, 00)
            next_time_as_str = next_time_as_time.strftime("%-I:%M %p")
            next_time_as_str__end = next_time_as_time__end.strftime("%-I:%M %p")
            next_timespan_as_str = f"{next_time_as_str} - {next_time_as_str__end}"
            TIME_CHOICE = (
                ((next_time_as_time, next_timespan_as_str),)
            )
            TIME_CHOICES += TIME_CHOICE

        widgets = {
            'delivery_date': forms.Select(choices=DATE_CHOICES),
            # 'delivery_time': forms.TimeInput(attrs={'type': 'time'}),
            'delivery_time': forms.Select(choices=TIME_CHOICES),
        }

class OrderDeliveryForm(ModelForm):
    class Meta:
        model = models.UserDeliveryDetail
        fields = ['phone', 'address', 'instructions', 'is_subscribed']
        widgets = {
          'address': forms.Textarea(attrs={'rows':4}),
          'instructions': forms.Textarea(attrs={'rows':4}),
        }
