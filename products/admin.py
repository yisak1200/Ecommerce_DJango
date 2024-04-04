from django.contrib import admin
from .models import Product, product_category,Wishlist,Comment

class ProductAdmin(admin.ModelAdmin):
    list_display = ('brand_name','price', 'stock_quantity',
                    'created_date','unique_id',)
    search_fields = ['brand_name',]


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ['name',]

class CommentAdmin(admin.ModelAdmin):
    list_display=('user','full_name','content','timestamp')
    search_fields = ['full_name',]
    readonly_fields = ['user','full_name','content','timestamp','email']
admin.site.register(Product, ProductAdmin)
admin.site.register(product_category, ProductCategoryAdmin)
admin.site.register(Comment,CommentAdmin)