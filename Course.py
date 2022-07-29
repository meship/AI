from Constants import *

class Course:
    def __init__(self, name, number, faculties, type, credits, attempt, change_periods_date=None):
        self.name_ = name
        self.number_ = number
        self.faculties_ = faculties.split(", ")
        self.type_ = type
        self.credits_ = credits
        self.attempt_ = attempt
        self.exam_time_ = 0
        self.change_periods_date_ = change_periods_date
        self.exam_id_ = None

    def get_name(self):
        return self.name_

    def get_number(self):
        return self.number_

    def get_faculties(self):
        return self.faculties_

    def get_type(self):
        return self.type_

    def get_credits(self):
        return self.credits_

    def get_attempt(self):
        return self.attempt_

    def get_exam_time(self):
        return self.exam_time_

    def get_change_periods_date(self):
        return self.change_periods_date_

    def get_exam_id(self):
        return self.exam_id_

    def set_exam_time(self, time):
        self.exam_time_ = time

    def set_exam_id(self, exam_id):
        self.exam_id_ = exam_id

    def __repr__(self):
        return self.name_


