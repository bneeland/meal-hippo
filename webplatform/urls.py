from django.urls import path, include

from . import views

app_namespace = 'webplatform'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_view'),
    path('support', views.SupportView.as_view(), name='support_view'),
    path('contact', views.ContactView.as_view(), name='contact_view'),
    path('supplier/guide', views.SupplierGuideView.as_view(), name='supplier_guide_view'),
    path('order/items', views.OrderItemsView.as_view(), name='order_items_view'),
    path('order/timing', views.OrderTimingView.as_view(), name='order_timing_view'),
    path('order/delivery', views.OrderDeliveryView.as_view(), name='order_delivery_view'),
    path('order/payment', views.OrderPaymentView.as_view(), name='order_payment_view'),
    path('order/complete', views.OrderCompleteView.as_view(), name='order_complete_view'),
    path('order/history', views.OrderHistoryView.as_view(), name='order_history_view'),
    path('feedback', views.FeedbackView.as_view(), name='feedback_view'),
    path('feedback/thanks', views.FeedbackCompleteView.as_view(), name='feedback_complete_view'),
    path('add_to_order/<int:pk>', views.add_to_order, name='add_to_order'),
    path('remove_from_order/<int:pk>', views.remove_from_order, name='remove_from_order'),
    path('to_be_delivered_toggle', views.to_be_delivered_toggle, name='to_be_delivered_toggle'),
    path('is_individual_toggle/<int:pk>', views.is_individual_toggle, name='is_individual_toggle'),
    path('subscribe_toggle/<path:path>', views.subscribe_toggle, name='subscribe_toggle'),
]
