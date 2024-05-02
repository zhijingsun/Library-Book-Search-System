from django.urls import path

from . import views

# urlpatterns = [
#     path('', views.run_query),
# ]

    
#app_name = 'admin'
urlpatterns = [
    path('adminlogin/', views.admin_login, name='admin_login'),
    path('book_management/', views.book_management, name='book_management'),
    path('user_management/', views.user_management, name='user_management'),
    path('result/', views.execute_query, name='execute_query'),
    path('execute_user_query/', views.execute_user_query, name='execute_user_query'),
]