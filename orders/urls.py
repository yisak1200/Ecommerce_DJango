from django.urls import path
from .views import *
urlpatterns = [
    path('order_page/<str:unique_id>/', order_view.as_view(), name='order_page'),
    path('order_status/',OrderStatus.as_view(),name='order_status'),
    path('order_detail/<str:unique_id>/',OrderDetail.as_view(),name='order_detail'),
    path('order-history/',OrderHistory.as_view(),name='order_history')
    # path('order_done/', order_done.as_view(), name='order_done')
]
