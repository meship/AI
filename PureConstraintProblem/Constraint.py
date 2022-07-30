from abc import ABC, abstractmethod


class Constraint(ABC):
    def __init__(self, variables):
        self.variables_ = variables

    @abstractmethod
    def satisfied(self, assignment):
        ...
