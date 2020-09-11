from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.utils import timezone

from . import forms
from . import tasks

class SignUpView(CreateView):
    form_class = forms.CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        new_user = authenticate(email=email, password=password)
        login(self.request, new_user)

        # tasks.send_mail_with_celery.delay(
        #     subject='New user signed up on mealhippo.com beta',
        #     message='A new user signed up on mealhippo.com beta. The user who did this was '+email+'. This was done at '+str(timezone.localtime(timezone.now()))+'.',
        #     recipient_list=['hello@mealhippo.com'],
        #     html_message='<h1>New user</h1><p>A new user signed up on mealhippo.com beta.</p><p>The user who did this was '+email+'.</p><p>This was done at '+str(timezone.localtime(timezone.now()))+'.</p>',
        # )

        tasks.send_mail_with_celery.delay(
            subject='Welcome to Meal Hippo!',
            message='Hi '+email+'! Welcome to Meal Hippo! Thank you so much for joining us. You’re on your way to saving time and effort with good, convenient food, effortlessly. Meal Hippo makes it easy to order fully cooked, ready-to-eat home-style food, so you can enjoy great food every day—even when you don\'t have time to cook. Order a multi-portion dish, and use it for lunches and supper for the next few days, or feed the whole family family easily--with enough for leftovers. Your next step would be to make an order through Meal Hippo. Click here to check out the dishes available in your area! Have any questions? Just shoot us an email! We’re always here to help. The Meal Hippo team &middot; hello@mealhippo.com &middot; mealhippo.com',
            recipient_list=[email],
            html_message='<p>Hi '+email+'!</p><p>Welcome to Meal Hippo! Thank you so much for joining us. You’re on your way to saving time and effort with good, convenient food, effortlessly.</p><p>Meal Hippo makes it easy to order fully cooked, ready-to-eat home-style food, so you can enjoy great food every day—even when you don\'t have time to cook. Order a multi-portion dish, and use it for lunches and supper for the next few days, or feed the whole family family easily--with enough for leftovers.</p><p>Your next step would be to make an order through Meal Hippo. <a href="https://www.mealhippo.com/order/items"><b>Click here</b></a> to check out the dishes available in your area!</p><p>Have any questions? Just shoot us an email! We’re always here to help.</p><p>The Meal Hippo team<br>hello@mealhippo.com<br>mealhippo.com</p>',
        )

        return valid

    def get_success_url(self):
        next = self.request.POST.get('next')
        if next == None:
            return reverse_lazy('webplatform:home_view')
        else:
            return next
