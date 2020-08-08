from django import forms
from django.forms import ModelForm
from django.utils import timezone
import datetime
# from datetime import timedelta, time

from . import models

class OrderTimingForm(ModelForm):
    class Meta:
        model = models.Order
        fields = ['delivery_date', 'delivery_time']
        labels = {
            'delivery_date': 'Date',
            'delivery_time': 'Time', 
        }


        # Date dropdown menu choices
        cutoff_days = 1
        weeks_worth_of_dates = 3
        acceptable_days = [0, 1, 2, 3, 4, ] # Monday is 0, Tuesday is 1, ... Sunday is 6
        blackout_day = datetime.date(2020, 8, 3)

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
                    if next_date_as_date != blackout_day:
                        next_date_as_str = next_date_as_date.strftime("%A, %B %-d")
                        DATE_CHOICE = ((next_date_as_date, next_date_as_str),)
                        DATE_CHOICES += DATE_CHOICE


        # Time dropdown menu choices
        TIME_CHOICES = (('', 'Select a time'),)

        time = datetime.time(13, 30)
        time_start = datetime.time(13, 30).strftime("%-I:%M %p")
        time_end = datetime.time(14, 00).strftime("%-I:%M %p")
        time_range = f"{time_start} - {time_end}"
        TIME_CHOICE = (((time, time_range),))
        TIME_CHOICES += TIME_CHOICE

        time = datetime.time(14, 00)
        time_start = datetime.time(14, 00).strftime("%-I:%M %p")
        time_end = datetime.time(14, 30).strftime("%-I:%M %p")
        time_range = f"{time_start} - {time_end}"
        TIME_CHOICE = (((time, time_range),))
        TIME_CHOICES += TIME_CHOICE

        time = datetime.time(14, 30)
        time_start = datetime.time(14, 30).strftime("%-I:%M %p")
        time_end = datetime.time(15, 00).strftime("%-I:%M %p")
        time_range = f"{time_start} - {time_end}"
        TIME_CHOICE = (((time, time_range),))
        TIME_CHOICES += TIME_CHOICE

        time = datetime.time(15, 00)
        time_start = datetime.time(15, 00).strftime("%-I:%M %p")
        time_end = datetime.time(15, 30).strftime("%-I:%M %p")
        time_range = f"{time_start} - {time_end}"
        TIME_CHOICE = (((time, time_range),))
        TIME_CHOICES += TIME_CHOICE


        # start_time_h = 13 # 12 is noon
        # start_time_m = 30
        # end_time_h = 15
        # end_time_m = 30
        #
        # TIME_CHOICES = (('', 'Select a time'),)
        #
        # for next_hour in range(start_time_h, end_time_h + 1):
        #     next_time_as_date__start = datetime.datetime(100, 1, 1, next_hour, start_time_m)
        #     next_time_as_date__end = datetime.datetime(100, 1, 1, next_hour, start_time_m) + datetime.timedelta(minutes=30)
        #
        #     next_time_as_time__start = next_time_as_date__start.time()
        #     next_time_as_time__end = next_time_as_date__end.time()
        #
        #     next_time_as_str__start = next_time_as_time__start.strftime("%-I:%M %p")
        #     next_time_as_str__end = next_time_as_time__end.strftime("%-I:%M %p")
        #
        #     next_timespan_as_str = f"{next_time_as_str__start} - {next_time_as_str__end}"
        #
        #     TIME_CHOICE = (
        #         ((next_time_as_date__start, next_timespan_as_str),)
        #     )
        #     TIME_CHOICES += TIME_CHOICE



        # start_time_h = 13 # 12 is noon
        # start_time_m = 30
        # end_time_h = 15
        # end_time_m = 30
        # cutoff_time_for_hot_h = 4
        # cutoff_time_for_hot_m = 00
        # TIME_CHOICES = (('', 'Select a time'),)
        # for t in range(start_time_h, end_time_h + 1):
        #     if t < cutoff_time_for_hot_h:
        #         # hot_or_cold = "(fresh and warm)"
        #         hot_or_cold = ""
        #     else:
        #         # hot_or_cold = "(fresh and refrigerated - heat and serve)"
        #         hot_or_cold = ""
        #     # :00
        #     next_time_as_time = datetime.time(t, start_time_m)
        #     next_time_as_time__end = (datetime.datetime(100, 1, 1, t, start_time_m) + datetime.timedelta(minutes=30)).time()
        #     # next_time_as_time__end = next_time_as_time + time(0, 30)
        #     next_time_as_str = next_time_as_time.strftime("%-I:%M %p")
        #     next_time_as_str__end = next_time_as_time__end.strftime("%-I:%M %p")
        #     next_timespan_as_str = f"{next_time_as_str} - {next_time_as_str__end} {hot_or_cold}"
        #     TIME_CHOICE = (
        #         ((next_time_as_time, next_timespan_as_str),)
        #     )
        #     TIME_CHOICES += TIME_CHOICE
            # # :30
            # next_time_as_time = time(t+12, 30)
            # next_time_as_time__end = time(t+12+1, 00)
            # next_time_as_str = next_time_as_time.strftime("%-I:%M %p")
            # next_time_as_str__end = next_time_as_time__end.strftime("%-I:%M %p")
            # next_timespan_as_str = f"{next_time_as_str} - {next_time_as_str__end} {hot_or_cold}"
            # TIME_CHOICE = (
            #     ((next_time_as_time, next_timespan_as_str),)
            # )
            # TIME_CHOICES += TIME_CHOICE

        widgets = {
            'delivery_date': forms.Select(choices=DATE_CHOICES),
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
