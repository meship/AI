from CSP import CSP
import itertools
from ExamConstraint import ExamConstraint
import queue

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

    def shrink_domain(self, cur_assignment, shrank_domain, assigned_variable):

        for var in self.variables:
            new_domain = set()
            new_domain = new_domain.union({cur_assignment})
            int_cur_assignment = int(cur_assignment)
            if var != assigned_variable:
                start_boundary = max(1, int_cur_assignment - self.calculate_days_((var, assigned_variable)))
                end_boundary = min(self.exam_period_time, int_cur_assignment +
                                   self.calculate_days_((assigned_variable, var)))
                for day in range(start_boundary, end_boundary + 1):
                    new_domain -= {day + 0.1, day + 0.2, day + 0.3}

                # if var.get_attempt() == 2 and assigned_variable.get_attempt() == 1:
                #     for day in range(1, int_cur_assignment + 1):
                #         new_domain -= {day + 0.1, day + 0.2, day + 0.3}
                #
                # if var.get_name()[:-1] == assigned_variable.get_name()[:-1]:
                #     if var.get_attempt() == 2:
                #         for day in range(int_cur_assignment, int_cur_assignment + 15):
                #             new_domain -= {day + 0.1, day + 0.2, day + 0.3}
                #     else:
                #         for day in range(int_cur_assignment - 14, int_cur_assignment + 1):
                #             new_domain -= {day + 0.1, day + 0.2, day + 0.3}
            new_set = shrank_domain[var] - new_domain
            shrank_domain[var] = new_set
        return shrank_domain

    def remove_inconsistent_values(self, X_i, X_j):
        removed = False
        union_constraints = self.constraints[X_i] + self.constraints[X_j]
        common_constraints = list()
        for constraint in union_constraints:
            if X_i in constraint.variables and X_j in constraint.variables:
                common_constraints.append(constraint)

        for index in range(len(self.domains[X_i])):
            x = self.domains[X_i][index]
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
                neighbors.add(set(constraint.variables))
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





