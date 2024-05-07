from django.contrib import admin
from django.urls import path, include
from backend import views
# from auth_clicker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('call_click/', views.call_click, name='call_click'),
    path('', include('auth_clicker.urls'))
]