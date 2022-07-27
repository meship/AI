from CSP import CSP
import itertools
from ExamConstraint import ExamConstraint
import queue
from Constants import *


class CSPExams(CSP):
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
        # first hard constraint - each time slot has at most one exam scheduled to it
        pairs_combinations = list(itertools.combinations(self.variables, 2))
        for pair in pairs_combinations:
            self.add_constraint(ExamConstraint(pair, EXAMS_ON_DIFFERENT_DAYS_CONSTRAINT))

        # second hard constraint - each exam must be scheduled
        for variable in self.variables:
            self.add_constraint(ExamConstraint((variable,), EACH_EXAM_HAS_A_DATE_CONSTRAINT))

        # third hard constrain:
        #  --> between CS courses we demand at least 6 days
        #  --> between EE courses we demand at least 6 days
        #  --> between Math courses we demand at least 7 days
        #  --> between CB courses we demand at least 4 days

        for pair, max_days in self.pairs_difference.items():
            if max_days:
                self.add_constraint(ExamConstraint(pair, DAYS_DIFFERENCE_ON_COMMON_FACULTIES_CONSTRAINT, max_days))

        # forth hard constrain - At least 14 days between moed A and moed B of the same course
        for pair in pairs_combinations:
            if pair[0].get_name()[:-1] == pair[1].get_name()[:-1]:
                self.add_constraint(ExamConstraint(pair, MOED_A_AND_B_DIFFERENCE_CONSTRAINT))

    def shrink_domain(self, cur_assignment, shrank_domain, assigned_variable, unassigned_variables):
        for var in unassigned_variables:
            int_cur_assignment = int(cur_assignment)
            if var != assigned_variable:
                first_day = self.domains[var][1]
                final_day = self.domains[var][-1]

                start_boundary = final_day + EVENING_EXAM
                end_boundary = first_day

                if self.pairs_difference[(var, assigned_variable)]:
                    start_boundary = max(first_day, int_cur_assignment - self.pairs_difference[(var, assigned_variable)])

                if self.pairs_difference[(assigned_variable, var)]:
                    end_boundary = min(final_day, int_cur_assignment +
                                       self.pairs_difference[(assigned_variable, var)])

                if var.get_name()[:-1] == assigned_variable.get_name()[:-1]:
                    if var.get_attempt() == MOED_B:
                        start_boundary = first_day
                        end_boundary = cur_assignment + MIN_ATTEMPTS_DIFFERENCE - 1 + EVENING_EXAM
                    else:
                        start_boundary = int(cur_assignment) - MIN_ATTEMPTS_DIFFERENCE
                        end_boundary = final_day

                updated_domain = self.domains[var][(self.domains[var] < start_boundary) | (self.domains[var] > end_boundary)]

                shrank_domain[var] = updated_domain
        return shrank_domain

    def remove_inconsistent_values(self, X_i, X_j):
        removed = False
        union_constraints = self.constraints[X_i] + self.constraints[X_j]
        common_constraints = list()
        for constraint in union_constraints:
            if X_i in constraint.variables and X_j in constraint.variables:
                common_constraints.append(constraint)

        for x in self.domains[X_i].copy():
            for y in self.domains[X_j]:
                is_satisfied = True
                for constraint in common_constraints:
                    is_satisfied = is_satisfied and constraint.satisfied({X_i: x, X_j: y})
                if is_satisfied:
                    break
            else:
                self.domains[X_i] = self.domains[X_i][self.domains[X_i] != x]
                removed = True
        return removed

    def get_neighbors(self, current_variable):
        neighbors = set()
        for constraint in self.constraints[current_variable]:
            if constraint.kind not in {EACH_EXAM_HAS_A_DATE_CONSTRAINT}:
                neighbors.update(set(constraint.variables))
        return list(neighbors - {current_variable})

    def arc3(self):
        arcs_queue = queue.Queue()
        for pair in itertools.combinations(self.variables, 2):
            arcs_queue.put(pair)

        while not arcs_queue.empty():
            X_i, X_j = arcs_queue.get()
            if self.remove_inconsistent_values(X_i, X_j):
                X_i_neighbors = self.get_neighbors(X_i)
                for neighbor in X_i_neighbors:
                    arcs_queue.put((neighbor, X_i))


