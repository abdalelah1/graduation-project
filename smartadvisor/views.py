from django.shortcuts import render
from .function import *
from .models import *
from django.http import JsonResponse

# Create your views here.
def test(request):
   courses_map=courses_with_remaining_students()   
   split_course_counts_by_conditions()
   ispassedallprerequist= check_prerequist('ENIT4314','201910602')
   course_with_level(1)
   get_graduted_student()
   calculate_gpa('201910602')
   
   
   return JsonResponse({
                         'courses_map ':courses_map,
                         'if is passed :':ispassedallprerequist

                        })


