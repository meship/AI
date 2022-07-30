from PureConstraintProblem.Constraint import Constraint
from Utils.Constants import *


class ExamConstraint(Constraint):

    def __init__(self, variables, kind, max_days=0):
        Constraint.__init__(self, variables)
        self.kind_ = kind
        self.max_days_ = max_days

    def satisfied_1_(self, assignment):
        if self.variables_[0] not in assignment or self.variables_[1] not in assignment:
            return True
        return assignment[self.variables_[0]] != assignment[self.variables_[1]]

    def satisfied_2_(self, assignment):
        return assignment[self.variables_[0]] != 0

    def satisfied_3_(self, assignment):
        if self.variables_[0] not in assignment or self.variables_[1] not in assignment:
            return True
        return abs(int(assignment[self.variables_[0]]) - int(assignment[self.variables_[1]])) >= self.max_days_

    def satisfied_4_(self, assignment):
        moed_a = self.variables_[0] if self.variables_[0].get_attempt() == MOED_A else self.variables_[1]
        moed_b = self.variables_[0] if self.variables_[0].get_attempt() == MOED_B else self.variables_[1]
        if moed_a not in assignment or moed_b not in assignment:
            return True
        return int(assignment[moed_b]) - int(assignment[moed_a]) >= MIN_ATTEMPTS_DIFFERENCE

    def satisfied(self, assignment):
        if self.kind_ == EXAMS_ON_DIFFERENT_DAYS_CONSTRAINT:
            return self.satisfied_1_(assignment)
        elif self.kind_ == EACH_EXAM_HAS_A_DATE_CONSTRAINT:
            return self.satisfied_2_(assignment)
        elif self.kind_ == DAYS_DIFFERENCE_ON_COMMON_FACULTIES_CONSTRAINT:
            return self.satisfied_3_(assignment)
        elif self.kind_ == MOED_A_AND_B_DIFFERENCE_CONSTRAINT:
            return self.satisfied_4_(assignment)





