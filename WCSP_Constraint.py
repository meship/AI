# Base class for all constraints
from abc import ABC, abstractmethod
from Constants import *


class WCSP_Constraint(ABC):
    # The variables that the constraint is between
    def __init__(self, variables, cost, constraint_type=HARD):
        self.variables_ = variables
        self.type_ = constraint_type
        self.cost_ = cost
        self.is_satisfied_ = None

    def get_variables(self):
        return self.variables_

    def get_is_satisfied(self):
        return self.is_satisfied_

    @abstractmethod
    def satisfied(self, assignment):
        ...

    @abstractmethod
    def get_cost(self, value):
        ...
