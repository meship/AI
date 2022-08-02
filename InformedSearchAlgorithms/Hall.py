class Hall:
	def __init__(self, name, area, capacity, chair_type, hall_type):
		self.name_ = name
		self.area_ = area
		self.hall_type_ = hall_type
		self.chair_type_ = chair_type
		self.capacity_ = capacity

	def get_name(self):
		return self.name_

	def get_area(self):
		return self.area_

	def get_hall_type(self):
		return self.hall_type_

	def get_chair_type(self):
		return self.chair_type_

	def get_capacity(self):
		return self.capacity_

	def __repr__(self):
		return self.name_
