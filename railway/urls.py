from django.urls import path,include
from . import views
urlpatterns = [
    path('home',views.home,name="home"),
    path('login',views.login,name="login"),
    path('register_user',views.register_user,name="register_user"),
    path('login_user',views.login_user,name="login_user"),
    path('user_home',views.user_home,name="user_home"),
]