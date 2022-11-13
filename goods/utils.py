from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Category, Product, Tag
from django.db.models import Q
import requests


def paginateProjects(request, categories, results):
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


def paginateProducts(request, products, results):
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

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)

    products = Product.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(tags__in=tags)
    )

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
    result = requests.get('https://api.novaposhta.ua/v2.0/json/', json=context_city).json()
    data = (result['data'])
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
    resp = requests.get('https://api.novaposhta.ua/v2.0/json/', json=context_posts).json()
    posts = (resp['data'])
    posts_list = []
    for x in posts:
        posts_list.append(x['Description'])

    return posts_list
