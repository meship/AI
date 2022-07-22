# Press the green button in the gutter to run the script.
import numpy as np
import copy
import itertools
import queue
from abc import ABC, abstractmethod


class CSP(ABC):
    def __init__(self, variables, domains):
        self.variables = variables  # variables to be constrained
        self.domains = dict()  # domain of each variable
        self.constraints = dict()
        for variable in self.variables:
            self.constraints[variable] = []
            self.domains[variable] = domains.copy()

    def add_constraint(self, constraint):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)

    def consistent(self, variable, assignment):
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking_search(self, assignment={}):
        # assignment is complete if every variable is assigned (our base case)
        if len(assignment) == len(self.variables):
            return assignment

        # get all variables in the CSP but not in the assignment
        unassigned = [v for v in self.variables if v not in assignment]

        # get the every possible domain value of the first unassigned variable
        first = unassigned[0]
        for value in self.domains[first]:
            if not value:
                continue
            local_assignment = assignment.copy()
            local_assignment[first] = value
            # if we're still consistent, we recurse (continue)
            if self.consistent(first, local_assignment):
                result = self.backtracking_search(local_assignment)
                # if we didn't find the result, we will end up backtracking
                if result is not None:
                    return result
        return None

    def find_var_to_assign_by_domain(self, unassigned, shrank_domain):
        min_len = np.Inf
        min_var = None
        for var in unassigned:
            if var.get_attempt() == 2:
                continue
            domain_len = len(shrank_domain[var])
            if domain_len < min_len:
                min_len = domain_len
                min_var = var

        if min_var is None:
            for var in unassigned:
                domain_len = len(shrank_domain[var])
                if domain_len < min_len:
                    min_len = domain_len
                    min_var = var
        return min_var

    def find_var_to_assign_by_constraint(self, unassigned):
        max_len = 0
        max_var = None
        for var in unassigned:
            constraint_len = len(self.constraints[var])
            if constraint_len > max_len:
                max_len = constraint_len
                max_var = var
        return max_var

    def choose_best_value(self, chosen_variable, unassigned_variables, domains):
        value_and_domain_len = []
        for value in domains[chosen_variable]:
            new_domain = self.shrink_domain(value, domains.copy(), chosen_variable, unassigned_variables)
            new_domain_len = sum(len(var_domain) for var_domain in new_domain.values())
            value_and_domain_len.append((value, new_domain_len))
        return sorted(value_and_domain_len, key=lambda x: x[1], reverse=True)


    @abstractmethod
    def shrink_domain(self, cur_assignment, shrank_domain, assigned_variable):
        ...

    def minimum_remaining_vars(self, assignment, shrank_domain):
        # assignment is complete if every variable is assigned (our base case)
        if len(assignment) == len(self.variables):
            return assignment

        # get all variables in the CSP but not in the assignment
        unassigned = [v for v in self.variables if v not in assignment]

        # get the every possible domain value of the first unassigned variable
        first = self.find_var_to_assign_by_domain(unassigned, shrank_domain)
        # first = unassigned[0]
        # copy_of_first_domain = shrank_domain[first].copy()
        for value in shrank_domain[first]:
            if not value:
                continue
            local_assignment = assignment.copy()
            # to_shrink_domain = copy.deepcopy(shrank_domain)
            to_shrink_domain = shrank_domain.copy()
            local_assignment[first] = value
            to_shrink_domain = self.shrink_domain(value, to_shrink_domain, first, unassigned)
            # if we're still consistent, we recurse (continue)
            if self.consistent(first, local_assignment):
                result = self.minimum_remaining_vars(local_assignment, to_shrink_domain)
                # if we didn't find the result, we will end up backtracking
                if result is not None:
                    return result
        return None

    def degree_heuristic(self, assignment={}):
        # assignment is complete if every variable is assigned (our base case)
        if len(assignment) == len(self.variables):
            return assignment

        # get all variables in the CSP but not in the assignment
        unassigned = [v for v in self.variables if v not in assignment]

        # get the every possible domain value of the first unassigned variable
        first = self.find_var_to_assign_by_constraint(unassigned)
        for value in self.domains[first]:
            if not value:
                continue
            local_assignment = assignment.copy()
            local_assignment[first] = value
            # if we're still consistent, we recurse (continue)
            if self.consistent(first, local_assignment):
                result = self.degree_heuristic(local_assignment)
                # if we didn't find the result, we will end up backtracking
                if result is not None:
                    return result
        return None

    def least_constraining_value(self, assignment={}):
        # assignment is complete if every variable is assigned (our base case)
        if len(assignment) == len(self.variables):
            return assignment

        # get all variables in the CSP but not in the assignment
        unassigned = [v for v in self.variables if v not in assignment]

        # get the every possible domain value of the first unassigned variable
        first = unassigned[0]
        ordered_values = self.choose_best_value(first, unassigned, self.domains)
        for value in ordered_values:
            if not value:
                continue
            local_assignment = assignment.copy()
            local_assignment[first] = value[0]
            # if we're still consistent, we recurse (continue)
            if self.consistent(first, local_assignment):
                result = self.backtracking_search(local_assignment)
                # if we didn't find the result, we will end up backtracking
                if result is not None:
                    return result
        return None


    def both_heuristics(self, assignment, shrank_domain):
        # assignment is complete if every variable is assigned (our base case)
        if len(assignment) == len(self.variables):
            return assignment

        # get all variables in the CSP but not in the assignment
        unassigned = [v for v in self.variables if v not in assignment]

        # get the every possible domain value of the first unassigned variable
        first = self.find_var_to_assign_by_domain(unassigned, shrank_domain)
        ordered_values = self.choose_best_value(first, unassigned, shrank_domain)
        for value in ordered_values:
            if not value[0]:
                continue
            local_assignment = assignment.copy()
            # to_shrink_domain = copy.deepcopy(shrank_domain)
            to_shrink_domain = shrank_domain.copy()
            local_assignment[first] = value[0]
            to_shrink_domain = self.shrink_domain(value[0], to_shrink_domain, first, unassigned)
            # if we're still consistent, we recurse (continue)
            if self.consistent(first, local_assignment):
                result = self.both_heuristics(local_assignment, to_shrink_domain)
                # if we didn't find the result, we will end up backtracking
                if result is not None:
                    return result
        return None




