from .function import *
def recommendation_course(semester):
    students = Student.objects.all()
    max_priority=assign_course_priorities() 
    print(max_priority)
    for student in students :
        _,_,_,_,_,_=get_students_details(student.university_ID)