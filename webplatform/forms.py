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

        widgets = {
            'delivery_date': forms.Select(),
            'delivery_time': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super(OrderTimingForm, self).__init__(*args, **kwargs)

        order_items = self.instance.items.all()

        # Set list of dates

        cutoff_days = 1
        weeks_worth_of_dates = 3
        blackout_day = datetime.date(2020, 8, 18)

        acceptable_days_qs = order_items[0].item.supplier.day_range.all()

        for order_item in order_items:
            acceptable_days_qs = acceptable_days_qs.intersection(order_item.item.supplier.day_range.all())

        acceptable_days = []

        for acceptable_day in acceptable_days_qs:
            acceptable_days += [acceptable_day.number]

        print(acceptable_days)
        acceptable_days.sort()
        print(acceptable_days)

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



        # Set list of times

        start_time_h = order_items[0].item.supplier.start_time_h
        start_time_m = order_items[0].item.supplier.start_time_m
        end_time_h = order_items[0].item.supplier.end_time_h
        end_time_m = order_items[0].item.supplier.end_time_m

        for order_item in order_items:
            if order_item.item.supplier.start_time_h > start_time_h:
                start_time_h = order_item.item.supplier.start_time_h
                if order_item.item.supplier.start_time_m > start_time_m:
                    start_time_m = order_item.item.supplier.start_time_m

            if order_item.item.supplier.end_time_h < end_time_h:
                end_time_h = order_item.item.supplier.end_time_h
                if order_item.item.supplier.end_time_m < end_time_m:
                    end_time_m = order_item.item.supplier.end_time_m

        TIME_CHOICES = (('', 'Select a time'),)

        for next_hour, next_minute in [(h, m) for h in range(start_time_h, end_time_h+1) for m in [0, 30]]:
            if (
                    ((start_time_m == 30 and next_minute == 0) and next_hour == start_time_h)
                    or ((end_time_m == 0 and next_minute == 30) and next_hour == end_time_h)
                ):
                pass
            else:
                next_time_as_date__start = datetime.datetime(100, 1, 1, next_hour, next_minute)
                next_time_as_date__end = next_time_as_date__start + datetime.timedelta(minutes=30)

                next_time_as_time__start = next_time_as_date__start.time()
                next_time_as_time__end = next_time_as_date__end.time()

                next_time_as_str__start = next_time_as_time__start.strftime("%-I:%M %p")
                next_time_as_str__end = next_time_as_time__end.strftime("%-I:%M %p")

                next_timespan_as_str = f"{next_time_as_str__start} - {next_time_as_str__end}"

                TIME_CHOICE = (
                    ((next_time_as_date__start, next_timespan_as_str),)
                )
                TIME_CHOICES += TIME_CHOICE

        self.fields['delivery_date'].widget.choices = DATE_CHOICES
        self.fields['delivery_time'].widget.choices = TIME_CHOICES

class OrderDeliveryForm(ModelForm):
    class Meta:
        model = models.UserDeliveryDetail
        fields = ['phone', 'address', 'instructions']
        widgets = {
          'address': forms.Textarea(attrs={'rows':4}),
          'instructions': forms.Textarea(attrs={'rows':4}),
        }

class OrderNotesForm(ModelForm):
    class Meta:
        model = models.Order
        fields = ['notes',]
        widgets = {
          'notes': forms.Textarea(attrs={'rows':4}),
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


class SupplierSignUpForm(ModelForm):
    class Meta:
        model = models.UserSupplierInfo
        fields = ['first_name', 'last_name', 'company_name', 'company_address', 'agree_to_terms_conditions']
        widgets = {
            'company_address': forms.Textarea(attrs={'rows':3}),
        }

    def clean_agree_to_terms_conditions(self):
        agree_to_terms_conditions = self.cleaned_data.get('agree_to_terms_conditions')
        if not agree_to_terms_conditions:
            raise forms.ValidationError('You must agree to continue')
        return agree_to_terms_conditions
