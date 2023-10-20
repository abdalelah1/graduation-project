from django.shortcuts import render
from .function import *
from .models import *
from django.http import JsonResponse

# Create your views here.
def test(request):
   remaining_courses_for_student, completed_courses, conditional_courses, fail_courses,= get_students_details(201910602)
   
   return JsonResponse({'remaining_courses_for_student ':remaining_courses_for_student,
                        'completed_courses ':completed_courses,
                        'conditional_courses ':conditional_courses,
                        'fail_courses ':fail_courses,
                        })
   