from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from .models import user_profile
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
import re
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from carts.models import Cart
from products.models import *
from django.contrib.auth import logout
from django.contrib import messages
class register_user(View):
    def get(self, request):
        product_cat =product_category.objects.all()
        context = {'product_cat':product_cat}
        return render(request, 'account/register_user.html',context)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        # username = request.POST.get('username')
        phone_num = request.POST.get('phone_num')
        address = request.POST.get('address')
        # Allows alphabets, hyphens, and single quotes
        name_regex = r"^[A-Za-z\-']+$"
        username_regex = r"^\w+$"  # Allows alphanumeric characters and underscores
        # Validates email addresses
        email_regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"

        user_email_check = User.objects.filter(email=email)
        user_phone_check = user_profile.objects.filter(
            user_phone_number=phone_num)
        product_cat =product_category.objects.all()
        if not re.match(name_regex, first_name):
            message = "Please enter a valid first name using only letters."
            context = {'first_name': first_name, 'last_name': last_name, 'email': email,
                       'password': password, 'confirm_password': confirm_password, 'phone_num': phone_num, 'username': username, 'address': address, 'message': message,'product_cat':product_cat}
            return render(request, 'account/register_user.html', context)
        if not re.match(name_regex, last_name):
            message = "Please enter a valid last name with only letters."
            context = {'first_name': first_name, 'last_name': last_name, 'email': email,
                       'password': password, 'confirm_password': confirm_password, 'phone_num': phone_num, 'username': username, 'address': address, 'message': message,'product_cat':product_cat}
            return render(request, 'account/register_user.html', context)
        if not re.match(email_regex, email):
            message = "Invalid email format. Please enter a valid email address."
            context = {'first_name': first_name, 'last_name': last_name, 'email': email,
                       'password': password, 'confirm_password': confirm_password, 'phone_num': phone_num, 'username': username, 'address': address, 'message': message,'product_cat':product_cat}
            return render(request, 'account/register_user.html', context)
        # if user_check:
        #     message = "Sorry, the chosen username is already in use. Please select a different username."
        #     context = {'first_name': first_name, 'last_name': last_name, 'email': email,
        #                'password': password, 'confirm_password': confirm_password, 'phone_num': phone_num, 'username': username, 'address': address, 'message': message,'product_cat':product_cat}
        #     return render(request, 'account/register_user.html', context)
        if user_email_check:
            message = "This email is already associated with an existing account. Please use a different email address or proceed to log in if this is your account."
            context = {'first_name': first_name, 'last_name': last_name, 'email': email,
                       'password': password, 'confirm_password': confirm_password, 'phone_num': phone_num,  'address': address, 'message': message,'product_cat':product_cat}
            return render(request, 'account/register_user.html', context)
        if user_phone_check:
            message = "The provided phone number is already in use. Please choose a different phone number or log in with the existing one."
            context = {'first_name': first_name, 'last_name': last_name, 'email': email,
                       'password': password, 'confirm_password': confirm_password, 'phone_num': phone_num,  'address': address, 'message': message,'product_cat':product_cat}
            return render(request, 'account/register_user.html', context)
        if password != confirm_password:
            message = "Ensure that the entered passwords match in both 'Password' and 'Confirm Password' fields for verification."
            context = {'first_name': first_name, 'last_name': last_name, 'email': email,
                       'password': password, 'confirm_password': confirm_password, 'phone_num': phone_num,  'address': address, 'message': message,'product_cat':product_cat}
            return render(request, 'account/register_user.html', context)
        if not re.match(r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z]).{8,}$', password):
            message = "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit."
            context = {'first_name': first_name, 'last_name': last_name, 'email': email,
                       'password': password, 'confirm_password': confirm_password, 'phone_num': phone_num, 'address': address, 'message': message,'product_cat':product_cat}
            return render(request, 'account/register_user.html', context)
        user_obj = User.objects.create(
            first_name=first_name, last_name=last_name, username=email, email=email)
        user_obj.set_password(password)
        group = Group.objects.get(name='customer')
        user_obj.groups.add(group)
        user_obj.save()
        token = str(uuid.uuid4())
        user_p = user_profile(
            user=user_obj, user_address=address, user_phone_number=phone_num, email_token=token)
        user_p.save()
        send_mail_for_registraion(email, token)
        message_succ = f"Dear {first_name} {last_name}, please check your email ({email}) to activate your account."
        context = {'message_succ': message_succ,'product_cat':product_cat}
        return render(request, 'account/register_user.html', context)


class login_page(View):
    def get(self, request):
        product_cat =product_category.objects.all()
        context = {'product_cat':product_cat}
        return render(request, 'account/login.html',context)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = authenticate(request, username=username, password=password)
        if user_obj is not None:
            if user_obj.groups.filter(name='customer').exists():
                user_p = user_profile.objects.get(user=user_obj)
                if user_p.is_verified is False:
                    message_error = 'This account is not activated please check your email'
                    context = {'username': username,
                               'message_error': message_error}
                    return render(request, 'account/login.html', context)
                else:
                    login(request, user_obj)
                    return redirect('index_page')
            else:
                message_error = "This user Group can't login in this page"
                return render(request, 'account/login.html', {'message_error': message_error})
        message_error = 'invalid username or password'
        context = {'username': username, 'message_error': message_error}
        return render(request, 'account/login.html', context)


def account_verify(request, email_token):
    user_p = user_profile.objects.filter(email_token=email_token).first()
    if user_p:
        user_p.is_verified = True
        user_p.save()
        messages.success(request, 'User activated successfully') 
        return redirect('login_page')
    else:
        message_error = 'User is not activated successfully'
        return render(request, 'product_temp/index.html', {'message_error': message_error})


def send_mail_for_registraion(email, token):
    subject = 'Your account has been verified'
    message = f'touch this link to verify your account http://192.168.4.151:8000/verify/{token}'
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_form, recipient_list)


class ChangePass(View):
    @method_decorator(login_required)
    def get(self, request):
        product_cat =product_category.objects.all()
        cart_db =Cart.objects.filter(user=request.user).count()
        context = {'cart_db':cart_db,'product_cat':product_cat}
        return render(request, 'account/change_pass.html',context)

    @method_decorator(login_required)
    def post(self, request):
        product_cat =product_category.objects.all()
        cart_db =Cart.objects.filter(user=request.user).count()
        # context = {}
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if request.user.check_password(current_password):
            if not re.match(r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z]).{8,}$', new_password):
                message_error = 'New password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit.'
                context = {'current_password': current_password,
                           'new_password': new_password, 'confirm_password': confirm_password, 'message_error': message_error,'cart_db':cart_db,'product_cat':product_cat}
                return render(request, 'account/change_pass.html', context)
            elif new_password != confirm_password:
                message_error = 'passwords do not match.'
                context = {'current_password': current_password,
                           'new_password': new_password, 'confirm_password': confirm_password, 'message_error': message_error,'cart_db':cart_db,'product_cat':product_cat}
                return render(request, 'account/change_pass.html', context)
            else:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                message_succ = 'password has been changed successfully!'
                return redirect('login_page')
        else:
            message_error = 'Current password is incorrect'
            context = {'current_password': current_password,
                       'new_password': new_password, 'confirm_password': confirm_password, 'message_error': message_error,'cart_db':cart_db,'product_cat':product_cat}
            return render(request, 'account/change_pass.html', context)
        
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login_page')