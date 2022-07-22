from CSP import CSP
import itertools
from ExamConstraint import ExamConstraint
import queue
import numpy as np

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
            self.add_constraint(ExamConstraint(pair, 1))

        # second hard constrain - each exam must be scheduled
        for variable in self.variables:
            self.add_constraint(ExamConstraint((variable,), 2))

        # third hard constrain:
        #  --> between CS courses we demand at least 6 days
        #  --> between EE courses we demand at least 6 days
        #  --> between Math courses we demand at least 7 days
        #  --> between CB courses we demand at least 4 days

        for pair, max_days in self.pairs_difference.items():
            # print(f"Pair is:{pair} and difference is: {max_days}")
            if max_days:
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

    def shrink_domain(self, cur_assignment, shrank_domain, assigned_variable, unassigned_variables):
        for var in unassigned_variables:
            elements_to_remove = set()
            elements_to_remove = elements_to_remove.union({cur_assignment})
            int_cur_assignment = int(cur_assignment)
            if var != assigned_variable:
                # np_domain = np.array(list(shrank_domain[var]))
                start_boundary = max(1, int_cur_assignment - self.pairs_difference[(var, assigned_variable)])
                end_boundary = min(self.exam_period_time, int_cur_assignment +
                                   self.pairs_difference[(assigned_variable, var)])
                for day in range(start_boundary, end_boundary + 1):
                    elements_to_remove.add(day + 0.1)
                    elements_to_remove.add(day + 0.2)
                    elements_to_remove.add(day + 0.3)

                if var.get_attempt() == 2 and assigned_variable.get_attempt() == 1:
                    # for day in range(1, int_cur_assignment + 1):
                    #     elements_to_remove.add(day + 0.1)
                    #     elements_to_remove.add(day + 0.2)
                    #     elements_to_remove.add(day + 0.3)
                    # np_domain = np_domain[np_domain > cur_assignment + 0.3]
                    for day in self.domains[var]:
                        if day > int_cur_assignment:
                            continue
                        elements_to_remove.add(day)

                if var.get_name()[:-1] == assigned_variable.get_name()[:-1]:
                    if var.get_attempt() == 2:
                        for day in range(int_cur_assignment, int_cur_assignment + 15):
                            elements_to_remove.add(day + 0.1)
                            elements_to_remove.add(day + 0.2)
                            elements_to_remove.add(day + 0.3)
                        # np_domain = np_domain[np_domain > cur_assignment + 13.3]
                    else:
                        for day in range(int_cur_assignment - 14, int_cur_assignment + 1):
                            elements_to_remove.add(day + 0.1)
                            elements_to_remove.add(day + 0.2)
                            elements_to_remove.add(day + 0.3)
                        # np_domain = np_domain[(np_domain < cur_assignment - 13.3) & (np_domain > cur_assignment)]
                # shrank_domain[var] = set(np_domain)
                new_set = shrank_domain[var] - elements_to_remove
                shrank_domain[var] = new_set
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
                self.domains[X_i].remove(x)
                removed = True
        return removed

    def get_neighbors(self, current_variable):
        neighbors = set()
        for constraint in self.constraints[current_variable]:
            if constraint.kind != 2:
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


