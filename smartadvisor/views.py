from django.shortcuts import render
from .function import *
from .models import *
from django.http import JsonResponse

# Create your views here.
def test(request):
   remaining_courses_for_student, completed_courses, conditional_courses, fail_courses,= get_students_details(201910602)
   courses_map=courses_with_remaining_students()   
   split_course_counts_by_conditions()
   ispassedallprerequist= check_prerequist('ENIT4314','201910602')
   course_with_level(1)
   get_graduted_student()
   
   
   return JsonResponse({'remaining_courses_for_student ':remaining_courses_for_student,
                        'completed_courses ':completed_courses,
                        'conditional_courses ':conditional_courses,
                        'fail_courses ':fail_courses,
                         'courses_map ':courses_map,
                         'if is passed :':ispassedallprerequist

                        })


