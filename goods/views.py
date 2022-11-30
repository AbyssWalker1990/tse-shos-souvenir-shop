import json

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Product, Category, OrderProduct, OrderCard
from userprofile.models import User, Profile
from userprofile.forms import OrderProductForm
from .utils import paginate_categories, search_product, paginate_products, nova_poshta_cities, nova_poshta_posts, \
    create_order_product
from .signals import delete_bucket_item
from userprofile.views import _get_session_id
from .forms import CategoryForm
import copy


# Create your views here.

# View for main page
def goods(request):
    products = Product.objects.all()
    # products = products[0:3]
    print(products)
    context = {'products': products}
    return render(request, 'goods/goods.html', context)


def goods_article(request, pk):
    profile_id = None

    product_article = Product.objects.get(id=pk)
    featured_products = Product.objects.all().filter(
        prod_category=product_article.prod_category)
    form = OrderProductForm()
    context = {
        'product_article': product_article,
        'form': form,
        'featured_products': featured_products,
    }
    # Create session for anonymous user
    if not request.session or not request.session.session_key:
        request.session.save()

    if request.user.is_authenticated:
        user_profile = request.user.profile
        profile_id = user_profile.id
    else:
        user_profile = None
        profile_id = None
    """create_order_products will return True if user is authenticated"""
    if request.method == 'POST':
        if create_order_product(request, user_profile, profile_id, product_article):
            return redirect('bucket', profile_id)
        else:
            return redirect('non-user-bucket')

    return render(request, 'goods/goods_article.html', context)


# View for ALL categories
def categories(request):
    goods_category = Category.objects.all()
    custom_range, categories = paginate_categories(request, goods_category, 3)

    context = {
        'categories': categories,
        'custom_range': custom_range,
    }
    return render(request, 'goods/categories.html', context)


# View for all products for ONE category
def product_category(request, pk):
    category_id = Category.objects.get(id=pk)
    products = Product.objects.all().filter(prod_category=category_id)
    custom_range = ""

    if request.method == "POST":
        if request.POST.get('high') == 'high':
            products = products.order_by('-price')
        if request.POST.get('low') == 'low':
            products = products.order_by('price')
            print('low')
        if request.POST.get('new') == 'new':
            products = products.order_by('-created')
            print('new')
    else:
        custom_range, products = paginate_products(request, products, 12)

    if request.method == "GET":
        print(request.GET.get('page'))

    context = {
        'products': products,
        'custom_range': custom_range,
        'category_id': category_id
    }

    return render(request, 'goods/product_category.html', context)


def create_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            if len(request.FILES) != 0:
                form.featured_img = request.FILES['featured_img']
            form.save()
            return redirect('categories')

    context = {'form': form, 'category': None}
    return render(request, 'goods/category-form.html', context)


def search_goods(request):
    products, search_query = search_product(request)
    print('Products: ', products)
    print(search_query)
    custom_range, products = paginate_products(request, products, 500)
    context = {'products': products, 'search_query': search_query, 'custom_range': custom_range, }
    return render(request, 'goods/search_page_goods.html', context)


def about(request):
    return render(request, 'about_us.html')


def contacts(request):
    return render(request, 'contacts.html')


def get_mail_posts(request):
    post_list = []
    if request.method == "POST":
        raw_data = json.loads(request.body)
        city = raw_data.get('city')
        posts_list = nova_poshta_posts(request, city=city)
    return JsonResponse(posts_list, safe=False)


def goods_processing(request):
    profile = {}
    city = ""
    messages = []
    if request.user.is_authenticated:
        profile = request.user.profile
    posts_list = []
    total_sum = 0
    city_list = nova_poshta_cities(request)

    if request.POST.get('posts') != None:
        if request.POST.get('phone') == "":
            messages.append("Введіть номер телефону")
        if request.POST.get('name') == "":
            messages.append("Введіть ім'я")
        if request.POST.get('surname') == "":
            messages.append("Введіть прізвище")
        if request.POST.get('father_name') == "":
            messages.append("Вкажіть по батькові")

        if messages:
            return render(request, 'goods_processing.html', {'messages': messages,
                                                             'city_list': city_list,
                                                             'posts_list': posts_list,
                                                             'profile': profile,
                                                             'city': city,
                                                             })

        else:
            if request.user.is_authenticated:
                order_products = OrderProduct.objects.all().filter(client=profile, status="PROCESSING")
            else:
                order_card = OrderCard.objects.get(session_id=request.session.session_key)
                print("CARD: ", order_card)
                order_products = OrderProduct.objects.all().filter(session_id=order_card)
                print(order_products)
            total_sum = 0
            for i in order_products:
                total_sum += i.total_price

            # city = request.POST.get('selected-city')
            if request.user.is_authenticated:
                order_card = OrderCard(
                    client=profile,
                    city=request.POST.get('selected-city'),
                    mail_post=request.POST.get('posts'),
                    name=request.POST.get('name'),
                    surname=request.POST.get('surname'),
                    father_name=request.POST.get('father_name'),
                    phone_number=request.POST.get('phone'),
                    email=request.POST.get('email'),
                    total=total_sum
                )
                order_card.save()
                for order in order_products:
                    order_card.goods.add(order)
                return redirect('order_success')
            else:
                order_card.city = request.POST.get('selected-city')
                order_card.mail_post = request.POST.get('posts')
                order_card.name = request.POST.get('name')
                order_card.surname = request.POST.get('surname')
                order_card.father_name = request.POST.get('father_name')
                order_card.phone_number = request.POST.get('phone')
                order_card.email = request.POST.get('email')
                order_card.total = total_sum
                order_card.save()
                for order in order_products:
                    order_card.goods.add(order)
                    print(order)
                order_card.save()
                return redirect('order_success')

    context = {'city_list': city_list,
               'posts_list': posts_list,
               'profile': profile,
               'city': city,
               'messages': messages,
               'total': total_sum
               }

    return render(request, 'goods_processing.html', context)


def order_success(request):
    return render(request, 'order_success.html')


def orders_management(request):
    cards = OrderCard.objects.all()

    if request.method == 'POST':
        changes = request.POST.get('status')
        card_id = request.POST.get('order_id')
        card = OrderCard.objects.get(id=card_id)
        card.status = changes
        card.save()

    context = {'cards': cards}
    return render(request, 'orders_management.html', context)


def user_order(request, pk):
    card = OrderCard.objects.get(id=pk)
    context = {'card': card}
    return render(request, 'user_order.html', context)
