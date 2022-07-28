from WCSP import WCSP
import itertools
from WCSP_Exam_Constraint import WCSPExamConstraint
import queue
from Constants import *


class WCSPExams(WCSP):
    def __init__(self, variables, domains, change_periods_date, k):
        # CSP.__init__(self, variables, domains)
        self.variables_ = variables  # variables to be constrained
        self.domains_ = dict()  # domain of each variable
        self.constraints_ = dict()
        for variable in self.variables_:
            self.constraints_[variable] = []
            if variable.get_attempt() == MOED_A:
                self.domains_[variable] = domains[:change_periods_date + 1]
            else:
                self.domains_[variable] = domains[change_periods_date + 1:]

        self.days_difference_ = {'CS': CS_EXAM_DIFFERENCE_A,
                                 'EE': EE_EXAM_DIFFERENCE_A,
                                 'M': M_EXAM_DIFFERENCE_A,
                                 'CB': CB_EXAM_DIFFERENCE_A}

        self.exam_period_time_ = int(max(domains))
        self.maximum_cost_ = k
        # self.operator_ = lambda x, y: min(self.maximum_cost_, x + y)
        # self.valuation_structure_ = (list(range(self.maximum_cost_)), self.operator_)
        self.upper_bound_ = None
        self.best_assignment_ = None
        self.best_assignment_flag_ = False
        pairs_permutations = list(itertools.permutations(self.variables_, 2))
        self.pairs_difference_ = dict()
        for pair in pairs_permutations:
            self.calculate_days_(pair)

    def calculate_days_(self, pair):
        for faculty in self.days_difference_:
            if faculty in pair[0].get_faculties() and faculty in pair[1].get_faculties():
                self.pairs_difference_[pair] = max([self.days_difference_[val] for val in pair[1].get_faculties()])
                return
        self.pairs_difference_[pair] = 0

    def create_constraints(self):
        # first hard constrain - each time slot has at most one exam scheduled to it
        pairs_combinations = list(itertools.combinations(self.variables_, 2))
        for pair in pairs_combinations:
            self.add_constraint(WCSPExamConstraint(pair, self.maximum_cost_, HARD, EXAMS_ON_DIFFERENT_DAYS_CONSTRAINT))

        # second hard constrain - each exam must be scheduled
        for variable in self.variables_:
            self.add_constraint(WCSPExamConstraint((variable,), self.maximum_cost_, HARD,
                                                   EACH_EXAM_HAS_A_DATE_CONSTRAINT))

        # third hard constrain:
        #  --> between CS courses we demand at least 6 days
        #  --> between EE courses we demand at least 6 days
        #  --> between Math courses we demand at least 7 days
        #  --> between CB courses we demand at least 4 days

        for pair, max_days in self.pairs_difference_.items():
            if max_days:
                self.add_constraint(WCSPExamConstraint(pair, self.maximum_cost_, HARD,
                                                       DAYS_DIFFERENCE_ON_COMMON_FACULTIES_CONSTRAINT, max_days))

        # forth hard constrain - At least 14 days between moed A and moed B of the same course
        for pair in pairs_combinations:
            if pair[0].get_name()[:-1] == pair[1].get_name()[:-1]:
                self.add_constraint(WCSPExamConstraint(pair, self.maximum_cost_, HARD,
                                                       MOED_A_AND_B_DIFFERENCE_CONSTRAINT))

        # First soft constraints  - Math exams only on mornings
        for variable in self.variables_:
            if 'M' in variable.get_faculties():
                self.add_constraint(WCSPExamConstraint((variable,), MATH_EXAMS_ON_MORNING_COST, SOFT,
                                                       MATH_EXAMS_ON_MORNING))


