import random

from InformedSearchAlgorithms.ISAState import ISAState
from Utils.Constants import *


class SimulatedAnnealingSolver:

    def __init__(self, n_courses, n_times, courses_to_rows_dict, reverse_courses_dict,
                 times_to_cols_dict, reverse_times_to_cols_dict, assignment_dict, times_to_days_dict,
                 alpha, cooling_function, max_iter=5000, callback=None):
        self.state_ = ISAState(n_courses, n_times, courses_to_rows_dict, reverse_courses_dict,
                               times_to_cols_dict, reverse_times_to_cols_dict, assignment_dict, {},
                               times_to_days_dict, True)
        self.initial_temperature_ = 1
        self.alpha_ = alpha
        self.cooling_function_ = cooling_function
        self.max_iter_ = max_iter
        self.callback = callback

    def solve(self):
        temperature = self.initial_temperature_
        for t in range(self.max_iter_):
            if self.callback:
                self.callback(self.state_.get_value(), temperature)
            if temperature == 0:
                print("here!!!!!!!!!!")
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

    def check_solution_quality(self):
        print("Results: ")
        print(f"Duplicate status: {self.state_.check_duplicates()}")
        print(f"Difference status: ")
        diff_results = self.state_.check_exams_diff()
        for pair, diff in diff_results.items():
            print(f"({pair[0]}, {pair[1]}): {diff}")
        print(f"Number of Friday exams: {self.state_.exam_on_friday_constraint()}")
        print(f"Number of Sunday morning exams: {self.state_.exam_on_sunday_morning_constraint()}")
        print(f"Number of evening exams: {self.state_.exam_on_evening_constraint()}")
        print(f"Number of Math NOT morning exams: {self.state_.math_exam_on_morning_constraint()}")








