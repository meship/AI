import itertools
from Constants import *


class GeneticAlgorithmState:
    def __init__(self, n_courses, n_times, courses_to_rows_dict,
                 times_to_cols_dict, reverse_times_to_cols_dict, assignment_dict,
                 should_initialize, times_to_dates_dict):
        self.n_courses = n_courses
        self.n_times = n_times
        self.courses_dict = courses_to_rows_dict  # mapping courses objects to their indices
        self.times_dict = times_to_cols_dict  # mapping "representative times" to their indices
        self.reverse_times_dict = reverse_times_to_cols_dict  # mapping indices to their "representative" times
        if should_initialize:
            self.assignment_dict = dict()  # mapping from courses indices to times indices
            while self.initialize_state() == 0:
                self.assignment_dict = dict()
        else:
            self.assignment_dict = assignment_dict  # mapping from courses indices to times indices

        self.days_difference = {'CS': (CS_EXAM_DIFFERENCE_A, CS_EXAM_DIFFERENCE_B),
                                'EE': (EE_EXAM_DIFFERENCE_A, EE_EXAM_DIFFERENCE_B),
                                'M': (M_EXAM_DIFFERENCE_A, M_EXAM_DIFFERENCE_B),
                                'CB': (CB_EXAM_DIFFERENCE_A, CB_EXAM_DIFFERENCE_B),
                                'ST': (ST_EXAM_DIFFERENCE_A, ST_EXAM_DIFFERENCE_B),
                                'E': (E_EXAM_DIFFERENCE_A, E_EXAM_DIFFERENCE_B),
                                'P': (P_EXAM_DIFFERENCE_A, P_EXAM_DIFFERENCE_B),
                                'PS': (PS_EXAM_DIFFERENCE_A, PS_EXAM_DIFFERENCE_B),
                                'CSM': (CSM_EXAM_DIFFERENCE_A, CSM_EXAM_DIFFERENCE_B),
                                'CSE': (CSE_EXAM_DIFFERENCE_A, CSE_EXAM_DIFFERENCE_B),
                                'CSP': (CSP_EXAM_DIFFERENCE_A, CSP_EXAM_DIFFERENCE_B),
                                'PSB': (PSB_EXAM_DIFFERENCE_A, PSB_EXAM_DIFFERENCE_B)}
        pairs_permutations = list(itertools.permutations(self.courses_dict.keys(), 2))
        self.pairs_difference = dict()
        for pair in pairs_permutations:
            self.calculate_days_(pair)
        self.times_to_days_dict = times_to_dates_dict


    def __eq__(self, other):
        eq_count = 0
        for course_ind in self.assignment_dict.keys():
            if self.assignment_dict[course_ind] == other.assignment_dict[course_ind]:
                eq_count += 1
        return eq_count == self.n_courses
