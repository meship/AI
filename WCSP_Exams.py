from WCSP import WCSP
import itertools
from WCSP_Exam_Constraint import WCSP_Constraint
import queue
from Constants import *


class WCSP_Exams(WCSP):
    def __init__(self, variables, domains, change_periods_date):
        # CSP.__init__(self, variables, domains)
        self.variables = variables  # variables to be constrained
        self.domains = dict()  # domain of each variable
        self.constraints = dict()
        for variable in self.variables:
            self.constraints[variable] = []
            if variable.get_attempt() == MOED_A:
                self.domains[variable] = domains[:change_periods_date + 1]
            else:
                self.domains[variable] = domains[change_periods_date + 1:]

        self.days_difference = {'CS': CS_EXAM_DIFFERENCE,
                                'EE': EE_EXAM_DIFFERENCE,
                                'M': M_EXAM_DIFFERENCE,
                                'CB': CB_EXAM_DIFFERENCE}

        self.exam_period_time = int(max(domains))
        pairs_permutations = list(itertools.permutations(self.variables, 2))
        self.pairs_difference = dict()
        for pair in pairs_permutations:
            self.calculate_days_(pair)

    def calculate_days_(self, pair):
        for faculty in self.days_difference:
            if faculty in pair[0].get_faculties() and faculty in pair[1].get_faculties():
                self.pairs_difference[pair] = max([self.days_difference[val] for val in pair[1].get_faculties()])
                return
        self.pairs_difference[pair] = 0

    def create_constraints(self):
        # first hard constrain - each time slot has at most one exam scheduled to it
        pairs_combinations = list(itertools.combinations(self.variables, 2))
        for pair in pairs_combinations:
            self.add_constraint(WSCP_Exam_Constraint(pair, self.maximum_cost, HARD, EXAMS_ON_DIFFERENT_DAYS_CONSTRAINT))

        # # second hard constrain - each exam must be scheduled
        # for variable in self.variables:
        #     self.add_constraint(WSCP_Exam_Constraint((variable,), EACH_EXAM_HAS_A_DATE_CONSTRAINT))
        #
        # # third hard constrain:
        # #  --> between CS courses we demand at least 6 days
        # #  --> between EE courses we demand at least 6 days
        # #  --> between Math courses we demand at least 7 days
        # #  --> between CB courses we demand at least 4 days
        #
        # for pair, max_days in self.pairs_difference.items():
        #     if max_days:
        #         self.add_constraint(WSCP_Exam_Constraint(pair, DAYS_DIFFERENCE_ON_COMMON_FACULTIES_CONSTRAINT, max_days))
        #
        # # forth hard constrain - At least 14 days between moed A and moed B of the same course
        # for pair in pairs_combinations:
        #     if pair[0].get_name()[:-1] == pair[1].get_name()[:-1]:
        #         self.add_constraint(WSCP_Exam_Constraint(pair, MOED_A_AND_B_DIFFERENCE_CONSTRAINT))

        # First soft constraints  - Math exams only on mornings
        for variable in self.variables:
            if 'M' in variable.get_faculties():
                self.add_constraint(WSCP_Exam_Constraint((variable,), MATH_EXAMS_ON_MORNING_COST, SOFT, MATH_EXAMS_ON_MORNING))


