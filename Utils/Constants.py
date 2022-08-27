import numpy as np  # for later use

#############################################################
###################### Global Constants #####################
#############################################################
# Solver Pure CSP
MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6
EVENING_EXAM = 0.3
NOON_EXAM = 0.2
MORNING_EXAM = 0.1
MOED_A_RATIO = 0.6

# Course
MOED_A = 0
MOED_B = 1

#############################################################
########### Pure Constraint Satisfaction Constants ##########
#############################################################

PURE_CONSTRAINT_COURSE_DATABASE = "../Data/Courses_Data.csv"
PURE_CONSTRAINT_COURSE_DATABASE2 = "../Data/Courses_Data2.csv"
COURSE_ATTRIBUTES = ['name', 'number', 'faculties', 'campus', 'students', 'hall type']
CLASSROOMS_ATTRIBUTES = ['name', 'area', 'capacity', 'chair type', 'classroom type']
CHOICE_CSP = 'csp'
CHOICE_WCSP = 'wcsp'
BACKTRACKING = 'backtracking'
MINIMUM_REMAINING_VARS = 'mrv'
DEGREE = 'd'
LEAST_CONSTRAINING_VALUE = 'lcv'
LEAST_CONSTRAINING_VALUE_AND_MINIMUM_REMAINING_VARS = 'combined'

# Exam Constraint
EXAMS_ON_DIFFERENT_DAYS_CONSTRAINT = 1
EACH_EXAM_HAS_A_DATE_CONSTRAINT = 2
DAYS_DIFFERENCE_ON_COMMON_FACULTIES_CONSTRAINT = 3
MOED_A_AND_B_DIFFERENCE_CONSTRAINT = 4
MIN_ATTEMPTS_DIFFERENCE = 14

# WCSP_Constraint
HARD = 0
SOFT = 1
MAXIMUM_COST = np.inf

# WCSP_Exam_Constraint
MATH_EXAMS_ON_MORNING = 5

# WeightedConstraintSatisfactionProblem
BEST_ASSIGNMENT_FOUND = 1
BEST_ASSIGNMENT_NOT_FOUND = 0

# WCSP_EXAM
MATH_EXAMS_ON_MORNING_COST = 1
CS_EXAM_DIFFERENCE = 6
EE_EXAM_DIFFERENCE = 6
M_EXAM_DIFFERENCE = 7
CB_EXAM_DIFFERENCE = 4

#############################################################
################ Informned Search Algorithms ################
#############################################################

# Exam differences constants
# First attempts
# Single faculties symbols
CS_EXAM_DIFFERENCE_A = 6
EE_EXAM_DIFFERENCE_A = 5
M_EXAM_DIFFERENCE_A = 7
CB_EXAM_DIFFERENCE_A = 5  # 4
ST_EXAM_DIFFERENCE_A = 5
E_EXAM_DIFFERENCE_A = 4
P_EXAM_DIFFERENCE_A = 6
PC_EXAM_DIFFERENCE_A = 5
# Multi faculties symbols
CSM_EXAM_DIFFERENCE_A = 4  # 3
CSE_EXAM_DIFFERENCE_A = 4  # 3
CSP_EXAM_DIFFERENCE_A = 4  # 3
PSB_EXAM_DIFFERENCE_A = 3
CSC_EXAM_DIFFERENCE_A = 4  # 3
# Second attempts
# Single faculties symbols
CS_EXAM_DIFFERENCE_B = 4
EE_EXAM_DIFFERENCE_B = 4
M_EXAM_DIFFERENCE_B = 4
CB_EXAM_DIFFERENCE_B = 3
ST_EXAM_DIFFERENCE_B = 3
E_EXAM_DIFFERENCE_B = 3
P_EXAM_DIFFERENCE_B = 4
PC_EXAM_DIFFERENCE_B = 3
# Multi faculties symbols
CSM_EXAM_DIFFERENCE_B = 3
CSE_EXAM_DIFFERENCE_B = 3
CSP_EXAM_DIFFERENCE_B = 3
PSB_EXAM_DIFFERENCE_B = 3
CSC_EXAM_DIFFERENCE_B = 3

# SimulatedAnnealing
ISA_COURSE_DATABASE = "../Data/Courses_Data.csv"
ISA_COURSE_DATABASE2 = "../Data/Courses_Data2.csv"
ISA_COURSE_DATABASE3 = "../Data/Courses_Data3.csv"  # "../Data/Courses_Data3.csv"
ISA_CLASSROOMS_DATABASE = "../Data/Classrom_Data.csv"
UNARY_PERIODS_MOVE = 0
UNARY_MOVE_FORWARD = 1
UNARY_MOVE_BACKWARD = -1
BINARY_MOVE = 1
RANDOM_MOVE = 2
ADD_HALL = 3
REMOVE_HALL = 4
ATTEMPTS_DIFF = 12
N_TRIES = 250
ALPHA = 0.85

# Genetic Algorithms
N_ATTEMPTS_TO_REPRODUCE = 100
CROSSOVER_PROB = 90
MUTAION_PROB = 40
PROB_DOMAIN = 100
PENALTY_RATIO = 0.5
MAX_STUDENTS_PER_TIME = 540

# Run solvers
RANDOM_GRADIENT_DESCENT = "rgd"
SIMULATED_ANNEALING = "sa"
GENETIC_ALGORITHM = "ga"
GRADIENT_DESCENT = "gd"
ALGORITHM_TO_MESSAGE = {"sa": "Chosen algorithm is SimulatedAnnealing", "gd": "Chosen algorithm is Gradient Descent",
						"rgd": "Chosen algorithm is Random Gradient Descent"}
GENETIC_ALGORITHM_MESSAGE = "Chosen algorithm is Genetic Algorithm"
GD_MAX_ITER = 100
GD_MAX_ITER_COMPLEX = 150
SA_MAX_ITER = 5000
POPULATION_SIZE = 92
POPULATION_SIZE_COMPLEX = 62
GENERATION_SIZE = 300
GENERATION_SIZE_COMPLEX = 350
#############################################################
################ Extended problem ###########################
#############################################################
UNARY_HALL_MOVE = 0
BINARY_HALL_MOVE = 1
CONTINUE_TO_COMPLEX_MESSAGE = "Do you wish to assign halls as well? y/n\n"
SQUEEZE_RATIO = 1.25

#############################################################
######################## Utils ##############################
#############################################################

# Google Calendar
TIMEZONE = "Israel"
DECISION_MESSAGE = "Do you want to save the calendar? Please insert y/n\n"
DELETE_MESSAGE = "Deleting calendar"
