# from django.urls import path
# from . import views
#
# urlpatterns = [
#     # path('admin/', admin.site.urls),
#     path('', views.index, name='index'),
#     path('login/', views.user_login, name='login'),
#     path('logout/', views.user_logout()),
#     path('registartion/', views.user_registration(), name='registartion'),
#     path('user/<int:pk>/', views.UserDetail.as_view())
#
# ]

from django.contrib import admin
from django.urls import path
from . import views


# urlpatterns = [
#     # path('admin/', admin.site.urls),
#     path('', views.index, name='index'),
#     path('login/', views.user_login, name='login'),
#     path('logout/', views.user_logout),
#     path('registration/', views.user_registration, name='registration'),
#     path('user/<int:pk>/', views.UserDetail.as_view())
#
# ]

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout),
    path('registration/', views.user_registration, name='registration'),
    path('user/<int:pk>/', views.UserDetail.as_view())

]