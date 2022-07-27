import copy
import itertools

import numpy as np
from Constants import *


class SimulatedAnnealingState:
    # todo: courses in the requested matrix should be arranged by attempts
    def __init__(self, n_courses, n_times, courses_to_rows_dict,
                 times_to_cols_dict, reverse_times_to_cols_dict, assignment_dict,
                 initialize_mat, exam_time_mat=None):
        self.n_courses = n_courses
        self.n_times = n_times
        self.courses_dict = courses_to_rows_dict # mapping courses objects to their indices
        self.times_dict = times_to_cols_dict # mapping "representative times" to their indices
        self.reverse_times_dict = reverse_times_to_cols_dict # mapping indices to their "representative" times
        if initialize_mat:
            # self.exam_time_mat = np.zeros(shape=(n_courses, n_times))
            self.assignment_dict = dict() # mapping from courses indices to times indices
            while self.initialize_state() == 0:
                self.assignment_dict = dict()
        else:
            # self.exam_time_mat = exam_time_mat
            self.assignment_dict = assignment_dict # mapping from courses indices to times indices

    def initialize_state(self):
        moed_a_courses_indices = np.array(range(self.n_courses // 2))
        times_indices = np.array(range(self.n_times))
        n_courses_assigned = 0
        while n_courses_assigned < self.n_courses // 2:
            current_moed_a = np.random.choice(moed_a_courses_indices)
            current_moed_a_time = np.random.choice(times_indices)
            current_moed_b = current_moed_a + self.n_courses // 2
            available_moed_b_times = times_indices[times_indices >= current_moed_a_time + ATTEMPTS_DIFF]
            if not len(available_moed_b_times):
                return 0
            current_moed_b_time = np.random.choice(available_moed_b_times)
            # self.exam_time_mat[current_moed_a][current_moed_a_time] = 1
            # self.exam_time_mat[current_moed_b][current_moed_b_time] = 1
            self.assignment_dict[current_moed_a] = current_moed_a_time
            self.assignment_dict[current_moed_b] = current_moed_b_time
            moed_a_ind = np.argwhere(moed_a_courses_indices == current_moed_a)
            moed_a_courses_indices = np.delete(moed_a_courses_indices, moed_a_ind)
            moed_a_time_ind = np.argwhere(times_indices == current_moed_a_time)
            times_indices = np.delete(times_indices, moed_a_time_ind)
            moed_b_time_ind = np.argwhere(times_indices == current_moed_b_time)
            times_indices = np.delete(times_indices, moed_b_time_ind)
            n_courses_assigned += 1
        return 1

    def is_legal_moed_b_date(self, moed_a_col, moed_b_col):
        moed_a_rep_time = self.reverse_times_dict[moed_a_col]
        moed_b_rep_time = self.reverse_times_dict[moed_b_col]
        return int(moed_b_rep_time) - int(moed_a_rep_time) >= ATTEMPTS_DIFF # 12 instead of 14 due to 2 Saturdays between moed a and moed b

    def generate_successor(self):
        successor_state = self.__copy__()
        # Generate all legal moves
        for course_ind in range(self.n_courses):
            time_ind = successor_state.assignment_dict[course_ind]
            action_to_apply = np.random.choice([UNARY_PERIODS_MOVE, BINARY_MOVE])
            if action_to_apply == UNARY_PERIODS_MOVE:
                successor_state.apply_unary_periods_move(course_ind, time_ind)
            else:
                successor_state.apply_binary_move(course_ind, time_ind)
            # for course1, course_ind1 in self.courses_dict.items():
        return successor_state

    def apply_unary_periods_move(self, course_row, course_col):
        progress_way = np.random.choice([UNARY_MOVE_FORWARD, UNARY_MOVE_BACKWARD])
        for try_ind in range(1, N_TRIES + 1):
            move = UnaryMove(course_row, course_col, course_row, course_col + progress_way * try_ind,
                             UNARY_PERIODS_MOVE)
            if self.check_unary_periods_legal_move(move):
                self.apply_move(move)
                return

    def apply_binary_move(self, course_row, course_col):
        # todo: consider trying till a new friend is swappable
        friend_row = np.random.choice(range(self.n_courses))
        while course_row == friend_row or abs(course_row - friend_row) == (self.n_courses // 2):
            friend_row = np.random.choice(range(self.n_courses))
        move = BinaryMove(course_row, course_col,
                          friend_row, self.assignment_dict[friend_row], BINARY_MOVE)
        if self.check_binary_legal_move(move):
            self.apply_move(move)

    def check_unary_periods_legal_move(self, move):
        # Check whether we are in the proper bounds
        if move.new_col < 0 or move.new_col >= self.n_times:
            return False
        # Check whether we are not on Friday
        elif self.reverse_times_dict[move.new_col] not in self.times_dict.keys():
            return False
        # Check whether the hard constraint between 2 attempts remains satisfied
        elif not self.check_legal_transfer(move.old_row, move.new_col):
            return False
        # Check whether the requested slot is not empty
        # return self.exam_time_mat[move.new_row][move.new_col] == 0
        for assignment in self.assignment_dict.values():
            if assignment == move.new_col:
                return False
        return True

    def check_binary_legal_move(self, move):
        exam1_new_col, exam2_new_col = move.second_col, move.first_col
        exam1_row, exam2_row = move.first_row, move.second_row
        if not self.check_legal_transfer(exam1_row, exam1_new_col):
            return False
        if not self.check_legal_transfer(exam2_row, exam2_new_col):
            return False
        return True

    def check_legal_transfer(self, exam_row, exam_new_col):
        # Check whether the right difference between first and second attempt is kept
        if exam_row < (self.n_courses // 2):
            moed_b_row = exam_row + self.n_courses // 2
            moed_b_time = self.assignment_dict[moed_b_row]
            if not self.is_legal_moed_b_date(exam_new_col, moed_b_time):
                return False
        else:
            moed_a_row = exam_row - self.n_courses // 2
            moed_a_time = self.assignment_dict[moed_a_row]
            if not self.is_legal_moed_b_date(moed_a_time, exam_new_col):
                return False
        return True

    def apply_move(self, move):
        if move.type == UNARY_PERIODS_MOVE:
            # self.exam_time_mat[move.old_row][move.old_col] = 0
            # self.exam_time_mat[move.new_row][move.new_col] = 1
            self.assignment_dict[move.new_row] = move.new_col
        else:
            # self.exam_time_mat[move.first_row][move.first_col] = 0
            # self.exam_time_mat[move.first_row][move.second_col] = 1
            self.assignment_dict[move.first_row] = move.second_col
            # self.exam_time_mat[move.second_row][move.second_col] = 0
            # self.exam_time_mat[move.second_row][move.first_col] = 1
            self.assignment_dict[move.second_row] = move.first_col

    def get_value(self):
        state_value = 0
        # Check math exams are on mornings
        for course, course_ind in self.courses_dict.items():
            if 'M' in course.get_faculties():
                repr_time = self.reverse_times_dict[self.assignment_dict[course_ind]]
                if round(repr_time, 1) - int(repr_time) != MORNING_EXAM:
                    state_value += 1
        print(state_value)
        return state_value

    def check_duplicates(self):
        assigned_values = self.assignment_dict.values()
        return len(assigned_values) != len(np.unique(np.array(list(assigned_values))))

    # def score(self, player):
    #     return self.scores[player]
    #
    # def __eq__(self, other):
    #     return np.array_equal(self.state, other.state) and np.array_equal(self.pieces, other.pieces)
    #
    # def __hash__(self):
    #     return hash(str(self.state))
    #
    # def __str__(self):
    #     out_str = []
    #     for row in range(self.board_h):
    #         for col in range(self.board_w):
    #             if self.state[col, row] == -1:
    #                 out_str.append('_')
    #             else:
    #                 out_str.append(str(self.state[col, row]))
    #         out_str.append('\n')
    #     return ''.join(out_str)

    def __copy__(self):
        c_n_courses = self.n_courses
        c_n_times = self.n_times
        c_courses_dict = self.courses_dict.copy()
        c_times_dict = self.times_dict
        c_n_reverse_times_dict = self.reverse_times_dict
        c_assignment_dict = self.assignment_dict.copy()
        # c_exam_time_mat = copy.deepcopy(self.exam_time_mat)
        return SimulatedAnnealingState(c_n_courses, c_n_times, c_courses_dict, c_times_dict,
                                       c_n_reverse_times_dict, c_assignment_dict, False, None)

    def __repr__(self):
        repr_val = "Exam Scheduling Is:\n"
        for course, course_ind in self.courses_dict.items():
            repr_time = self.reverse_times_dict[self.assignment_dict[course_ind]]
            repr_val += f"{course}: {repr_time}\n"
        return repr_val


class UnaryMove:

    def __init__(self, old_row, old_col, new_row, new_col, move_type):
        self.old_row = old_row
        self.old_col = old_col
        self.new_row = new_row
        self.new_col = new_col
        self.type = move_type # Determines whether the move is between periods or days

    def __str__(self):
        return f"({self.old_row, self.old_col} -> {self.new_row, self.new_col})"


class BinaryMove:

    def __init__(self, first_row, first_col, second_row, second_col, move_type):
        self.first_row = first_row
        self.first_col = first_col
        self.second_row = second_row
        self.second_col = second_col
        self.type = move_type # Binary move type

    def __str__(self):
        return f"({self.first_row, self.first_col} <-> {self.second_row, self.second_col})"