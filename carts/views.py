from django.shortcuts import render,redirect
from django.views import View
from products.models import Product
from carts.models import Cart
from django.contrib.auth.models import User
from products.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from orders.models import Order,OrderItem
from django.core.mail import send_mail
from django.conf import settings
import random
from django.utils import timezone
from django.contrib import messages
import requests
class AddToCart(View):
    @method_decorator(login_required)
    def get(self, request, unique_id):
        product_cat = product_category.objects.all()
        product = Product.objects.get(unique_id=unique_id)
        context = {'product': product, 'product_cat': product_cat}
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user)[:6]
            cart_item = Cart.objects.filter()
            cart_db = Cart.objects.filter(user=request.user).count()
            context.update({'cart': cart, 'cart_item': cart_item, 'cart_db': cart_db})
        return render(request, 'cart_temp/add_to_cart.html', context)
    @method_decorator(login_required)
    def post(self, request, unique_id):
        product = Product.objects.get(unique_id=unique_id)
        product_cat = product_category.objects.all()
        amount = request.POST.get('amount')  
        product_price = product.price
        total = int(amount) * product_price  
        cart_filter = Cart.objects.filter(user=request.user, product=product).count()
        cart_item = Cart.objects.filter(user = request.user)
        def sum_total_amount_in_cart(cart_item):
            total_sum = 0
            for cart_amount in cart_item:
                total_sum += cart_amount.total_price
            return total_sum
        total_amount = sum_total_amount_in_cart(cart_item)
        if int(amount) <= 0 :
            message_error = "The Amount should be greater than Zero"
            cart = Cart.objects.filter(user=request.user)[:6]
            all_my_cart = Cart.objects.filter(user=request.user)
            cart_db = Cart.objects.filter(user=request.user).count()
            context = {'cart': cart, 'all_my_cart': all_my_cart, 'cart_db': cart_db,
                       'product_cat': product_cat, 'message_error': message_error,'total_amount':total_amount,'product':product}
            return render(request, 'cart_temp/add_to_cart.html', context)
        if cart_filter == 1:
            message_error = "This item is already in your cart"
            cart = Cart.objects.filter(user=request.user)[:6]
            all_my_cart = Cart.objects.filter(user=request.user)
            cart_db = Cart.objects.filter(user=request.user).count()
            context = {'cart': cart, 'all_my_cart': all_my_cart, 'cart_db': cart_db,
                       'product_cat': product_cat, 'message_error': message_error,'total_amount':total_amount}
            return render(request, 'cart_temp/my_cart.html', context)
        
        else:
            cart_save = Cart.objects.create(product=product, user=request.user, amount=amount, total_price=total)
            cart_save.save()
            message_succ = 'Added to cart'
            cart = Cart.objects.filter(user=request.user)[:6]
            cart_db = Cart.objects.filter(user=request.user).count()
            product_new = Product.objects.filter(is_new=True)
            product = Product.objects.filter(available=True)[:8]
            cart_item = Cart.objects.filter()
            context = {'message_succ': message_succ, 'cart': cart, 'cart_db': cart_db,
                       'product_cat': product_cat, 'cart_item': cart_item, 'product_new': product_new,
                       'product': product,'total_amount':total_amount}
            return render(request, 'product_temp/index.html', context)
class view_cart(View):
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
        print(total_amount)
        context = {'cart_item':cart_item,'cart_db':cart_db,'product_cat':product_cat,'cart':cart,'total_amount':total_amount}
        return render(request,'cart_temp/cart_items.html',context)

class Remove_cart(View):
    @method_decorator(login_required)
    def get(self,request,unique_id):
        my_cart = Cart.objects.get(unique_id=unique_id)
        cart_db =Cart.objects.filter(user = request.user).count()
        all_my_cart = Cart.objects.filter(user = request.user)
        def sum_total_amount_in_cart(cart_total_amounts):
            total_sum = 0
            for cart_amount in cart_total_amounts:
                total_sum += cart_amount.total_price
            return total_sum
        total_amount = sum_total_amount_in_cart(all_my_cart)
        context = {'all_my_cart':all_my_cart,'cart_db':cart_db,'total_amount':total_amount}
        return render(request,'cart_temp/delete_cart.html',context)
    @method_decorator(login_required)
    def post(self,request,unique_id):
        my_cart = Cart.objects.get(unique_id=unique_id)
        my_cart.delete()
        return redirect('my_cart')


class MyCart(View):
    @method_decorator(login_required)
    def get(self, request):
        product_cat = product_category.objects.all()
        cart = Cart.objects.filter(user=request.user)[:6]
        all_my_cart = Cart.objects.filter(user=request.user)
        cart_db = Cart.objects.filter(user=request.user).count()
        cart_total_amounts = Cart.objects.filter(user=request.user)
        def sum_total_amount_in_cart(cart_total_amounts):
            total_sum = 0
            for cart_amount in cart_total_amounts:
                total_sum += cart_amount.total_price
            return total_sum
        total_amount = sum_total_amount_in_cart(cart_total_amounts)
        print(total_amount)  
        context = {
            'cart_db': cart_db,
            'cart': cart,
            'all_my_cart': all_my_cart,
            'product_cat': product_cat,
            'total_amount': total_amount,
        }

        return render(request, 'cart_temp/my_cart.html', context)   
  
  
class Update_cart(View):
    @method_decorator(login_required)
    def get(self,request,unique_id):
        product_cat = product_category.objects.all()
        cart_db =Cart.objects.filter(user = request.user).count()
        cart = Cart.objects.filter(user=request.user)[:6]
        my_cart = Cart.objects.get(unique_id=unique_id)
        context = {'my_cart':my_cart,'cart':cart,'cart_db':cart_db,'product_cat':product_cat}  
        return render(request,'cart_temp/update_cart.html',context)
    def post(self,request,unique_id):
        amount = request.POST.get('amount')
        product_cat = product_category.objects.all() 
        if int(amount) <= 0 :
            message_error = "The Amount should be greater than Zero"
            my_cart = Cart.objects.get(unique_id=unique_id)
            cart = Cart.objects.filter(user=request.user)[:6]
            all_my_cart = Cart.objects.filter(user=request.user)
            cart_db = Cart.objects.filter(user=request.user).count()
            context = {'cart': cart, 'all_my_cart': all_my_cart, 'cart_db': cart_db,
                       'product_cat': product_cat, 'message_error': message_error,'my_cart':my_cart}
            return render(request, 'cart_temp/update_cart.html', context)
        product_cat = product_category.objects.all()
        my_cart = Cart.objects.get(unique_id=unique_id)
        my_cart.amount = request.POST['amount']
        total_price_updated = int(my_cart.amount) * int(my_cart.product.price)
        my_cart.total_price = total_price_updated
        my_cart.save()
        return redirect('my_cart')

import datetime

class OrderItemFromCart(View):
    def post(self, request):
        shipping_address = request.POST.get('shipping_address')
        if not shipping_address:
            messages.error(request, 'Shipping address cannot be empty.')
            return redirect('my_cart')

        cart_items = Cart.objects.filter(user=request.user)
        cart_db = Cart.objects.filter(user=request.user).count()
        total_amount = sum(item.total_price for item in cart_items)
        random_number = random.randint(10000, 99999)

        new_order = Order.objects.create(
            shipping_address=shipping_address,
            user=request.user,
            order_status='processing',
            order_number=random_number,
            total_price=total_amount
        )

        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=new_order,
                product=cart_item.product,
                quantity=cart_item.amount,
                price=cart_item.total_price
            )
        user_email = request.user.email
        cart_items.delete()
        order_items = OrderItem.objects.filter(order=new_order)
        order_date_str = new_order.order_date.strftime('%B %d, %Y')
        order_item_count = OrderItem.objects.filter(order= new_order).count()
        send_mail_for_order(user_email, new_order.order_number, order_date_str, order_items,order_item_count, new_order.total_price)
        message_succ = "Order confirmed! Watch your email for detailed information."
        context = {'message_succ': message_succ, 'cart_db': cart_db, 'total_amount': total_amount}
        return render(request, 'orders_temp/order_done.html', context)


def send_mail_for_order(email, order_number, order_date, order_items, order_item_count, total_price):
    subject = 'Your Order Confirmation'
    product_names = [order_item.product.brand_name for order_item in order_items]
    product_amount = [order_item.quantity for order_item in order_items]
    product_names_str = ', '.join(f'{name} ({amount})' for name, amount in zip(product_names, product_amount))

    message = f"Thank you for choosing E-GEBEYA! We're excited to inform you that your order has been successfully accepted. Below are the details of your order\n\n" \
              f"Order Number: {order_number}\n" \
              f"Date: {order_date}\n" \
              f"Product names: {product_names_str}\n" \
              f"Quantities: {order_item_count}\n" \
              f"Total Price: {total_price} birr\n\n" \
              f"If you have any questions or concerns, please don't hesitate to contact our customer support.\n\n" \
              "phone number: +251912007665\n\n"
              
    message_for_telegram = f"New order Alert:\n\n" \
              f"Order Number: {order_number}\n" \
              f"Date: {order_date}\n" \
              f"Product names: {product_names_str}\n" \
              f"Quantities: {order_item_count}\n" \
              f"Total Price: {total_price} birr\n\n"
              
    base_url ='https://api.telegram.org/bot6637520265:AAEPx6_EN4-K8y4gl_78H-RgCpmFicpqx1c/sendMessage?chat_id=-4197103320&text="{}" '.format(message_for_telegram)
    requests.get(base_url)
    
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_form, recipient_list)


