from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name="home"),
    path('login',views.login_first,name="login"),
    path('logout',views.logout_user,name="logout_user"),
    path('register_user',views.register_user,name="register_user"),
    path('login_user',views.login_user,name="login_user"),
    path('user_home',views.user_home,name="user_home"),
    path('profile',views.profile,name="profile"),
    path('add_station',views.add_station,name="add_station"),
    path('admin_home',views.admin_home,name="admin_home"),
    path('add_train',views.add_train,name="add_train"),
    path('view_station',views.view_station,name="view_station"),
    path('view_train',views.view_train,name="view_train"),
    path('add_route',views.add_route,name="add_route"),
    path('search_train',views.search_train,name="search_train"),
    path('book_ticket/<str:trainname>/<str:fare>/<str:source>/<str:destination>/<str:date>/', views.book_ticket, name='book_ticket'),
    path('booking_history',views.booking_history,name="booking_history"),
    path('download/<int:id>/', views.download_ticket, name='download_ticket'),
    path('cancel/<int:id>/', views.cancel_ticket, name='cancel_ticket'),
    path('edit_profile',views.edit_profile,name='edit_profile'),

]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)