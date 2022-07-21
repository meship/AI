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

        self.exam_period_time = int(max(domains))

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
            if (pair[0].get_attempt() == 1 and pair[1].get_attempt() == 2) or \
                    (pair[0].get_attempt() == 2 and pair[1].get_attempt() == 1):
                self.add_constraint(ExamConstraint(pair, 4))

        # fifth hard constrain - At least 14 days between moed A and moed B of the same course
        for pair in pairs_combinations:
            if pair[0].get_name()[:-1] == pair[1].get_name()[:-1]:
                self.add_constraint(ExamConstraint(pair, 5))

    def shrink_domain(self, cur_assignment, shrank_domain, assigned_variable):
        for var in self.variables:
            shrank_domain[var] -= {cur_assignment}
            if var != assigned_variable:
                start_boundary = max(1, int(cur_assignment) - self.calculate_days_((var, assigned_variable)))
                end_boundary = min(self.exam_period_time, int(cur_assignment) +
                                   self.calculate_days_((assigned_variable, var)))
                for day in range(start_boundary, end_boundary + 1):
                    shrank_domain[var] -= {day + 0.1, day + 0.2, day + 0.3}

                if var.attempt == 2 and assigned_variable.attempt == 1:
                    for day in range(1, cur_assignment + 1):
                        shrank_domain[var] -= {day + 0.1, day + 0.2, day + 0.3}

                if var.get_name()[:-1] == cur_assignment.get_name()[:-1]:
                    if var.attempt == 2:
                        for day in range(cur_assignment, cur_assignment + 15):
                            shrank_domain[var] -= {day + 0.1, day + 0.2, day + 0.3}
                    else:
                        for day in range(cur_assignment - 14, cur_assignment + 1):
                            shrank_domain[var] -= {day + 0.1, day + 0.2, day + 0.3}
        return shrank_domain






