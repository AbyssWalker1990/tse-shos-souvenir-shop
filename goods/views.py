from django.shortcuts import render, redirect
from .models import Product, Category, OrderProduct, OrderCard
from userprofile.models import User, Profile
from userprofile.forms import OrderProductForm
from .utils import paginateProjects, search_product, paginateProducts, nova_poshta_cities, nova_poshta_posts
from .signals import delete_bucket_item
import copy


# Create your views here.

# View for main page
def goods(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'goods/goods.html', context)


# View for one item
def goods_article(request, pk):
    product_article = Product.objects.get(id=pk)
    featured_products = Product.objects.all().filter(
        prod_category=product_article.prod_category)
    user_profile = request.user.profile
    profile_id = user_profile.id
    form = OrderProductForm()

    if request.method == 'POST':
        form = OrderProductForm(request.POST)
        if form.is_valid():
            order_product = OrderProduct(
                client=user_profile,
                product_id=product_article,
                count=form.cleaned_data['count'],
                status='PROCESSING',
            )
            order_product.save()
        return redirect('bucket', profile_id)

    context = {
        'product_article': product_article,
        'form': form,
        'featured_products': featured_products,
    }

    return render(request, 'goods/goods_article.html', context)


# View for ALL categories
def categories(request):
    goods_category = Category.objects.all()
    custom_range, categories = paginateProjects(request, goods_category, 3)

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
        custom_range, products = paginateProducts(request, products, 20)

    if request.method == "GET":
        print(request.GET.get('page'))

    context = {
        'products': products,
        'custom_range': custom_range,
        'category_id': category_id
    }

    return render(request, 'goods/product_category.html', context)


def search_goods(request):
    products, search_query = search_product(request)
    print('Products: ', products)
    print(search_query)
    custom_range, products = paginateProducts(request, products, 500)
    context = {'products': products, 'search_query': search_query, 'custom_range': custom_range, }
    return render(request, 'goods/search_page_goods.html', context)


def about(request):
    return render(request, 'about_us.html')


def contacts(request):
    return render(request, 'contacts.html')


def goods_processing(request):
    profile = {}
    city = ""
    messages = []
    if request.user.is_authenticated:
        profile = request.user.profile
    posts_list = []
    city_list = nova_poshta_cities(request)

    if request.method == 'POST' and city == "":
        city = request.POST.get('city')

        posts_list = nova_poshta_posts(request, city=city)
        old_city = copy.copy(city)

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
            order_products = OrderProduct.objects.all().filter(client=profile, status="PROCESSING")
            total_sum = 0
            for i in order_products:
                total_sum += i.total_price

            city = request.POST.get('selected-city')
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

    context = {'city_list': city_list,
               'posts_list': posts_list,
               'profile': profile,
               'city': city,
               'messages': messages,
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
