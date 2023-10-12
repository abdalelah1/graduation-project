

# Create your models here.
from django.db import models

class College(models.Model):
    name =models.CharField(max_length=50)
    
class Department(models.Model):
    name =models.CharField(max_length=50)
    college=models.ForeignKey(College,on_delete=models.CASCADE,null=False)
class Major(models.Model):
    name =models.CharField(max_length=50)
    department=models.ForeignKey(Department,on_delete=models.CASCADE,null=False)

class AdvisoryPlan(models.Model):
    department=models.ForeignKey(Department,on_delete=models.CASCADE,null=False)

class Year (models.Model):
    name =models.CharField(max_length=50)
    advisoryPlan=models.ForeignKey(AdvisoryPlan,on_delete=models.CASCADE,null=False)


class Semester(models.Model):
    name =models.CharField(max_length=50)
    year=models.ForeignKey(Year,on_delete=models.CASCADE,null=False)


# Create your models here.
class Course(models.Model):
    name =models.CharField(max_length=50)
    code=models.CharField(max_length=20)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE,null=False)
    credit = models.CharField(max_length=10) #ساعات مسجلة
    preRequst =models.ManyToManyField('self', blank=True, symmetrical=False,null=True)
class University_General_Education_course(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=False)
    is_required = models.BooleanField(default=False)
    n_of_course_completed = models.IntegerField()

class Major_Course(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=False)
    is_required = models.BooleanField(default=False)
    n_of_course_completed = models.IntegerField()


class College_Course(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=False)
    is_required = models.BooleanField(default=False)
    n_of_course_completed = models.IntegerField()

class Student (models.Model):
    university_ID=models.CharField(max_length=50)
    GPA = models.CharField(max_length=50)

class Course_History(models.Model):
    degree = models.CharField(max_length=50)
    student=models.ForeignKey(Student,on_delete=models.CASCADE,null=False)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=False)
class Recommended_Course (models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=False)
    student=models.ForeignKey(Student,on_delete=models.CASCADE,null=False)
    no_student = models.IntegerField()


