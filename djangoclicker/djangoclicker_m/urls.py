
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include, reverse_lazy, re_path
from django.views.generic import RedirectView

urlpatterns = [
    path('', include('backend.urls')),
    path('admin/', admin.site.urls),
    path("backend/", include("backend.urls")),
    path('api/', include("api.urls")),
    path('frontend/', include("frontend.urls")),
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('index'), permanent=False)),
]