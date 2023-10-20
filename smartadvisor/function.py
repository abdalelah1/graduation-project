from .models import *
from collections import Counter

def RemainingCourses(all_courses, completed_courses):
    all_courses_set = set(all_courses)
    completed_courses_set = set(completed_courses)
    remaining_courses_set = all_courses_set - completed_courses_set
    remaining_courses = list(remaining_courses_set)

    return remaining_courses
def letter_grade_to_numeric(grade):
    if grade =='A+':
        return 98
    elif grade == 'A':
        return 95
    elif grade == 'A-':
        return 90
    elif grade == 'B+':
        return 85
    
    elif grade == 'B':
        return 80
    elif grade == 'B-':
        return 75
    elif grade == 'C+':
        return 70
    elif grade == 'C':
        return 65  
    elif grade == 'C-':
        return 60 
    elif grade == 'D+':
        return 55 
    elif grade == 'D':
        return 50
    elif grade== 'F' :
        return 0
    else :
        print("error on this grada ",grade)
        return 0
def calculate_gpa(grades):
    gpa_scale = {
        60: 2.0,
        65: 2.25,
        70: 2.5,
        75: 2.75,
        80: 3.0,
        85: 3.25,
        90: 3.5,
        95: 3.75,
        98: 4.0
    }

    total_points = 0.0
    total_credits = 0.0

    for grade, credits in grades:
        print(grade , credits)
        gpa = gpa_scale.get(grade, 0) 
        print(type(gpa)) 
        print(type(credits)) 
        total_points += float(gpa) * float(credits)
        total_credits += float(credits)
    if total_credits == 0:
        return 0 
    gpa = total_points / total_credits
    return gpa
def allcourses():
    courses = Course.objects.all()
    university_courses = University_Courses.objects.all()
    list_of_courses = [course.code for course in courses] + [u_course.code for u_course in university_courses]
    return list_of_courses

def get_students_details(student_id):
    completed_courses = []
    fail_courses = []
    grades = [] 
    conditional_courses = []
    repeated_course_codes = []
    counter = 0
    conditional_passed=[]
    is_graduate = False

    try:
        student = Student.objects.get(university_ID=student_id)
    except Student.DoesNotExist:
        return "Student not found"
    
    all_student_courses = Course_History.objects.filter(student=student)
    
    for course in all_student_courses:
        grade = letter_grade_to_numeric(course.degree)
        credits = course.course.credit  
        course_code = course.course.code
        grades.append((grade,credits))
        ###############################################   
        if letter_grade_to_numeric( course.degree )> 59:   
            completed_courses.append(course.course.code)
        elif letter_grade_to_numeric( course.degree ) < 50:
            fail_courses.append(course.course.code)
        else:
            conditional_courses.append(course.course.code)
    all_courses = allcourses()
    remaining_courses_for_student = RemainingCourses(all_courses, completed_courses)
    if float(student.GPA) >2.00 :
        conditional_passed = set(remaining_courses_for_student) & set(conditional_courses)
        remaining_courses_for_student = set(remaining_courses_for_student) - conditional_passed
    return list(remaining_courses_for_student), completed_courses, conditional_courses, fail_courses


def courses_with_remaining_students():
    courses_map = {}  
    
    all_students = Student.objects.all()
    
    for student in all_students:
        student_id = student.university_ID
        remaining_courses_for_student, _, _, _ = get_students_details(student_id=student_id)
        
        courses_map[student_id] = remaining_courses_for_student
        
    return courses_map

