import random

from InformedSearchAlgorithms.ISAState import ISAState
from InformedSearchAlgorithms.ISAHallState import ISAHallState
from Utils.Constants import *


class SimulatedAnnealingSolver:

    def __init__(self, n_courses, n_times, courses_to_rows_dict, reverse_courses_dict,
                 times_to_cols_dict, reverse_times_to_cols_dict, assignment_dict, times_to_days_dict,
                 alpha, cooling_function, max_iter=5000, callback=None, complex_callback=None,
                 complex_problem=False, n_halls=None, halls_to_cols_dict=None,  reverse_halls_to_cols_dict=None,
                 time_assignment_dict=None):
        self.initial_temperature_ = 1
        self.alpha_ = alpha
        self.cooling_function_ = cooling_function
        self.max_iter_ = max_iter
        self.callback = callback
        self.complex_problem = complex_problem
        self.complex_callback = complex_callback
        if not complex_problem:
            self.state_ = ISAState(n_courses, n_times, courses_to_rows_dict, reverse_courses_dict,
                                   times_to_cols_dict, reverse_times_to_cols_dict, assignment_dict, {},
                                   times_to_days_dict, True)
        else:
            self.state_ = ISAHallState(n_courses, n_times, n_halls, courses_to_rows_dict, reverse_courses_dict,
                                       halls_to_cols_dict, reverse_halls_to_cols_dict, time_assignment_dict, True)

    def solve(self):
        temperature = self.initial_temperature_
        for t in range(self.max_iter_):
            if self.callback:
                self.callback(self.state_.get_value(), temperature)
            if self.complex_callback:
                self.complex_callback(self.state_.get_value(), temperature)
            if temperature == 0:
                # print("here!!!!!!!!!!")
                return
            next_state = self.state_.generate_successor()
            delta = next_state.get_value() - self.state_.get_value()
            if delta < 0:
                self.state_ = next_state
            # else:
            #     val = random.uniform(0, 1)
            #     if val < np.exp(-delta/temperature):
            #         self.state_ = next_state
            temperature = self.cooling_function_(self.initial_temperature_, self.alpha_, t)

    def get_state(self):
        return self.state_



