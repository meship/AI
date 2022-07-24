##################################################################
###### CONSTANTS #################################################
##################################################################

# Course
MOED_A = 1
MOED_B = 2

# CSP Exams
CS_EXAM_DIFFERENCE = 4
EE_EXAM_DIFFERENCE = 4
M_EXAM_DIFFERENCE = 5
CB_EXAM_DIFFERENCE = 4


# Exam Constraint
EXAMS_ON_DIFFERENT_DAYS_CONSTRAINT = 1
EACH_EXAM_HAS_A_DATE_CONSTRAINT = 2
DAYS_DIFFERENCE_ON_COMMON_FACULTIES_CONSTRAINT = 3
MOED_A_AND_B_DIFFERENCE_CONSTRAINT = 4
MIN_ATTEMPTS_DIFFERENCE = 14

# Main
FRIDAY = 4
SATURDAY = 5
EVENING_EXAM = 0.3
NOON_EXAM = 0.2
MORNING_EXAM = 0.1
MOED_A_RATIO = 0.6

COURSE_DATABASE = "Courses_Data.csv"
COURSE_ATTRIBUTES = ['name', 'number', 'faculties', 'type', 'credits', 'attempt']


#  WCSP_Constraint
HARD = 0
SOFT = 1
MAXIMUM_COST = 10

#  WCSP_Exam_Constraint
MATH_EXAMS_ON_MORNING = 5

# WCSP_EXAM
MATH_EXAMS_ON_MORNING_COST = 1