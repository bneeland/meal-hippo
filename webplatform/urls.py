from django.urls import path, include

from . import views

app_namespace = 'webplatform'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_view'),
    path('support', views.SupportView.as_view(), name='support_view'),
    path('contact', views.ContactView.as_view(), name='contact_view'),
    path('dishes', views.DishesView.as_view(), name='dishes_view'),
    path('add_to_cart/<int:pk>', views.add_to_cart, name='add_to_cart')
]
