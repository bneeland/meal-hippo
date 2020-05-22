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

        tasks.send_mail_with_celery.delay(
            subject='New user signed up on mealhippo.com beta',
            message='A new user signed up on mealhippo.com beta. The user who did this was '+email+'. This was done at '+str(timezone.localtime(timezone.now()))+'.',
            recipient_list=['hello@mealhippo.com'],
            html_message='<h1>New user</h1><p>A new user signed up on mealhippo.com beta.</p><p>The user who did this was '+email+'.</p><p>This was done at '+str(timezone.localtime(timezone.now()))+'.</p>',
        )

        tasks.send_mail_with_celery.delay(
            subject='Thanks for signing up to Meal Hippo!',
            message='Hi '+email+', Thanks for signing up on mealhippo.com! If you have any questions about Meal Hippo, such as how to start your order, don\'t hesitate to get in touch with me by phone or email. I\'d be happy to help. -Brian from Meal Hippo | Call: 780-243-7675 | Email: hello@mealhippo.com | beta.mealhippo.com',
            recipient_list=[email],
            html_message='<h1>Thanks for signing up to Meal Hippo!</h1><p>Hi '+email+',</p><p>Thanks for signing up on mealhippo.com!</p><p>If you have any questions about Meal Hippo, such as how to start your order, don\'t hesitate to get in touch with me by phone or email. I\'d be happy to help.</p><p>Brian</p><p>Meal Hippo<br>Meal Hippo<br>Call: 780-243-7675<br>Email: hello@mealhippo.com<br><a href="https://b.mealhippo.com">beta.mealhippo.com</a></p>',
        )

        return valid

    def get_success_url(self):
        next = self.request.POST.get('next')
        if next == None:
            return reverse_lazy('webplatform:home_view')
        else:
            return next
