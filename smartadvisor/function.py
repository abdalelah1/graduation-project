def RemainingCourses(all_courses, completed_courses):
    all_courses_set = set(all_courses)
    completed_courses_set = set(completed_courses)
    remaining_courses_set = all_courses_set - completed_courses_set
    remaining_courses = list(remaining_courses_set)

    return remaining_courses
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

    total_points = 0
    total_credits = 0

    for grade, credits in grades:
        gpa = gpa_scale.get(grade, 0)  
        total_points += gpa * credits
        total_credits += credits
    if total_credits == 0:
        return 0 
    gpa = total_points / total_credits
    return gpa
