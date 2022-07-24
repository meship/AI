# Press the green button in the gutter to run the script.
import numpy as np
from Constants import *
import copy
from abc import ABC, abstractmethod


class WCSP(ABC):
    def __init__(self, variables, domains, k):
        self.variables = variables  # variables to be constrained
        self.domains = dict()  # domain of each variable
        self.constraints = dict()
        for variable in self.variables:
            self.constraints[variable] = []
            self.domains[variable] = domains.copy()
        self.maximum_cost = k
        self.operator = lambda x, y: min(self.maximum_cost, x + y)
        self.valuation_structure = (list(range(self.maximum_cost)), self.operator)
        self.upper_bound = None
        self.best_assignment = None

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

    def branch_and_bound(self, assignment, total_cost, variables):
        if not len(variables):
            if self.upper_bound is None or self.upper_bound > total_cost:
                self.upper_bound = total_cost
                self.best_assignment = assignment

        chosen_variable = variables[0]
        for value in self.domains[chosen_variable]:
            assignment[chosen_variable] = value
            total_assignment_cost = total_cost + sum([constraint.get_cost(value) for constraint in self.constraints[chosen_variable]])
            if total_assignment_cost > self.upper_bound:
                return
            return self.branch_and_bound(assignment, total_cost + total_assignment_cost, variables[1:])


