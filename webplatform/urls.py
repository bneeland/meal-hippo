from django.urls import path, include

from . import views

app_namespace = 'webplatform'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_view'),
    path('support', views.SupportView.as_view(), name='support_view'),
    path('contact', views.ContactView.as_view(), name='contact_view'),
    path('dishes', views.DishesView.as_view(), name='dishes_view'),
    path('add_to_order/<int:pk>', views.add_to_order, name='add_to_order'),
    path('remove_from_order/<int:pk>', views.remove_from_order, name='remove_from_order'),
]
