from django.urls import path, include

from . import views

app_namespace = 'webplatform'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_view'),
    path('support', views.SupportView.as_view(), name='support_view'),
    path('contact', views.ContactView.as_view(), name='contact_view'),
    path('order/items', views.OrderItemsView.as_view(), name='order_items_view'),
    path('order/timing', views.OrderTimingView.as_view(), name='order_timing_view'),
    path('order/delivery', views.OrderDeliveryView.as_view(), name='order_delivery_view'),
    path('order/payment', views.OrderPaymentView.as_view(), name='order_payment_view'),
    path('order/complete', views.OrderCompleteView.as_view(), name='order_complete_view'),
    path('charge', views.charge, name="charge"),
    path('add_to_order/<int:pk>', views.add_to_order, name='add_to_order'),
    path('remove_from_order/<int:pk>', views.remove_from_order, name='remove_from_order'),
]
