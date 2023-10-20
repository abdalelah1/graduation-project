from .function import *
def recommendation_course(student_id,semister):
    remaining_courses_for_student, completed_courses, conditional_courses, fail_courses=get_students_details(student_id)
    return get_students_details