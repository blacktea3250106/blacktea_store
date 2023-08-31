from django.shortcuts import render, get_object_or_404
from .forms import RegisterForm, LoginForm, ChangePasswordForm, CommentForm, CartForm, UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Product, Comment, Cart, Color, Capacity
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
import time
import json

# Create your views here.

# def format_price(all_prices):
#     formatted_prices = ["NT$ {:,}".format(price) for price in all_prices]
#     return formatted_prices

def index(request):
    query = request.GET.get('q', '')  # Get the search query from the URL parameter 'q'
    
    products = Product.objects.all()

    # Zip products and prices together

    # Filter products by name if there is a search query
    if query:
        products = [product for product in products if query.lower() in product.name.lower()]

    # Sort products by time
    products = sorted(products, key=lambda product: product.time, reverse=True)


    context = {
        "products": products,
    }

    return render(request, 'store/index.html', context)

# def sign_up(request):
#     return render(request, 'store/register.html')

def sign_up(request):
    forms = RegisterForm()
    if request.method == "POST":
        forms = RegisterForm(request.POST)
        if forms.is_valid():
            forms.save()
            return HttpResponseRedirect(reverse('login'))
    
    context = {
        'forms': forms
    }

    # forms = UserCreationForm()
    # context = {
    #     'forms': forms
    # }
    return render(request, 'store/register.html', context)

def sign_in(request):
    error_message = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        
        if user is not None:
            login(request, user)
            # time.sleep(0.3);
            return HttpResponseRedirect(reverse('index'))
        else:
            error_message = "帳號或密碼錯誤"
    
    forms = LoginForm()
    context = {
        'forms': forms,
        'error_message':error_message
    }
        
    return render(request, 'store/login.html',context)

def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def change_password(request):
    forms = ChangePasswordForm()

    if request.method == "POST":
        forms = ChangePasswordForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data.get("username")
            email = forms.cleaned_data.get("email")
            password1 = forms.cleaned_data.get("password1")
            password2 = forms.cleaned_data.get("password2")
            user = User.objects.filter(username=username, email=email) 
            # 'filter' returns a QuerySet, which is a collection of multiple objects, not a single object.

            if user.exists():
                user = user.first() # which is a collection of multiple objects, not a single object.
                user.set_password(password1)  # change password
                user.save()  # save data
                return HttpResponseRedirect(reverse('login'))
            else:
                # 如果找不到用戶，向username字段添加錯誤訊息
                forms.add_error("username", "帳號或電子郵件錯誤")

    context = {
        'forms': forms,
    }
    
    return render(request, 'store/change_password.html',context)

def product(request, slug):
    product = get_object_or_404(Product, slug=slug)

    contents = product.content.splitlines()
    comments = product.comments.all().order_by("date")

    def capacity_sort_key(capacity_name):
        capacity_order_mapping = {
            '64GB': 1,
            '128GB': 2,
            '256GB': 3,
            '512GB': 4,
            '1TB': 5
        }
        return capacity_order_mapping.get(capacity_name, 6)

    # Sort style_capacity names based on custom sorting function
    sorted_capacities = sorted(product.style_capacity.all(), key=lambda capacity: capacity_sort_key(capacity.name))


    product_name = product.name.split()
    reach_text = product_name[0] + " " + product_name[1]
    products = Product.objects.all()

    # Filter products by name if there is a search query
    related_products = [product for product in products if reach_text.lower() in product.name.lower() and slug != product.slug]
    related_products = sorted(related_products, key=lambda related_product: related_product.time, reverse=True)

    forms = CommentForm()

    context = {
        "product": product,
        "style_capacity":sorted_capacities,
        "contents": contents,
        "comments":comments,
        "forms":forms,
        "related_products":related_products
    }

    return render(request, "store/product.html", context)

def add_comment(request, slug):
    if request.method == "POST":
        product = get_object_or_404(Product, slug=slug)
        forms = CommentForm(request.POST)  # 新增留言表單
        
        if forms.is_valid():
            comment = forms.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(reverse("product", args=[slug]))
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


def edit_comment(request, slug, comment_id):
    if request.method == 'POST':
        try:
            comment = Comment.objects.get(id=comment_id)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse("product", args=[slug])) # 處理留言不存在的情況
        
        forms = CommentForm(request.POST, instance=comment)
        if forms.is_valid():
            forms.save()
        
    # 然後進行頁面重定向或其他處理
    return HttpResponseRedirect(reverse("product", args=[slug]))


def delete_comment(request):
    if request.method == 'DELETE':

        data = json.loads(request.body)
        comment_id = data.get('comment_id')

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Comment does not exist'})

        if comment.user == request.user:
            comment.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Permission denied'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    



def cart(request):
    try:
        user = request.user
        cart_items = Cart.objects.filter(user=user)        
        
        context = {
            'cart_items': cart_items,
        }
        
        return render(request, "store/cart.html", context)
    except:
        return HttpResponseRedirect(reverse('login'))


def update_volume(request):
    if request.method == 'POST':        
        
        data = json.loads(request.body)
        cart_item_id = data.get("cart_item_id")
        volume = data.get("volume")

        try:
            cart_item = Cart.objects.get(id=cart_item_id)
        except Cart.DoesNotExist:
            return JsonResponse({'success': False})
        
        # 更新購物車項目的數量
        cart_item.volume = volume
        cart_item.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

@csrf_exempt
# @login_required 
def add_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        product_name = data.get('product_name')
        product = get_object_or_404(Product, name=product_name)

        color_name = data.get('color')
        capacity_name = data.get('capacity')

        color = get_object_or_404(Color, name=color_name)
        capacity = get_object_or_404(Capacity, name=capacity_name)
        volume = data.get('volume')

        print("volume:",volume,type(volume))

        cart = Cart.objects.create(
            user = request.user,
            product = product,
            volume = volume,
        )
        cart.style_color.add(color)  
        cart.style_capacity.add(capacity) 
        print(cart.volume)
        response_data = {'message': '成功加入購物車'}
        return JsonResponse(response_data)

    return JsonResponse({'message': '無效的請求方式'}, status=400)


def delete_cart_item(request):
    if request.method == 'DELETE':

        data = json.loads(request.body)
        cart_item_id = data.get('cart_item_id')

        try:
            cart_item  = Cart.objects.get(id=cart_item_id)
        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Comment does not exist'})

        if cart_item.user == request.user:  # 確認只能刪除自己的留言
            cart_item.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Permission denied'})

def page_not_found(request,exception):
    return render(request, "store/404.html", status=404)



    




