class Course:
    def __init__(self, name, number, faculties, type, credits, attempt):
        self.name_ = name
        self.number_ = number
        self.faculties_ = faculties.split(", ")
        self.type_ = type
        self.credits_ = credits
        self.attempt_ = attempt
        self.exam_time_ = 0

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

    def set_exam_time(self, time):
        self.exam_time_ = time

    def __repr__(self):
        return self.name_

    # def __eq__(self, o):
    #     return self.name_ == o.get_name()
    #
    # def __ne__(self, o):
    #     return self.name_ != o.get_name()
    #
    # def __hash__(self) -> int:
    #     return self.name_.__hash__()




