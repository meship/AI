import random
import numpy as np
import pandas as pd
from simulated_annealing_state import SimulatedAnnealingState
from main import make_variables, make_domain
from Course import *
from Constants import *


class SimulatedAnnealingSolver:

    def __init__(self, n_courses, n_times, courses_to_rows_dict,
                 times_to_cols_dict, reverse_times_to_cols_dict, assignment_dict,
                 alpha, cooling_function, max_iter=5000):
        self.state_ = SimulatedAnnealingState(n_courses, n_times, courses_to_rows_dict, times_to_cols_dict,
                                              reverse_times_to_cols_dict, assignment_dict, True)
        self.initial_temperature_ = 1
        self.alpha_ = alpha
        self.cooling_function_ = cooling_function
        self.max_iter_ = max_iter

    def solve(self):
        temperature = self.initial_temperature_
        for t in range(self.max_iter_):
            if temperature == 0:
                return
            next_state = self.state_.generate_successor()
            delta = next_state.get_value() - self.state_.get_value()
            if delta < 0:
                self.state_ = next_state
            else:
                val = random.uniform(0, 1)
                if val < np.exp(-delta/temperature):
                    self.state_ = next_state
            temperature = self.cooling_function_(self.initial_temperature_, self.alpha_, t)

    def get_state(self):
        return self.state_


def get_courses(given_data):
    courses = list()
    for moed in [(MOED_A, 'A'), (MOED_B, 'B')]:
        for index in given_data.index:
            courses.append(Course(given_data[COURSE_ATTRIBUTES[0]][index] + f' - {moed[1]}',
                                  given_data[COURSE_ATTRIBUTES[1]][index],
                                  given_data[COURSE_ATTRIBUTES[2]][index],
                                  given_data[COURSE_ATTRIBUTES[3]][index],
                                  given_data[COURSE_ATTRIBUTES[4]][index],
                                  moed[0]))
    return courses


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


if __name__ == '__main__':
    data = pd.read_csv(COURSE_DATABASE) # .iloc[:8, :]
    courses = get_courses(data)
    representative_times, number_to_real_date_dict = make_domain('2022/01/15', '2022/03/08')
    n_courses, n_times, courses_to_rows_dict, times_to_cols_dict, reverse_times_to_cols_dict = preprocess_courses(
        courses, representative_times)
    for i in range(100):
        solver = SimulatedAnnealingSolver(n_courses, n_times, courses_to_rows_dict, times_to_cols_dict,
                                          reverse_times_to_cols_dict, None, 0.85, cooling_function)
        solver.solve()
        # print(solver.get_state())
        print(solver.get_state().check_duplicates())


