from django.urls import path
from . import views


urlpatterns = [
    path('', views.goods, name="goods"),
    path('goods_article/<str:pk>/', views.goods_article, name="goods_article"),
    path('product_category/<str:pk>/', views.product_category, name="product_category"),
    path('categories/', views.categories, name="categories"),
    path('search_goods/', views.search_goods, name="search_goods"),
    path('about/', views.about, name="about"),
    path('contacts/', views.contacts, name="contacts"),
    path('goods_processing/', views.goods_processing, name="goods_processing"),
    path('order_success/', views.order_success, name="order_success"),
    path('orders_management/', views.orders_management, name="orders_management"),
    path('user_order/<str:pk>/', views.user_order, name="user_order"),

]