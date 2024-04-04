from django.urls import path
from .views import index_page, all_products,ProductDetail,Page404,CommentView,ProductByCategory,product_search

urlpatterns = [
    path('', index_page.as_view(), name='index_page'),
    path('product_detail/<str:unique_id>/',ProductDetail.as_view(),name='product_detail'),
    path('404/',Page404.as_view(),name='404'),
    path('all-products/',all_products.as_view(),name='all-products'),
    path('comment/',CommentView.as_view(),name='comment'),
    path('product-by-category/<name>/',ProductByCategory.as_view(),name='product_by_category'),
    path('serach-product/',product_search,name='search_product')

]

