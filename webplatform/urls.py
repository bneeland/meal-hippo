from django.urls import path, include

from . import views

app_namespace = 'webplatform'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_view'),
    path('about', views.AboutView.as_view(), name='about_view'),
    path('contact', views.ContactView.as_view(), name='contact_view'),
]
