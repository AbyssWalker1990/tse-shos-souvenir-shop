from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    path('user/<str:pk>/', views.profile, name="profile"),
    path('edit_account/<str:pk>', views.edit_account, name="edit_account"),
    path('bucket/<str:pk>', views.bucket, name="bucket"),
    path('delete_item/<str:pk>', views.delete_item, name="delete_item"),
    path('increase_item/<str:pk>', views.increase_item, name="increase_item"),
    path('decrease_item/<str:pk>', views.decrease_item, name="decrease_item"),
    path('non-user-bucket/', views.non_user_bucket, name="non-user-bucket"),
    path('increase-item-non-user/<str:pk>', views.increase_item_non_user, name="increase-item-non-user"),
    path('decrease-item-non-user/<str:pk>', views.decrease_item_non_user, name="decrease-item-non-user"),
    path('delete-item-non-user/<str:pk>', views.delete_item_non_user, name="delete-item-non-user"),
    path('check-bucket/', views.check_bucket, name="check-bucket"),
    # path('goods_article/<str:pk>/', views.goods_article, name="goods_article")
]