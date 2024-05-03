from django.contrib import admin
from django.urls import path, include
# from auth_clicker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('auth_clicker.urls'))
]