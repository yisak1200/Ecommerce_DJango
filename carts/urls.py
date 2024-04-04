from django.urls import path
from .views import AddToCart,view_cart,Remove_cart,MyCart,Update_cart,OrderItemFromCart
urlpatterns = [
    path('Add_cart/<str:unique_id>/', AddToCart.as_view(), name='Add_cart'),
    path('carts/',view_cart.as_view(),name ='carts'),
    path('Remove_cart/<str:unique_id>/',Remove_cart.as_view(),name='remove_cart'),
    path('my_cart/',MyCart.as_view(),name='my_cart'),
    path('update_cart/<str:unique_id>/',Update_cart.as_view(),name = 'update_cart'),
    path('place_order/',OrderItemFromCart.as_view(),name='place_order')
    
]
