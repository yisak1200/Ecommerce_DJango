from django.shortcuts import render,redirect
from django.views import View
from products.models import Product
from .models import Order
import random
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from carts.models import Cart
from products.models import product_category
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from .models import Order,OrderItem
import requests
class order_view(View):
    @method_decorator(login_required)
    def get(self, request, unique_id):
        cart_db =Cart.objects.filter(user=request.user).count()
        # print('-------------------------------------',cart_db)
        cart = Cart.objects.filter(user=request.user)[:6]
        product = Product.objects.get(unique_id = unique_id)
        product_cat =product_category.objects.all()
        product_new = Product.objects.filter(is_new=True)
        cart_item = Cart.objects.filter(user = request.user)
        def sum_total_amount_in_cart(cart_item):
            total_sum = 0
            for cart_amount in cart_item:
                total_sum += cart_amount.total_price
            return total_sum

        total_amount = sum_total_amount_in_cart(cart_item)
        context = {'product': product,'cart_db':cart_db,'product_new':product_new,'product_cat':product_cat,'cart':cart,'total_amount':total_amount}
        return render(request, 'orders_temp/order_item.html', context)
    

    @method_decorator(login_required)
    def post(self, request, unique_id):
        cart_db = Cart.objects.filter().count()
        amount = request.POST.get('amount')
        address = request.POST.get('address')
        random_number = random.randint(10000, 99999)

        product = get_object_or_404(Product, unique_id=unique_id)
        existing_order = Order.objects.filter(
        user=request.user, order_status='processing').first()
        order_item_fillter = OrderItem.objects.filter(order=existing_order,product=product).first()
        if int(amount) <= 0 :
            message_error = "Amount should be greater than 0"
            context = {'message_error': message_error, 'cart_db': cart_db,'product':product}
            return render(request, 'orders_temp/order_item.html', context)
        if not address:
            message_error = "Address is Required"
            context = {'message_error': message_error, 'cart_db': cart_db,'product':product}
            return render(request, 'orders_temp/order_item.html', context)
        if  order_item_fillter:
            message_error = "This item is already ordered. Please wait until you receive a response. Call and contact Customer Service +251911606654"
            context = {'message_error': message_error, 'cart_db': cart_db}
            return render(request, 'orders_temp/order_done.html', context)
        else:
            total = int(amount) * int(product.price)
            random_num = str(random_number)
            order = Order( user=request.user,
                      shipping_address=address, order_status='processing', order_number=random_number, total_price=total)
            order_item = OrderItem(order = order,product=product,quantity=amount,price = product.price)
            user_email = request.user.email
            current_date = timezone.now().date()
            formatted_date = current_date.strftime('%d-%m-%Y')
            order.save()
            order_item.save()
            send_mail_for_order(user_email,random_num,formatted_date,order_item.product.brand_name,order_item.quantity,order.total_price)
            message_succ = "Order confirmed!  Watch Your Email for Deatil Information"
            context = {'message_succ': message_succ, 'cart_db': cart_db}
            return render(request, 'orders_temp/order_done.html', context)

class order_done(View):
    @method_decorator(login_required)
    def get(self, request):
        cart_db =Cart.objects.filter().count()
        cart_item = Cart.objects.filter(user = request.user)
        def sum_total_amount_in_cart(cart_item):
            total_sum = 0
            for cart_amount in cart_item:
                total_sum += cart_amount.total_price
            return total_sum

        total_amount = sum_total_amount_in_cart(cart_item)
        context = {'cart_db':cart_db,'total_amount':total_amount}
        return render(request, 'orders_temp/order_done.html',context)
    
def send_mail_for_order(email,order_number,order_date,product,amount,total_price):
    subject = 'Your Order Confirmation'   
    message = f"Thank you for choosing E-GEBEYA! We're excited to inform you that your order has been successfully accepted. Below are the details of your order\n\n" \
    f"Order Number: {order_number}\n" \
    f"Date: {order_date}\n" \
    f"Product name: {product}\n" \
    f"Total Price: {total_price} birr\n" \
    f"Amount: {amount}\n\n" \
    f"If you have any questions or concerns, please don't hesitate to contact our customer support.\n\n" \
    "phone number: +251911606654\n\n" 
    message_for_telegram = (
              f"New order Alert:\n" +
              f"Order Number: {order_number}\n" +
              f"Date: {order_date}\n" +
              f"Product names: {product}\n" +
              f"Quantities: {amount}\n" +
              f"Total Price: {total_price} birr\n"
    )
    base_url ='https://api.telegram.org/bot6637520265:AAEPx6_EN4-K8y4gl_78H-RgCpmFicpqx1c/sendMessage?chat_id=-4197103320&text="{}" '.format(message_for_telegram)
    requests.get(base_url)
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_form, recipient_list)                    
    
class OrderStatus(View):
    @method_decorator(login_required)
    def get(self,request):
        cart = Cart.objects.filter(user=request.user)[:6]
        product_cat =product_category.objects.all()
        cart_db =Cart.objects.filter(user = request.user).count()
        cart_item = Cart.objects.filter(user = request.user)
        def sum_total_amount_in_cart(cart_item):
            total_sum = 0
            for cart_amount in cart_item:
                total_sum += cart_amount.total_price
            return total_sum

        total_amount = sum_total_amount_in_cart(cart_item)
        context = {'cart_item':cart_item,'cart_db':cart_db,'product_cat':product_cat,'cart':cart,'total_amount':total_amount}
        return render(request,'orders_temp/order_status.html',context)
    @method_decorator(login_required)
    def post(self,request):
        order_num = request.POST.get('order_num')
        order_selection = Order.objects.filter(order_number=order_num,user=request.user).first()
    
        if order_selection:
            user_order_number = Order.objects.get(order_number = order_num,user=request.user )
            cart = Cart.objects.filter(user=request.user)[:6]
            product_cat =product_category.objects.all()
            cart_db =Cart.objects.filter(user = request.user).count()
            cart_item = Cart.objects.filter(user = request.user)
            # context = {'cart_item':cart_item,'cart_db':cart_db,'product_cat':product_cat,'cart':cart,pk}
            return redirect('order_detail',unique_id=user_order_number.unique_id)
        else:
            cart = Cart.objects.filter(user=request.user)[:6]
            product_cat =product_category.objects.all()
            cart_db =Cart.objects.filter(user = request.user).count()
            cart_item = Cart.objects.filter(user = request.user)
            def sum_total_amount_in_cart(cart_item):
                total_sum = 0
                for cart_amount in cart_item:
                    total_sum += cart_amount.total_price
                return total_sum

            total_amount = sum_total_amount_in_cart(cart_item)
            message_error = "Wrong Order Number" 
            context = {'cart_item':cart_item,'cart_db':cart_db,'product_cat':product_cat,'cart':cart,'message_error':message_error,'total_amount':total_amount}
            return render(request,'orders_temp/order_status.html',context)
     
class OrderDetail(View):
    @method_decorator(login_required)
    def get(self,request,unique_id):
        user_detail_order=get_object_or_404(Order,unique_id=unique_id)
        order_status = user_detail_order.order_status
        shipping_method = user_detail_order.shipping_method
        order_item = OrderItem.objects.filter(order= user_detail_order)
        order_item_count = OrderItem.objects.filter(order= user_detail_order).count()
        cart = Cart.objects.filter(user=request.user)[:6]
        product_cat =product_category.objects.all()
        cart_db =Cart.objects.filter(user = request.user).count()

        def sum_total_amount_in_order(order_item):
            total_sum = 0
            for order in order_item:
                total_sum += order.price
            return total_sum
        total_amount = sum_total_amount_in_order(order_item)
        context = {'cart_db':cart_db,'product_cat':product_cat,'cart':cart,'user_detail_order':user_detail_order,'total_amount':total_amount,'order_item':order_item,'order_item_count':order_item_count,'order_status':order_status,'shipping_method':shipping_method}
        return render(request,'orders_temp/order_detail.html',context)
                
class OrderHistory(View):
    @method_decorator(login_required)
    def get(self, request):
        # Get the user's cart items
        cart = Cart.objects.filter(user=request.user)[:6]
        product_cat = product_category.objects.all()
        cart_db = Cart.objects.filter(user=request.user).count()
        cart_item = Cart.objects.filter(user=request.user)
        def sum_total_amount_in_cart(cart_item):
            total_sum = 0
            for cart_amount in cart_item:
                total_sum += cart_amount.total_price
            return total_sum
        orders = Order.objects.filter(user=request.user)
        order_items = []
        for order in orders:
            order_items.extend(OrderItem.objects.filter(order=order))
        total_amount = sum_total_amount_in_cart(cart_item)
        context = {
            'cart_item': cart_item,
            'cart_db': cart_db,
            'product_cat': product_cat,
            'cart': cart,
            'total_amount': total_amount,
            'order_items': order_items
        }
        return render(request, 'orders_temp/order_history.html', context)