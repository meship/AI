# Press the green button in the gutter to run the script.
import numpy as np
import copy
from abc import ABC, abstractmethod


class CSP(ABC):
    def __init__(self, variables, domains):
        self.variables = variables  # variables to be constrained
        self.domains = dict()  # domain of each variable
        self.constraints = dict()
        for variable in self.variables:
            self.constraints[variable] = []
            self.domains[variable] = domains
        #     if variable not in self.domains:
        #         raise LookupError("Every variable should have a domain assigned to it.")

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
        self.domains[first].remove(0)
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            # if we're still consistent, we recurse (continue)
            if self.consistent(first, local_assignment):
                result = self.backtracking_search(local_assignment)
                # if we didn't find the result, we will end up backtracking
                if result is not None:
                    return result
        return None

    def find_var_to_assign(self, unassigned):
        min_len = np.Inf
        min_var = None
        for var in unassigned:
            domain_len = len(self.domains[var])
            if domain_len < min_len:
                min_len = domain_len
                min_var = var
        return min_var

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
        first = self.find_var_to_assign(unassigned)
        self.domains[first].remove(0)
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            shrank_domain = shrank_domain.copy()
            local_assignment[first] = value
            shrank_domain = self.shrink_domain(value, shrank_domain, first)
            # if we're still consistent, we recurse (continue)
            if self.consistent(first, local_assignment):
                result = self.minimum_remaining_vars(local_assignment, shrank_domain)
                # if we didn't find the result, we will end up backtracking
                if result is not None:
                    return result
        return None



