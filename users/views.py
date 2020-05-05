from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail

from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        new_user = authenticate(email=email, password=password)
        login(self.request, new_user)

        # send_mail(
        #     subject='New user signed up on mealhippo.com',
        #     message='A new user signed up on mealhippo.com. The user\'s email is '+email+'.',
        #     from_email='web.bot@mealhippo.com',
        #     recipient_list=['hello@mealhippo.com'],
        #     fail_silently=True,
        # )

        return valid

    def get_success_url(self):
        next = self.request.POST.get('next')
        if next == None:
            return reverse_lazy('webplatform:home_view')
        else:
            return next
