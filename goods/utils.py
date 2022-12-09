from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect, render
from .models import Category, Product, Tag, OrderProduct, OrderCard
from django.db.models import Q
import requests
from userprofile.forms import OrderProductForm
from userprofile.views import _get_session_id


def paginate_categories(request, categories, results):
    page = request.GET.get('page')

    paginator = Paginator(categories, results)
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        categories = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        categories = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)
    return custom_range, categories


def paginate_products(request, products, results):
    page = request.GET.get('page')

    paginator = Paginator(products, results)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        products = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        products = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)
    return custom_range, products


def search_product(request):
    search_query = ''
    products = []

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        tags = Tag.objects.filter(name__icontains=search_query)

        products = Product.objects.distinct().filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__in=tags)
        )
    print('search: ', products)

    return products, search_query


def nova_poshta_cities(request):
    context_city = {
        "apiKey": "579264d060d2b873b95848224f6b1122",
        "modelName": "Address",
        "calledMethod": "getCities",
        "methodProperties": {
            "Page": "1",
            "Limit": "50000"
        }
    }
    result = requests.post('https://api.novaposhta.ua/v2.0/json/', json=context_city).json()
    data = (result['data'])
    print("DATA: ", data)
    city_list = []
    for x in data:
        city_list.append(x['Description'])

    return city_list


def nova_poshta_posts(request, city):
    context_posts = {
        "apiKey": "579264d060d2b873b95848224f6b1122",
        "modelName": "Address",
        "calledMethod": "getWarehouses",
        "methodProperties": {
            "CityName": city
        }
    }
    resp = requests.post('https://api.novaposhta.ua/v2.0/json/', json=context_posts).json()
    posts = (resp['data'])
    posts_list = []
    for x in posts:
        posts_list.append(x['Description'])

    return posts_list


def create_order_product(request, user_profile, profile_id, product_article):
    form = OrderProductForm(request.POST)
    if form.is_valid() and request.user.is_authenticated:
        order_product = OrderProduct(
            client=user_profile,
            product_id=product_article,
            count=form.cleaned_data['count'],
            status='PROCESSING',
        )
        order_product.save()
    else:
        try:
            card = OrderCard.objects.get(session_id=request.session.session_key)
        except OrderCard.DoesNotExist:
            card = OrderCard.objects.create(
                session_id=_get_session_id(request)
            )

        order_product = OrderProduct(
            session_id=OrderCard.objects.get(session_id=request.session.session_key),
            product_id=product_article,
            count=form.cleaned_data['count'],
            status='PROCESSING',
        )
        order_product.save()
        return False
    return True
