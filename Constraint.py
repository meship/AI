# Base class for all constraints
from abc import ABC, abstractmethod


class Constraint(ABC):
    # The variables that the constraint is between
    def __init__(self, variables):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment):
        ...
