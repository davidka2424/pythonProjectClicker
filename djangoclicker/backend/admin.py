from django.contrib import admin

# Register your models here.
from backend.models import Boost, Core

admin.site.register(Core)
admin.site.register(Boost)