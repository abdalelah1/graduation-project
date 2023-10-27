from .function import *
def recommendation_course(semester):
    students = Student.objects.all()
    max_priority=assign_course_priorities() 
    course_on_this_semester=course_with_level(semester)
    popular_courses, less_popular_courses , test_courses=count_students_per_course()
    course_with_count_same_level_or_above(test_courses)
  
    for student in students :
        _,_,_,_,_,_=get_students_details(student.university_ID)