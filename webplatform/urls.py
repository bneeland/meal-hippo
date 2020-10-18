from django.urls import path, include

from . import views

app_namespace = 'webplatform'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_view'),
    path('app/support', views.SupportView.as_view(), name='support_view'),
    path('app/contact', views.ContactView.as_view(), name='contact_view'),
    path('app/supplier/guide', views.SupplierGuideView.as_view(), name='supplier_guide_view'),
    path('<supplier_slug>', views.OrderItemsView.as_view(), name='order_items_view'),
    path('app/order', views.OrderItemsView.as_view(), name='order_items_view'),
    path('app/order/timing', views.OrderTimingView.as_view(), name='order_timing_view'),
    path('app/order/delivery', views.OrderDeliveryView.as_view(), name='order_delivery_view'),
    path('app/order/payment', views.OrderPaymentView.as_view(), name='order_payment_view'),
    path('app/order/notes', views.OrderNotesView.as_view(), name='order_notes_view'),
    path('app/order/complete', views.OrderCompleteView.as_view(), name='order_complete_view'),
    path('app/order/history', views.OrderHistoryView.as_view(), name='order_history_view'),
    path('app/feedback', views.FeedbackView.as_view(), name='feedback_view'),
    path('app/feedback/thanks', views.FeedbackCompleteView.as_view(), name='feedback_complete_view'),
    path('app/supplier/signup', views.SupplierSignUpView.as_view(), name='supplier_sign_up_view'),
    path('app/add_to_order/<int:pk>', views.add_to_order, name='add_to_order'),
    path('app/remove_from_order/<int:pk>', views.remove_from_order, name='remove_from_order'),
    path('app/to_be_delivered_toggle', views.to_be_delivered_toggle, name='to_be_delivered_toggle'),
    path('app/is_individual_toggle/<int:pk>', views.is_individual_toggle, name='is_individual_toggle'),
    path('app/subscribe_toggle/<path:path>', views.subscribe_toggle, name='subscribe_toggle'),
    path('app/create_quick_feedback/<email>/<answer>', views.create_quick_feedback, name='create_quick_feedback'),
    path('app/list', views.ListView.as_view(), name='list_view'),
]
