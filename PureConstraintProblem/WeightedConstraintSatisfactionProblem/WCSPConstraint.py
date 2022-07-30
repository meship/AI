from abc import abstractmethod
from Utils.Constants import *
from PureConstraintProblem.Constraint import Constraint


class WCSPConstraint(Constraint):
    def __init__(self, variables, cost, constraint_type=HARD):
        super().__init__(variables)
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
    def get_cost(self, assignment):
        ...
