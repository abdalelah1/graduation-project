from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from .views import *
urlpatterns = [
    path('elective/',elective     , name='elective'),
    path('test/',test     , name='test')
]