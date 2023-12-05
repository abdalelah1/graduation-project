from django.shortcuts import render,redirect
from .function import *
from .algorithm import *
from .models import *
from django.http import JsonResponse
import timeit
from django.utils import timezone
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


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
###############
@login_required(login_url='login')
def home (request) : 
    if request.user.is_superuser:
        User.objects.filter(is_staff=True).exclude(username=request.user.username).update(is_active=False)
        
        # تسجيل الخروج من الحساب الحالي
        logout(request) 
    user  = request.user
    context = {}
    context= {
        'user':user
    }
    return render (request,'home/home.html',context)
@login_required(login_url='login')
def allcourses(request):
    courses_required = Course.objects.filter(is_reuqired=True)
    courses_not_required = Course.objects.filter(is_reuqired=False ,type=2)
    elective = Course.objects.filter(is_reuqired=False ,type=1)
    context={
        'courses_required':courses_required,
        'courses_not_required':courses_not_required,
        'elective':elective
    }
    return render (request,'allcourses/allcourses.html',context)
def courses(request):
        return render (request,'courses/courses.html')
def general(request):
    return render (request,'general/general.html')
def college(request):
    return render (request,'college/college.html')
def department(request):
    return render (request,'department/department.html')
def major(request):
    return render (request,'major/major.html')
def welcome(request):
    return render (request,'welcome/welcome.html')
def help(request):
    return render (request,'help/help.html')

def student_details(request, student_id):
    # Retrieve the student object from the database using the student_id
    try:
        student = Student.objects.get(university_ID=student_id)
    except Student.DoesNotExist:
        # Handle the case where the student is not found
        return render(request, 'student_details/student_not_found.html')

    # Fetch details for the selected student using the function
    student_details = get_students_details(student_id)

    # Pass the student object and their details to the template
    context = {
        'student': student,
        'student_details': student_details,
    }
    return render(request, 'student_details/student_details.html', context)
@login_required(login_url='login')
def students(request):
    user = request.user
    
    students = Student.objects.filter(major__department=user.advisor.department )
    context={}
    context={
        'students':students
    }
    return render (request,'students/students.html',context)

def department_details(request):
    departments = Department.objects.all()
    context = {
        'departments': departments
    }
    return render( request,'report/report.html', context)
@csrf_exempt
def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('admin:index')
            else : 
                login(request, user)
                return redirect('home')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login/login.html', {'error': error_message})
    return render(request, 'login/login.html')