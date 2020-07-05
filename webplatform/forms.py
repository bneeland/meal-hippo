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
        cutoff_days = 11
        weeks_worth_of_dates = 1
        acceptable_days = [2,] # Monday is 0, Tuesday is 1, ... Sunday is 6
        first_date = timezone.localtime(timezone.now()).date() + datetime.timedelta(cutoff_days)
        while first_date.weekday() not in acceptable_days:
            first_date += datetime.timedelta(1)
        DATE_CHOICES = (('', 'Select a date'),)
        for w in range(0, weeks_worth_of_dates):
            for d in acceptable_days:
                if w == 0 and first_date.weekday() > d:
                    pass
                else:
                    next_date_as_date = first_date + datetime.timedelta(w*7 + d - first_date.weekday())
                    next_date_as_str = next_date_as_date.strftime("%A, %B %-d")
                    DATE_CHOICE = ((next_date_as_date, next_date_as_str),)
                    DATE_CHOICES += DATE_CHOICE

        # next_date_as_date = datetime.datetime(2020, 7, 23)
        # next_date_as_str = next_date_as_date.strftime("%A, %B %-d")
        # DATE_CHOICES = ((next_date_as_date, next_date_as_str),)

        # Time dropdown menu choices
        start_time = 4 # 0 is noon
        end_time = 6
        cutoff_time_for_hot = 7
        TIME_CHOICES = (('', 'Select a time'),)
        for t in range(start_time, end_time + 1):
            if t < cutoff_time_for_hot:
                # hot_or_cold = "(fresh and warm)"
                hot_or_cold = ""
            else:
                # hot_or_cold = "(fresh and refrigerated - heat and serve)"
                hot_or_cold = ""
            # :00
            next_time_as_time = time(t+12, 00)
            next_time_as_time__end = time(t+12, 30)
            next_time_as_str = next_time_as_time.strftime("%-I:%M %p")
            next_time_as_str__end = next_time_as_time__end.strftime("%-I:%M %p")
            next_timespan_as_str = f"{next_time_as_str} - {next_time_as_str__end} {hot_or_cold}"
            TIME_CHOICE = (
                ((next_time_as_time, next_timespan_as_str),)
            )
            TIME_CHOICES += TIME_CHOICE
            # :30
            next_time_as_time = time(t+12, 30)
            next_time_as_time__end = time(t+12+1, 00)
            next_time_as_str = next_time_as_time.strftime("%-I:%M %p")
            next_time_as_str__end = next_time_as_time__end.strftime("%-I:%M %p")
            next_timespan_as_str = f"{next_time_as_str} - {next_time_as_str__end} {hot_or_cold}"
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
        fields = ['phone', 'address', 'instructions']
        widgets = {
          'address': forms.Textarea(attrs={'rows':4}),
          'instructions': forms.Textarea(attrs={'rows':4}),
        }

class FeedbackForm(ModelForm):
    class Meta:
        model = models.Feedback
        fields = ['feel_if_no_longer', 'type_of_people', 'main_benefit', 'how_to_improve']
        widgets = {
            'feel_if_no_longer': forms.RadioSelect,
            'type_of_people': forms.Textarea(attrs={'rows':3}),
            'main_benefit': forms.Textarea(attrs={'rows':3}),
            'how_to_improve': forms.Textarea(attrs={'rows':3}),
        }
