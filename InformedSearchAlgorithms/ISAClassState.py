# import itertools
# import math
#
# from Utils.Constants import *
#
#
# class ISAState:
#     def __init__(self, n_courses, n_halls, courses_to_rows_dict, halls_to_cols_dict,
#                  reverse_halls_to_cols_dict, should_initialize, assignment_dict={}):
#         self.n_courses_ = n_courses
#         self.n_halls_ = n_halls
#         self.courses_dict = courses_to_rows_dict  # mapping courses objects to their indices
#         self.halls_dict = halls_to_cols_dict  # mapping halls to their indices
#         self.reverse_halls_dict = reverse_halls_to_cols_dict  # mapping indices to hals
#         if should_initialize:
#             self.assignment_dict = dict()  # mapping exam to class
#             while self.initialize_state() == 0:
#                 self.assignment_dict = dict()
#         else:
#             self.assignment_dict = assignment_dict
#
#
#     def initialize_state(self):
#
#
#
#     def calculate_days_(self, pair):
#
#
#     def is_legal_moed_b_date(self, moed_a_col, moed_b_col):
#
#
#     def generate_successor(self):
#
#     def apply_unary_periods_move(self, course_row, course_col):
#
#     def apply_binary_move(self, course_row, course_col):
#
#
#     def apply_random_move(self, course_row, course_col):
#
#
#     def check_unary_periods_legal_move(self, move):
#
#
#     def check_binary_legal_move(self, move):
#
#
#     def check_legal_transfer(self, exam_row, exam_new_col):
#
#
#     def apply_move(self, move):
#
#
#     def get_value(self):
#
#
#     def exam_diff_constraint(self):
#
#
#     def periods_separation_constraint(self):
#
#
#     def __copy__(self):
#
#
#     def __repr__(self):
#
#
#     def __eq__(self, other):
#
#
#
# class UnaryMove:
#
#     def __init__(self, old_row, old_col, new_row, new_col, move_type):
#         self.old_row = old_row
#         self.old_col = old_col
#         self.new_row = new_row
#         self.new_col = new_col
#         self.type = move_type # Determines whether the move is between periods or days
#
#     def __str__(self):
#         return f"({self.old_row, self.old_col} -> {self.new_row, self.new_col})"
#
#
# class BinaryMove:
#
#     def __init__(self, first_row, first_col, second_row, second_col, move_type):
#         self.first_row = first_row
#         self.first_col = first_col
#         self.second_row = second_row
#         self.second_col = second_col
#         self.type = move_type # Binary move type
#
#     def __str__(self):
#         return f"({self.first_row, self.first_col} <-> {self.second_row, self.second_col})"
#
