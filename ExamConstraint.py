from Constraint import Constraint
from Constants import *


class ExamConstraint(Constraint):

    def __init__(self, variables, kind, max_days=0):
        Constraint.__init__(self, variables)
        self.kind = kind
        self.max_days = max_days

    def satisfied_1(self, assignment):
        if self.variables[0] not in assignment or self.variables[1] not in assignment:
            return True
        return assignment[self.variables[0]] != assignment[self.variables[1]]

    def satisfied_2(self, assignment):
        return assignment[self.variables[0]] != 0

    def satisfied_3(self, assignment):
        if self.variables[0] not in assignment or self.variables[1] not in assignment:
            return True
        return abs(int(assignment[self.variables[0]]) - int(assignment[self.variables[1]])) >= self.max_days

    def satisfied_4(self, assignment):
        moed_a = self.variables[0] if self.variables[0].get_attempt() == MOED_A else self.variables[1]
        moed_b = self.variables[0] if self.variables[0].get_attempt() == MOED_B else self.variables[1]
        if moed_a not in assignment or moed_b not in assignment:
            return True
        return int(assignment[moed_b]) - int(assignment[moed_a]) >= MIN_ATTEMPTS_DIFFERENCE

    def satisfied(self, assignment):
        if self.kind == EXAMS_ON_DIFFERENT_DAYS_CONSTRAINT:
            return self.satisfied_1(assignment)
        elif self.kind == EACH_EXAM_HAS_A_DATE_CONSTRAINT:
            return self.satisfied_2(assignment)
        elif self.kind == DAYS_DIFFERENCE_ON_COMMON_FACULTIES_CONSTRAINT:
            return self.satisfied_3(assignment)
        elif self.kind == MOED_A_AND_B_DIFFERENCE_CONSTRAINT:
            return self.satisfied_4(assignment)





