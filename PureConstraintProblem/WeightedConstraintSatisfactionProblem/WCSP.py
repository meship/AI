from Utils.Constants import *
from PureConstraintProblem.ConstriantSatisfactionProblem.CSP import CSP
# from abc import ABC


class WCSP(CSP):
    def __init__(self, variables, domains, k):
        # self.variables_ = variables  # variables to be constrained
        # self.domains_ = dict()  # domain of each variable
        # self.constraints_ = dict()
        # for variable in self.variables_:
        #     self.constraints_[variable] = []
        #     self.domains_[variable] = domains.copy()
        super().__init__(variables, domains)
        self.maximum_cost_ = k
        self.operator_ = lambda x, y: min(self.maximum_cost_, x + y)
        self.valuation_structure_ = (list(range(self.maximum_cost_)), self.operator_)
        self.upper_bound_ = None
        self.best_assignment_ = None
        self.best_assignment_flag_ = False

    # def add_constraint(self, constraint):
    #     for variable in constraint.variables_:
    #         if variable not in self.variables_:
    #             raise LookupError("Variable in constraint not in PureConstraintProblem")
    #         else:
    #             self.constraints_[variable].append(constraint)

    # def consistent(self, variable, assignment):
    #     for constraint in self.constraints_[variable]:
    #         if not constraint.satisfied(assignment):
    #             return False
    #     return True

    def branch_and_bound(self, assignment, total_cost, depth):
        if depth == len(self.variables_):
            if self.upper_bound_ is None or self.upper_bound_ > total_cost:
                self.upper_bound_ = total_cost
                self.best_assignment_ = assignment
                print(assignment)
                print(total_cost)
            if self.upper_bound_ == 0:
                self.best_assignment_flag_ = True
            return

        chosen_variable = self.variables_[depth]
        for value in self.domains_[chosen_variable]:
            if value == 0.0:
                continue
            assignment[chosen_variable] = value
            total_assignment_cost = total_cost
            for constraint in self.constraints_[chosen_variable]:
                a = constraint.get_cost(assignment)
                total_assignment_cost += a
            # total_assignment_cost = total_cost + sum([constraint.get_cost(assignment) for constraint in self.constraints_[chosen_variable]])
            if self.upper_bound_ is not None and total_assignment_cost > self.upper_bound_:
                return
            if total_assignment_cost >= np.inf:
                continue
            self.branch_and_bound(assignment.copy(), total_assignment_cost, depth + 1)
            if self.best_assignment_flag_:
                return
    #
    # def remove_inconsistent_values(self, X_i, X_j):
    #     removed = False
    #     union_constraints = self.constraints_[X_i] + self.constraints_[X_j]
    #     common_constraints = list()
    #     for constraint in union_constraints:
    #         if constraint.type_ == SOFT:
    #             continue
    #         if X_i in constraint.variables_ and X_j in constraint.variables_:
    #             common_constraints.append(constraint)
    #     for x in self.domains_[X_i].copy():
    #         for y in self.domains_[X_j]:
    #             is_satisfied = True
    #             for constraint in common_constraints:
    #                 is_satisfied = is_satisfied and constraint.satisfied({X_i: x, X_j: y})
    #             if is_satisfied:
    #                 break
    #         else:
    #             self.domains_[X_i] = self.domains_[X_i][self.domains_[X_i] != x]
    #             removed = True
    #     return removed
    #
    def get_neighbors_(self, current_variable):
        neighbors = set()
        for constraint in self.constraints_[current_variable]:
            if constraint.kind_ not in {EACH_EXAM_HAS_A_DATE_CONSTRAINT}:
                neighbors.update(set(constraint.variables_))
        return list(neighbors - {current_variable})
    #
    # def arc3(self):
    #     arcs_queue = queue.Queue()
    #     for pair in itertools.combinations(self.variables_, 2):
    #         arcs_queue.put(pair)
    #
    #     while not arcs_queue.empty():
    #         X_i, X_j = arcs_queue.get()
    #         if self.remove_inconsistent_values(X_i, X_j):
    #             X_i_neighbors = self.get_neighbors(X_i)
    #             for neighbor in X_i_neighbors:
    #                 arcs_queue.put((neighbor, X_i))
    #
    #

    def backtracking_search(self, assignments={}):
        pass

    def find_var_to_assign_by_domain_(self, unassigned, shrank_domain):
        pass

    def choose_best_value(self, chosen_variable, unassigned_variables, domains):
        pass

    def shrink_domain(self, cur_assignment, shrank_domain, assigned_variable, unassigned_variables):
        pass

    def minimum_remaining_vars(self, assignment, shrank_domain):
        pass

    def degree_heuristic(self, assignment={}):
        pass

    def least_constraining_value(self, assignment={}):
        pass

    def both_heuristics(self, assignment, shrank_domain):
        pass