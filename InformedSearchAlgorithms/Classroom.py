class Classroom:
    def __init__(self, name, area, classroom_type, chair_type, capacity):
        self.name_ = name
        self.area_ = area
		self.classroom_type_ = classroom_type
        self.chair_type_ = chair_type
        self.capacity_ = capacity

    def get_name(self):
        return self.name_

	def get_area(self):
		return self.area_

	def get_clasroom_type(self):
		return self.classroom_type_

    def get_chair_type(self):
        return self.chair_type_

	def get_capacity(self):
		return self.capacity_

    def __repr__(self):
        return self.name_
