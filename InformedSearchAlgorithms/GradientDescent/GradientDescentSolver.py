import random

from InformedSearchAlgorithms.ISAState import ISAState
from InformedSearchAlgorithms.ISAHallState import ISAHallState
from Utils.Constants import *
import numpy as np


class GradientDescentSolver:

	def __init__(self, n_courses, n_times, courses_to_rows_dict, reverse_courses_dict,
				 times_to_cols_dict, reverse_times_to_cols_dict, assignment_dict, times_to_days_dict,
				 alpha, cooling_function, algorithm, max_iter=5000, callback=None, complex_callback=None,
				 complex_problem=False, n_halls=None, halls_to_cols_dict=None, reverse_halls_to_cols_dict=None,
				 time_assignment_dict=None):
		self.alpha_ = alpha
		self.cooling_function_ = cooling_function
		self.max_iter_ = max_iter
		self.callback = callback
		self.complex_problem = complex_problem
		self.complex_callback = complex_callback
		self.algorithm = algorithm
		if not complex_problem:
			self.state_ = ISAState(n_courses, n_times, courses_to_rows_dict, reverse_courses_dict,
								   times_to_cols_dict, reverse_times_to_cols_dict, assignment_dict, {},
								   times_to_days_dict, True)
		else:
			self.state_ = ISAHallState(n_courses, n_times, n_halls, courses_to_rows_dict, reverse_courses_dict,
									   halls_to_cols_dict, reverse_halls_to_cols_dict, time_assignment_dict, True)

	def solve(self):
		min_state = None
		for t in range(self.max_iter_):
			if self.callback:
				self.callback(self.state_.get_value(), 0)
			if self.complex_callback:
				self.complex_callback(self.state_.get_value(), 0)
			next_state = self.state_.generate_successor_for_gd()
			delta = next_state.get_value() - self.state_.get_value()
			val = random.uniform(0, 1)
			if self.algorithm == RANDOM_GRADIENT_DESCENT and val < 0.009:
				if min_state is None or self.state_.get_value() < min_state.get_value():
					min_state = self.state_.__copy__()
				print("im here!!!!!")
				self.state_ = self.state_.generate_successor()
			if delta < 0:
				self.state_ = next_state
			else:
				if self.algorithm == RANDOM_GRADIENT_DESCENT:
					if min_state is None or self.state_.get_value() < min_state.get_value():
						min_state = self.state_.__copy__()
					self.state_.initialize()
					print("restart")
				else:
					return

		if min_state is not None:
			self.state_ = min_state

	def get_state(self):
		return self.state_
