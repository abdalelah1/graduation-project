from django.shortcuts import render
from .function import *
from .algorithm import *
from .models import *
from django.http import JsonResponse

# Create your views here.
def test(request):
    recommendation_course(1)
    return JsonResponse({
    })

