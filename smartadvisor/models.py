

from django.db import models ,connection

# Create your models here.
from django.contrib.auth.models import User
from datetime import date,datetime
class semester_name(models.Model):
    name=models.CharField(max_length=10)
class Level (models.Model):
    level =models.CharField(max_length=50)
    semester_name=models.ForeignKey(semester_name,on_delete=models.CASCADE,null=True)
class University( models.Model):
    name =models.CharField(max_length=50)
    no_university_courses_required = models.IntegerField()

class University_Courses (models.Model):
    name =models.CharField(max_length=50)
    code=models.CharField(max_length=20)
    level = models.ForeignKey(Level,on_delete=models.CASCADE,null=False)
    credit = models.CharField(max_length=10)
    is_reuqired = models.BooleanField(default=True)
    hours_condition= models.IntegerField(null=True,default=0)
    preRequst =models.ManyToManyField('self',blank=True, symmetrical=False)

class College(models.Model):
    name =models.CharField(max_length=50)
    number_of_required_optional_course = models.IntegerField(default=2)
    university= models.ForeignKey(University,on_delete=models.CASCADE,null=True)
class Admin (models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    college = models.ForeignKey(College,on_delete=models.CASCADE,null=False)
class Department(models.Model):
    name =models.CharField(max_length=50)
    college=models.ForeignKey(College,on_delete=models.CASCADE,null=False)
    full_courses_count =models.IntegerField()
    no_hourse_Tobe_graduated = models.IntegerField()
    no_required_Elecvtive=models.IntegerField()
    
class Major(models.Model):
    name =models.CharField(max_length=50)
    department=models.ForeignKey(Department,on_delete=models.CASCADE,null=False)

class Course_Type (models.Model):
    typeOfCourse =models.CharField(max_length=50)
class level2(models.Model):
    name=  models.CharField(max_length=50)
class sublevel(models.Model):
    name = models.CharField(max_length=50)
    level = models.ForeignKey(level2,on_delete=models.CASCADE,null=True)
# Create your models here.
class Course(models.Model):
    name =models.CharField(max_length=50)
    code=models.CharField(max_length=20)
    level = models.ForeignKey(Level,on_delete=models.CASCADE,null=False)
    credit = models.CharField(max_length=10)
    is_reuqired = models.BooleanField(default=True) #ساعات مسجلة
    majors = models.ManyToManyField(Major)
    type = models.ForeignKey(Course_Type,on_delete=models.CASCADE,null=False)
    hours_condition= models.IntegerField(null=True,default=0)
    preRequst =models.ManyToManyField('self',blank=True, symmetrical=False)
    level2 = models.ForeignKey(level2,on_delete=models.CASCADE,null=True )
    def __str__(self) :
            return  str(self.code)


class Student (models.Model):
    university_ID=models.CharField(max_length=50,null=True)
    name = models.CharField(max_length=50 , null=True)
    major=models.ForeignKey(Major,on_delete=models.CASCADE,null=True)
    GPA = models.CharField(max_length=50,null=True)
    level = models.ForeignKey(Level , on_delete=models.CASCADE,null=True)
    Hours_count= models.IntegerField(null=True)
class Course_History(models.Model):
    degree = models.CharField(max_length=50)
    student=models.ForeignKey(Student,on_delete=models.CASCADE,null=False)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    universit_course = models.ForeignKey(University_Courses,on_delete=models.CASCADE,null=True)
class Recommended_Course (models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=False)
    student=models.ForeignKey(Student,on_delete=models.CASCADE,null=False)
    no_student = models.IntegerField()

