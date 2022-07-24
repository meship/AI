from WCSP_Constraint import WCSP_Constraint
from Constants import *


class ExamConstraint(WCSP_Constraint):

    def __init__(self, variables, cost, constraint_type, kind, max_days=0):
        WCSP_Constraint.__init__(self, variables, constraint_type, cost)
        self.kind = kind
        self.max_days = max_days

    def hard_satisfied_1(self, assignment):
        if self.variables_[0] not in assignment or self.variables_[1] not in assignment:
            self.is_satisfied_ = True
            return
        self.is_satisfied_ = assignment[self.variables_[0]] != assignment[self.variables_[1]]

    def hard_satisfied_2(self, assignment):
        self.is_satisfied_ = assignment[self.variables_[0]] != 0

    def hard_satisfied_3(self, assignment):
        if self.variables_[0] not in assignment or self.variables_[1] not in assignment:
            self.is_satisfied_ = True
            return
        self.is_satisfied_ = abs(int(assignment[self.variables_[0]]) - int(assignment[self.variables_[1]])) >= self.max_days_

    def hard_satisfied_4(self, assignment):
        moed_a = self.variables_[0] if self.variables_[0].get_attempt() == MOED_A else self.variables_[1]
        moed_b = self.variables_[0] if self.variables_[0].get_attempt() == MOED_B else self.variables_[1]
        if moed_a not in assignment or moed_b not in assignment:
            self.is_satisfied_ = True
            return
        self.is_satisfied_ = int(assignment[moed_b]) - int(assignment[moed_a]) >= MIN_ATTEMPTS_DIFFERENCE

    def soft_satisfied_1(self, assignment):
        self.is_satisfied_ = assignment[self.variables_[0]] - int(assignment[self.variables_[0]]) == MORNING_EXAM

    def hard_satisfied(self, assignment):
        if self.kind == EXAMS_ON_DIFFERENT_DAYS_CONSTRAINT:
            self.hard_satisfied_1(assignment)
        elif self.kind == EACH_EXAM_HAS_A_DATE_CONSTRAINT:
            self.hard_satisfied_2(assignment)
        elif self.kind == DAYS_DIFFERENCE_ON_COMMON_FACULTIES_CONSTRAINT:
            self.hard_satisfied_3(assignment)
        elif self.kind == MOED_A_AND_B_DIFFERENCE_CONSTRAINT:
            self.hard_satisfied_4(assignment)

    def soft_satisfied(self, assignment):
        if self.kind == MATH_EXAMS_ON_MORNING:
            self.soft_satisfied_1(assignment)

    def satisfied(self, assignment):
        if self.type_ == HARD:
            self.hard_satisfied(assignment)
        else:
            self.soft_satisfied(assignment)
        return self.get_is_satisfied()

    def get_cost(self, value):
        if self.type_ == HARD:
            return 0 if self.is_satisfied_ else MAXIMUM_COST
        else:
            return 0 if self.is_satisfied_ else self.cost_






