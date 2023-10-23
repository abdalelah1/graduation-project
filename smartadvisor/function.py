from .models import *
from collections import Counter
from django.core.exceptions import ObjectDoesNotExist

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

        gpa = gpa_scale.get(grade, 0) 

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
    credits_completed=0
    credits_conditional=0
    is_graduate = False

    try:
        student = Student.objects.get(university_ID=student_id)
    except Student.DoesNotExist:
        return "Student not found"
    
    all_student_courses = Course_History.objects.filter(student=student)

    for course in all_student_courses:
        grade = letter_grade_to_numeric(course.degree)
        if course.course :
          
            credits = course.course.credit  
            course_code = course.course.code
        else : 
            
            credits = course.universit_course.credit  
            course_code = course.universit_course.code
        # uni_code = course.universit_course.code
        grades.append((grade,credits))
        ###############################################   
        if letter_grade_to_numeric( course.degree )> 59:
            credits_completed+=int(credits)
            completed_courses.append(course_code)
            # completed_courses.append(uni_code)
        elif letter_grade_to_numeric( course.degree ) < 50:
            fail_courses.append(course_code)
            # fail_courses.append(uni_code)
        else:
            conditional_courses.append(course_code)
            # conditional_courses.append(uni_code)
            credits_conditional+=int(credits)
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
def count_students_per_course():
    courses_map = courses_with_remaining_students()
    course_counts = Counter()

    # Count the number of students for each course
    for student_id, course_code in courses_map.items():
        for course in course_code:
            course_counts[course] += 1

    # Create a dictionary to store the result
    course_data = {}

    # Group the data by course ID
    for student_id, course_code in courses_map.items():
        for course in course_code:
            if course in course_data:
                course_data[course][1].append(student_id)
                course_data[course][2] += 1
            else:
                course_data[course] = [course, [student_id], 1]

    # Filter courses with 20 or more students
    popular_courses = [data for data in course_data.values() if data[2] >= 20]
    less_popular_courses = [data for data in course_data.values() if data[2] < 20]
    test_courses = [data for data in course_data.values() ]

    return popular_courses, less_popular_courses , test_courses
def split_course_counts_by_conditions():
    popular_courses, less_popular_courses , test_courses = count_students_per_course()
  
    # Define the conditions
    course_College_required = []
    course_College_not_required = []
    course_major_required = []
    course_major_not_required = []
    course_universite_required = []
    course_university_not_required = []    
    course = None
    for course_code, student_id, count in test_courses:
        try: 
            course = Course.objects.get(code=course_code)
            print(course.name, course.code,course.is_reuqired , course.type.id )
            course_type = course.type.id
            is_required = course.is_reuqired  


        except ObjectDoesNotExist:
            try:
                course = University_Courses.objects.get(code=course_code)
                print('This is a university course:', course.name, course.code,course.is_reuqired , )

                is_required = course.is_reuqired  
                # هنا يمكنك إضافة المزيد من المعالجة إذا لزم الأمر
            except ObjectDoesNotExist:
                print('Course not found:', course_code)
  
        if  isinstance(course, Course):
            if is_required and course_type==1:
                course_major_required.append(((student_id, course_code, count)))
            elif is_required and course_type==2:
                 course_College_required.append(((student_id, course_code, count)))
            elif is_required==False and course_type==1:
                course_major_not_required.append(((student_id, course_code, count)))
            elif is_required==False and course_type==2:
                 course_College_not_required.append(((student_id, course_code, count)))
        else:
            if is_required :
                course_universite_required.append((student_id, course_code, count))
            else :
                course_university_not_required.append((student_id, course_code, count))
    print("course_major_required" , course_major_required)
    print("course_major_not_required" , course_major_not_required)
    print("course_College_required" , course_College_required)
    print("course_College_not_required" , course_College_not_required)
    print("course_universite_required" , course_universite_required)
    print("course_university_not_required" , course_university_not_required)