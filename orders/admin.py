from django.contrib import admin
from .models import Order,OrderItem
from django.contrib import admin

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user','get_user_first_name', 'get_user_last_name','order_date',
                    'order_status', 'total_price','get_user_phone_number')
    readonly_fields=('order_number','user','order_date')
    def get_user_phone_number(self, obj):
        return obj.user.user_profile.user_phone_number
    def get_user_first_name(self,obj):
        return obj.user.first_name
    def get_user_last_name(self,obj):
        return obj.user.last_name
    get_user_phone_number.short_description = 'User Phone Number'
    get_user_first_name.short_description = 'First Name'
    get_user_last_name.short_description = 'Last Name'
    search_fields = ['order_number']

    list_filter = ('order_status',)
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj and obj.order_status == 'delivered':
            readonly_fields += ('order_status',)
        return readonly_fields
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(order_status__in=['processing', 'shipped', 'delivered', 'cancelled'])

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_order_number', 'product_brand_name', 'price', 'quantity')
    search_fields = ('order__order_number',) 
    readonly_fields = ('order', 'product', 'price', 'quantity')
    def order_order_number(self, obj):
        return obj.order.order_number

    def product_brand_name(self, obj):
        return obj.product.brand_name

admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
