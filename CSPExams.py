from CSP import CSP
import itertools
from ExamConstraint import ExamConstraint

CS_EXAM_DIFFERENCE = 6
EE_EXAM_DIFFERENCE = 6
M_EXAM_DIFFERENCE = 7
CB_EXAM_DIFFERENCE = 4


class CSPExams(CSP):

    def __init__(self, variables, domains):
        CSP.__init__(self, variables, domains)
        self.days_difference = {'CS': CS_EXAM_DIFFERENCE,
                                'EE': EE_EXAM_DIFFERENCE,
                                'M': M_EXAM_DIFFERENCE,
                                'CB': CB_EXAM_DIFFERENCE}

    def calculate_days_(self, pair):
        for faculty in self.days_difference:
            if faculty in pair[0].get_faculties() and faculty in pair[1].get_faculties():
                return max([self.days_difference[val] for val in pair[1].get_faculties()])
        return 0

    def create_constraints(self):
        # first hard constrain - each time slot has at most one exam scheduled to it
        pairs_combinations = list(itertools.combinations(self.variables, 2))
        for pair in pairs_combinations:
            self.add_constraint(ExamConstraint(pair, 1))

        # second hard constrain - each exam must be scheduled
        for variable in self.variables:
            self.add_constraint(ExamConstraint((variable,), 2))

        # third hard constrain:
        #  --> between CS courses we demand at least 6 days
        #  --> between EE courses we demand at least 6 days
        #  --> between Math courses we demand at least 7 days
        #  --> between CB courses we demand at least 4 days
        pairs_permutations = list(itertools.permutations(self.variables, 2))
        for pair in pairs_permutations:
            max_days = self.calculate_days_(pair)
            # print(f"Pair is:{pair} and difference is: {max_days}")
            self.add_constraint(ExamConstraint(pair, 3, max_days))

        # forth hard constrain - Moed B period starts after the last Moed A
        for pair in pairs_combinations:
            if (pair[0].get_attempt() == 1 and pair[1].get_attempt() == 2) or\
                    (pair[0].get_attempt() == 2 and pair[1].get_attempt() == 1):
                self.add_constraint(ExamConstraint(pair, 4))

        # fifth hard constrain - At least 14 days between moed A and moed B of the same course
        for pair in pairs_combinations:
            if pair[0].get_name()[:-1] == pair[1].get_name()[:-1]:
                self.add_constraint(ExamConstraint(pair, 5))


