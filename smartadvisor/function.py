from .models import *
from collections import Counter
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import copy
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

def allcourses():
    courses = Course.objects.all()
    university_courses = University_Courses.objects.all()
    list_of_courses = [course.code for course in courses] + [u_course.code for u_course in university_courses]
    return list_of_courses
def get_students_details(student_id):
    completed_courses = []
    fail_courses = []
    conditional_courses = []
    number_elective=0
    number_university_un_required =0
    number_college_un_required=0
    credits_completed=0
    credits_conditional=0
    fail_passed=[]
    elective_complete =[]
    universite_optional_passed =[]
    college_optional_passsed =[]
    elective_remaining =[]
    university_optional_remaining=[]
    college_optional_remaining=[]
    
    
    optional_map={
        'college':'',
        'elective':'',
        'university':'',
    }

    try:
        student = Student.objects.get(university_ID=student_id)
    except Student.DoesNotExist:
        return "Student not found"
    number_elective=int(student.major.department.no_required_Elecvtive)
    number_college_un_required=int(student.major.department.college.number_of_required_optional_course)
    number_university_un_required = int (student.major.department.college.university.no_university_courses_required)
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
        
    for course in fail_courses:
        if course in completed_courses:
            fail_courses.remove(course)
            fail_passed.append(course)
    for course in conditional_courses:
        if course in completed_courses:
            conditional_courses.remove(course)
    if float(student.GPA) >2.00 :
        conditional_passed = set(remaining_courses_for_student) & set(conditional_courses)
        remaining_courses_for_student = set(remaining_courses_for_student) - conditional_passed
    for code in completed_courses :
        course = None
        try :
            course = Course.objects.get(code = code)

            if course.is_reuqired==False and course.type.id==1:
               
                elective_complete.append(code)
            elif course.is_reuqired==False and course.type.id==2:
                college_optional_passsed.append(code)
        except : 
            course = University_Courses.objects.get(code = code)
  
            if course.is_reuqired==False and code in completed_courses :
                universite_optional_passed.append(code)
    key_delete=[]
    for code in remaining_courses_for_student :
        try :
            course = Course.objects.get(code = code)
            if course.is_reuqired==False and course.type.id==1:            
                elective_remaining.append(code)
                key_delete.append(code)
            elif course.is_reuqired==False and course.type.id==2:
                college_optional_remaining.append(code)
                key_delete.append(code)
        except : 
            course = University_Courses.objects.get(code = code)
            university_optional_remaining.append(code)
            key_delete.append(code)
    for code in key_delete : 
        remaining_courses_for_student.remove(code)
    if len(college_optional_passsed) == number_college_un_required:
        optional_map['college']='Passed'
    else : 
        optional_map['college']=(college_optional_passsed, {'remaining_count ':number_college_un_required - len(college_optional_passsed),
                                                            'remaining_course':college_optional_remaining})
    if len(universite_optional_passed) == number_university_un_required:
        optional_map['university']='Passed'
    else : 
        optional_map['university']=(universite_optional_passed, {'remaining ':number_university_un_required- len(universite_optional_passed),
                                                                'remaining_course':university_optional_remaining
                                                                 })
    if len(elective_complete) == number_elective:
        optional_map['elective']='Passed'
    else : 
        optional_map['elective']=(elective_complete, {'remaining ':number_elective- len(elective_complete),
                                                      'remaining_course':elective_remaining
                                                      })

    return list(remaining_courses_for_student),set( completed_courses), set(conditional_courses), set(fail_courses) , set(fail_passed),optional_map
def courses_with_remaining_students():
    courses_map = {}  
    optinal_map={}

    all_students = Student.objects.all()
    
    for student in all_students:
        student_id = student.university_ID
        remaining_courses_for_student, _, _, _ ,_,optional= get_students_details(student_id=student_id)
        
        courses_map[student_id] = remaining_courses_for_student
        optinal_map[student_id]=optional
    return courses_map,optinal_map
def count_students_per_course():
    courses_map,_ = courses_with_remaining_students()
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
                course_data[course][0].append(student_id)
                course_data[course][1] += 1
            else:
                course_data[course] = [[student_id], 20]

    # Filter courses with 20 or more students
    popular_courses = [data for data in course_data.values() if data[1] >= 20]
    less_popular_courses = [data for data in course_data.values() if data[1] < 20]
    test_courses = course_data.copy()

    keys_to_delete = []

    # التكرار عبر العناصر في القاموس
    for key, value in test_courses.items():
        if value[1] < 20:
            keys_to_delete.append(key)

    # حذف العناصر المحددة
    for key in keys_to_delete:
        del test_courses[key]
 
    return popular_courses, less_popular_courses , test_courses
def split_course_counts_by_conditions():

    popular_courses, less_popular_courses , test_courses = count_students_per_course()
    for code  in test_courses:
        print(test_courses[code])
    # Define the conditions
    course_College_required = []
    course_College_not_required = []
    course_major_required = []
    course_major_not_required = []
    course_universite_required = []
    course_university_not_required = []    
    course = None
    for course_code in test_courses:
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
def check_prerequist(course_code , student_id): 
    student = Student.objects.get(university_ID=student_id)
    course = Course.objects.get(code=course_code)
    prerequisites = course.preRequst.all()
    missing_pre=[]
    remaining_courses_for_student,completed_courses,conditional_courses ,fail_courses,_,_=get_students_details(student_id) 
    for pre in prerequisites :
        if pre.code in completed_courses:
            missing_pre=[]
        else:
             missing_pre.append(pre.code)
            # قائمة بأسماء المواد التي لم ينجزها الطالب بنجاح
    if missing_pre==[]:
        return True
    else :
        return missing_pre
def course_with_level(semester):
    levels = Level.objects.filter(semester_name=semester)
    courses_with_levels={}
    university_courses_with_levels={}
    for level in levels :
        condition1= Q(level=level)
        condition2= Q(is_reuqired=True)
        conditions=condition1 & condition2
        course=Course.objects.filter(conditions)
        university_Courses=University_Courses.objects.filter(conditions)
        university_courses_with_levels[level.level]=[c.code for c in university_Courses]
        courses_with_levels[level.level]=[c.code for c in course]
    return courses_with_levels , university_courses_with_levels
def get_graduted_student():
    graduated_student={}
    students=Student.objects.all()
    for student in students :
        _,completed_courses,_,_,_,_=get_students_details(student_id=student.university_ID)
        print(student.major.department.full_courses_count ,'-',student.Hours_count ,'=<',student.major.department.no_hourse_Tobe_graduated)
        if int(student.major.department.full_courses_count ) - int(student.Hours_count) <=int(student.major.department.no_hourse_Tobe_graduated):
            print(True)
            graduated_student[student.university_ID]=int(student.major.department.full_courses_count ) - int(student.Hours_count) 
    print('graduated_student',graduated_student)
    return graduated_student
def calculate_credits(list_of_courses): 
    course=None
    counter=0
    for code in list_of_courses:
        try:
            course= Course.objects.get(code=code)
            counter += int(course.credit)
        except :
            course=University_Courses.objects.get(code=code)
            counter += int(course.credit)
    return counter
    
def calculate_gpa(student_id):
    student = Student.objects.get(university_ID=student_id)
    remaining_courses_for_student, completed_courses, conditional_courses, fail_courses, fail_passed,_ = get_students_details(student_id)

    highest_degree = {}
    course_credits = {}

    for course_code in completed_courses.union(conditional_courses):
        highest_degree[course_code] = -1

    for course_code in completed_courses.union(conditional_courses):
        try:
            course = Course.objects.get(code=course_code)
            degree_numeric = highest_degree[course_code]

            for course_history in Course_History.objects.filter(student=student, course=course):
                degree_numeric = float(max(degree_numeric, letter_grade_to_numeric(course_history.degree)))
                highest_degree[course_code] = float(degree_numeric)
                course_credits[course_code] = float(course.credit)
        except Course.DoesNotExist:
            try:
                university_course = University_Courses.objects.get(code=course_code)
                degree_numeric = float(highest_degree[course_code])
                for course_history in Course_History.objects.filter(student=student, universit_course=university_course):
                    degree_numeric = float(max(degree_numeric, letter_grade_to_numeric(course_history.degree)))
                    highest_degree[course_code] = float(degree_numeric)
                    course_credits[course_code] = float(university_course.credit)
            except University_Courses.DoesNotExist:
                continue

    total_points = 0.0
    total_credits = 0.0

    gpa_scale = {
        50: 1.5,
        55: 1.75,
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
    print(course_credits    )
    for course_code in completed_courses.union(conditional_courses):
        degree_numeric = highest_degree[course_code]
        credits = course_credits[course_code]
        gpa = gpa_scale.get(degree_numeric, 0)
        total_points += gpa * credits
        total_credits += credits

    if total_credits == 0:
        return 0

    gpa = total_points / total_credits
    rounded_gpa = round(gpa, 2)
    print("Total Points:", total_points)
    print("full gpa is :", gpa)
    return rounded_gpa

def assign_course_priorities():
    graduated_student_ids = get_graduted_student()
    remaining_courses_map,_ = courses_with_remaining_students()

    course_priorities = {
        "1": {}
    }
    newmap={}
    # Assign max priority '1' to remaining courses for graduated students
    for student_id in graduated_student_ids:
        remaining_courses = remaining_courses_map.get(student_id, [])
        for course in remaining_courses:
            if course in course_priorities["1"]:
                course_priorities["1"][course].append(student_id)
            else:
                course_priorities["1"][course] = [student_id]
    modified_data = course_priorities.copy()  # لنقم بنسخ البيانات الأصلية

    for semester, courses in modified_data.items():
        for course, student_list in courses.items():
            student_count = len(student_list)
            courses[course] = (student_list, student_count)
    return modified_data
def course_with_count_same_level_or_above(test_courses):
    print(test_courses)
    same_level={}
    less_level ={}
    course_level_greater_than_student={}
    
    for course_code, course_info in test_courses.items():
        course = None
        try:
            course = Course.objects.get(code=course_code)
        except:
            course = University_Courses.objects.get(code=course_code)
        for university_id in course_info[0]:
            student = Student.objects.get(university_ID=university_id)
            if int(course.level.id) ==int(student.level.id):
                same_level[course_code]=course_info
            elif int(course.level.id) <int(student.level.id):
                less_level[course_code] = course_info
            else :   
                course_level_greater_than_student[course_code]=course_info
                
               
    print('test_courses from check',same_level)
    print('less level ', less_level)
    print('course_level_greater_than_student',course_level_greater_than_student)
    return same_level , less_level , course_level_greater_than_student
    
    
def calculate_gpa_directly(student_id, completed_courses, conditional_courses, fail_courses):
    highest_degree = {}
    course_credits = {}

    all_courses = set(completed_courses).union(conditional_courses).union(fail_courses)

    total_points = 0.0
    total_credits = 0.0

    gpa_scale = {
        50: 1.5,
        55: 1.75,
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

    for course_info in all_courses:
        course_code, (credit, grade) = course_info
        degree_numeric = letter_grade_to_numeric(grade)
        credits = float(credit)

        highest_degree[course_code] = degree_numeric
        course_credits[course_code] = credits

        gpa = gpa_scale.get(degree_numeric, 0)
        total_points += gpa * credits
        total_credits += credits

    if total_credits == 0:
        return 0

    gpa = total_points / total_credits
    rounded_gpa = round(gpa, 2)
    print("gpa2",gpa)
    return rounded_gpa