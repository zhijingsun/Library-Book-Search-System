from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('index/', views.index),
    path('user/profile/<int:user_id>/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('user/mylist/<int:user_id>/', views.mylist, name='mylist'),
    path('delete/<int:user_id>',views.delete_user, name='delete_user'),
    path('book_detail/<int:book_id>/', views.book_detail, name='book_detail'),
    path('edit_profile/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path('change_password/<int:user_id>/', views.change_password, name='change_password'),
    path('add_to_list/', views.add_to_list, name='add_to_list'),
]