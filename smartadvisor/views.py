from django.shortcuts import render
from .function import *
from .algorithm import *
from .models import *
from django.http import JsonResponse

# Create your views here.
def test(request):
    combined_data =recommendation_course(1)
    return render(request, 'test/test.html', {'combined_data': combined_data})
