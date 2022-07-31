from datetime import datetime
from Utils.utils import export_to_calendar

import pandas as pd
from InformedSearchAlgorithms.SimulatedAnnealing.SimulatedAnnealingSolver import SimulatedAnnealingSolver
import sys
from InformedSearchAlgorithms.GeneticAlgorithm.GeneticAlgorithmSolver import *
from Utils.utils import get_courses, make_domain


def preprocess_courses(courses_list, times_list):
    n_courses = len(courses_list)
    n_times = len(times_list)
    courses_to_rows_dict = dict()
    times_to_cols_dict = dict()
    reverse_times_to_cols_dict = dict()
    for course_index, course in enumerate(courses_list):
        courses_to_rows_dict[course] = course_index
    for time_index, time in enumerate(times_list):
        times_to_cols_dict[time] = time_index
        reverse_times_to_cols_dict[time_index] = time
    return n_courses, n_times, courses_to_rows_dict, times_to_cols_dict, reverse_times_to_cols_dict


def cooling_function(temp, alpha, t):
    return temp*(alpha**t)


def update_course_data(courses_dict, result_assignment_dict, reverse_time_dict, dates_dict, hours):
    for course, course_ind in courses_dict.items():
        repr_time = reverse_time_dict[result_assignment_dict[course_ind]]
        real_date = dates_dict[repr_time]
        year = real_date.year
        month = real_date.month
        day = real_date.day
        repr_time = round(repr_time - int(repr_time), 1)
        course.set_exam_time(datetime(year, month, day, hours[repr_time][0], hours[repr_time][1], 0))


if __name__ == '__main__':
    # argv[0] = kind, argv[1 + 2] = '2022/01/15', '2022/03/08'
    data = pd.read_csv(ISA_COURSE_DATABASE3)
    courses = get_courses(data)
    representative_times, number_to_real_date_dict = make_domain(sys.argv[2], sys.argv[3])
    n_courses, n_times, courses_to_rows_dict, times_to_cols_dict, reverse_times_to_cols_dict = preprocess_courses(
        courses, representative_times)
    hours_dict = {MORNING_EXAM: (9, 0), NOON_EXAM: (13, 30), EVENING_EXAM: (17, 0)}
    if sys.argv[1] == SIMULATED_ANNEALING:
        print(SIMULATED_ANNEALING_MESSAGE)
        solver = SimulatedAnnealingSolver(n_courses, n_times, courses_to_rows_dict, times_to_cols_dict,
                                          reverse_times_to_cols_dict, None, number_to_real_date_dict,
                                          0.85, cooling_function)
        solver.solve()
        print(solver.get_state())
        update_course_data(courses_to_rows_dict, solver.get_state().assignment_dict, reverse_times_to_cols_dict,
                           number_to_real_date_dict, hours_dict)
        solver.check_solution_quality()
    else:
        print(GENETIC_ALGORITHM_MESSAGE)
        solver = GeneticAlgorithmSolver(n_courses, n_times, courses_to_rows_dict,
                                        times_to_cols_dict, reverse_times_to_cols_dict, number_to_real_date_dict,
                                        POPULATION_SIZE)
        solver.solve()
        print(solver.get_best_child())
        update_course_data(courses_to_rows_dict, solver.get_best_child().assignment_dict, reverse_times_to_cols_dict,
                           number_to_real_date_dict, hours_dict)
        solver.check_solution_quality()


    # scopes = ["https://www.googleapis.com/auth/calendar"]
    # flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
    # credentials = flow.run_console()
    # pickle.dump(credentials, open("token.pkl", "wb"))
    # credentials = pickle.load(open("token.pkl", "rb"))
    # service = build("calendar", "v3", credentials=credentials)
    # result = service.calendarList().list().execute()
    # calendar_id = result["items"][0]['id']
    export_to_calendar(courses)
    # scopes = ["https://www.googleapis.com/auth/calendar"]
    # flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
    # flow.run_console()