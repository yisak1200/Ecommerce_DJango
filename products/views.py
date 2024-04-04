from django.shortcuts import render,redirect
from django.views import View
from .models import *
from carts.models import Cart
from django.contrib.auth.decorators import login_required
from .models import product_category,Comment
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
class index_page(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart_db =Cart.objects.filter(user=request.user).count()
            cart = Cart.objects.filter(user=request.user)[:6]
            product = Product.objects.filter(available=True)[:8]
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
            return render(request, 'product_temp/index.html', context)
        else :
            product = Product.objects.filter(available=True)[:8]
            product_cat =product_category.objects.all()
            product_new = Product.objects.filter(is_new=True)
            context = {'product': product,'product_new':product_new,'product_cat':product_cat}
            return render(request, 'product_temp/index.html', context)
class all_products(View):
    def get(self, request):
        category_counts = []
        product_cat = product_category.objects.all()
        for category in product_cat:
            count = Product.objects.filter(category=category).count()
            category_counts.append({'category_name': category.name, 'product_count': count})
        all_product = Product.objects.filter(available=True)
        
        # Paginate the products
        paginator = Paginator(all_product, 8)
        page_number = request.GET.get('page')
        try:
            all_product = paginator.page(page_number)
        except PageNotAnInteger:
            all_product = paginator.page(1)
        except EmptyPage:
            all_product = paginator.page(paginator.num_pages)
        
        if request.user.is_authenticated:  
            cart = Cart.objects.filter(user=request.user)[:6]
            cart_db = Cart.objects.filter(user=request.user).count()
            context = {
                'all_product': all_product,
                'cart_db': cart_db,
                'product_cat': product_cat,
                'cart': cart,
                'category_counts': category_counts,
            }
            return render(request, 'product_temp/all_products.html', context)
        else:
            context = {
                'all_product': all_product,
                'category_counts': category_counts,
                'product_cat': product_cat,
            }
            return render(request, 'product_temp/all_products.html', context)
class BasePage(View):
    def get(self, request):
        if user.is_authenticated:
            cart = Cart.objects.filter(user=request.user)[:6]
            cart_db =Cart.objects.filter(user=request.user)
            product_cat = product_category.objects.all()
            context = {'product_cat': product_cat,'cart_db':cart_db,'cart':cart}
            return render(request, 'product_temp/base.html', context)
        else :
            product_cat = product_category.objects.all()
            context = {'product_cat': product_cat}
            return render(request, 'product_temp/base.html', context)

class ProductDetail(View):
    def get(self, request, unique_id):
        product_cat = product_category.objects.all()
        product = Product.objects.get(unique_id=unique_id)
        related_products = product.related_products.all()
        context = {'product_cat': product_cat, 'product': product,'related_products':related_products}

        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user)[:6]
            cart_db = Cart.objects.filter(user=request.user).count()
            context.update({'cart_db': cart_db, 'cart': cart,'related_products':related_products})

        return render(request, 'product_temp/product_detail.html', context)

class Page404(View):
    def get(self,request):
         return render(request,'Base404/base404.html')   
    
def custom_404(request, exception):
        cart = Cart.objects.filter(user=request.user)[:6]
        cart_db =Cart.objects.filter(user=request.user).count()
        product_cat = product_category.objects.all()
        context = {'cart':cart,'cart_db':cart_db,'product_cat':product_cat}
        return render(request, 'Base404/404.html',context, status=404)          
class CommentView(View):
    def post(self, request):
        comment_text = request.POST.get('comment')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')

        if request.user.is_authenticated:
            new_comment = Comment(user=request.user, content=comment_text)
        else:
            new_comment = Comment(full_name=full_name, email=email, content=comment_text)

        new_comment.save() 

        return redirect('index_page')        
    
class ProductByCategory(View):
    def get(self,request,name):
        category_counts = []
        product_cat = product_category.objects.all()
        for category in product_cat:
            count = Product.objects.filter(category=category).count()
            category_counts.append({'category_name': category.name, 'product_count': count})

        category_by_name = product_category.objects.get(name = name)
        all_products = Product.objects.filter(available=True, category=category_by_name)

        paginator = Paginator(all_products, 8)
        page_number = request.GET.get('page')
        try:
            all_products = paginator.page(page_number)
        except PageNotAnInteger:
            all_products = paginator.page(1)
        except EmptyPage:
            all_products = paginator.page(paginator.num_pages)

        cart_db = 0
        cart = []
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user)[:6]
            cart_db = Cart.objects.filter(user=request.user).count()

        context = {
            'all_products': all_products,
            'cart_db': cart_db,
            'product_cat': product_cat,
            'cart': cart,
            'category_counts': category_counts,
        }
        return render(request, 'product_temp/products_by_category.html', context)   

def product_search(request):
    query = request.GET.get('q')
    product_cat = product_category.objects.all()
    
    if query:
        all_product = Product.objects.filter(brand_name__icontains=query, available=True) | \
                      Product.objects.filter(category__name__icontains=query, available=True)
        
        if request.user.is_authenticated:
            cart_db = Cart.objects.filter(user=request.user).count()
        else:
            cart_db = 0
        
        context = {
            'all_product': all_product,
            'product_cat': product_cat,
            'cart_db': cart_db,
        }
        return render(request, 'product_temp/all_products.html', context)
