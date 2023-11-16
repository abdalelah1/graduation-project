from django.shortcuts import render
from .function import *
from .algorithm import *
from .models import *
from django.http import JsonResponse
import timeit
from django.utils import timezone

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
database = client["advisor"]
# Create your views here.
def test(request):
    start_time = timezone.now()
    map = getCourseswithstudents(1)
    end_time = timezone.now()
    elapsed_time = end_time - start_time
    print(elapsed_time)

    context={
        'final_map' : map
    }
    return render(request, 'test/test.html', context)
def elective(request):
    electivemap={}
    # university_map, college_map=all_optinal_courses()
    # client = pymongo.MongoClient("mongodb://localhost:27017/")
    # database = client["advisor"]
    # results_collection = database["electiveResult"]
    # results_collection.insert_one({"elective": list(elective), "university_map": list(university_map) , "college_map":list(college_map)})
    # client.close()

    collection = database["elective"]
    result = collection.find({}, {"_id": 0})
# استعراض جميع الوثائق ف    ي مجموعة البيانات
    for r in result:
    # الوصول إلى الـ key والـ value لكل وثيقة
        for key, value in r.items():
             electivemap[key]=value
    context ={
        'elective' : electivemap
    }
    return render(request, 'elective/elective.html',context)
    