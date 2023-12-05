from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from .views import *
urlpatterns = [
    path('elective/',elective     , name='elective'),
    path('test/',test     , name='test'),
    path('',welcome     , name='home'),
    path('courses/',courses , name='courses'),
    path('general/',general , name='general'),
    path('college/',college , name='college'),
     path('help/',help , name='help'),
    path('department/',department , name='department'),
    path('major/',major , name='major'),
    path('students/',students , name='students'),
    path('allcourses/',allcourses , name='allcourses'),
    path('report/',department_details , name='report'),
    path('login/',login_page , name='login'),
    path('student-details/<str:student_id>/',student_details, name='student_details'),


]