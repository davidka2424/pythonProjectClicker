from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response

# Create your views here.
def index(request):
    return Response("ok")