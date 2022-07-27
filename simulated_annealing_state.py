import itertools

import numpy as np
from Constants import *


class State:

    def __init__(self, exam_time_mat, n_courses, n_times, courses_to_rows_dict,
                 times_to_cols_dict, reverse_times_to_cols_dict, initialize_mat, assignment_dict):
        self.n_courses = n_courses
        self.n_times = n_times
        self.courses_dict = courses_to_rows_dict # mapping courses objects to their indices
        self.times_dict = times_to_cols_dict # mapping "representative times" to their indices
        self.reverse_times_dict = reverse_times_to_cols_dict # mapping indices to their "representative" times
        if initialize_mat:
            self.exam_time_mat = np.zeros(shape=(n_courses, n_times))
            self.assignment_dict = dict() # mapping from courses indices to times indices
            self.initialize_state()
        else:
            self.exam_time_mat = exam_time_mat
            self.assignment_dict = assignment_dict # mapping from courses indices to times indices

    def initialize_state(self):
        moed_a_courses_indices = np.array(range(self.n_courses / 2))
        times_indices = np.array(range(self.n_times))
        n_courses_assigned = 0
        while n_courses_assigned < self.n_courses:
            current_moed_a = np.random.choice(moed_a_courses_indices)
            current_moed_a_time  = np.random.choice(times_indices)
            current_moed_b = current_moed_a + self.n_courses / 2
            current_moed_b_time = np.random.choice(times_indices)
            while not self.is_legal_moed_b_date(current_moed_a_time, current_moed_b_time):
                current_moed_b_time = np.random.choice(times_indices)
            self.exam_time_mat[current_moed_a][current_moed_a_time] = 1
            self.exam_time_mat[current_moed_b][current_moed_b_time] = 1
            self.assignment_dict[current_moed_a] = current_moed_a_time
            self.assignment_dict[current_moed_b] = current_moed_b_time


    def is_legal_moed_b_date(self, moed_a_time, moed_b_time):
        times_keys = self.times_dict.keys()
        moed_a_rep_time = self.reverse_times_dict[moed_a_time]
        moed_b_rep_time = self.reverse_times_dict[moed_b_time]
        return int(moed_b_rep_time) - int(moed_a_rep_time) >= 12 # 12 instead of 14 due to 2 Saturdays between moed a and moed b




    def add_move(self, player, move):


    def do_move(self, player, move):
        """
        Performs a move, returning a new board
        """
        new_board = self.__copy__()
        new_board.add_move(player, move)

        return new_board

    def get_legal_moves(self):
        # Generate all legal moves
        legal_moves = list()
        # for course_ind in range(self.n_courses):
        #     current_col = self.assignment_dict[course_ind]
        #     # Create unary periods move to possible moves to apply
        #     for span in [1, -1]:
        #         move = UnaryMove(course_ind, current_col, course_ind, current_col + span,
        #                          UNARY_PERIODS_MOVE)
        #         possible_moves.append(move)
        #     # Create unary days move to possible moves to apply
        #     for span in [3, -3]:
        #         move = UnaryMove(course_ind, current_col, course_ind, current_col + span,
        #                          UNARY_DAYS_MOVE)
        #         possible_moves.append(move)
        # courses_combinations = itertools.combinations(range(self.n_courses), 2)
        # # Create binary days move to apply
        # for course1, course2 in courses_combinations:
        #     move = BinaryMove(course1, self.assignment_dict[course1],
        #                       course2, self.assignment_dict[course2], BINARY_MOVE)
        #     possible_moves.append(move)
        # return filter(self.check_legal_move, possible_moves)
        for course_ind in range(self.n_courses):
            current_col = self.assignment_dict[course_ind]
            for span in [-1, 1]:
                for try_ind in range(1, N_TRIES + 1):
                    move = UnaryMove(course_ind, current_col, course_ind, current_col + span * try_ind,
                                     UNARY_PERIODS_MOVE)
                    if self.check_unary_periods_legal_move(move):
                        legal_moves.append(move)
                        break




    def check_legal_move(self, move):
        if move.type == UNARY_PERIODS_MOVE:
            return self.check_unary_periods_legal_move(move)
        elif move.type == UNARY_DAYS_MOVE:
            return self.check_unary_days_legal_move(move)
        else:
            return self.check_binary_days_legal_move(move)


    def check_unary_periods_legal_move(self, move):
        # Check whether we are in the proper bounds
        if move.new_col < 0 or move.new_col >= self.n_times:
            return False
        # # Check whether we are moving in the same day
        # elif int(self.reverse_times_dict[move.new_col]) - int(self.reverse_times_dict[move.old_col]) != 0:
        #     return False
        # Check whether we are not on Friday
        elif self.reverse_times_dict[move.new_col] not in self.times_dict.keys():
            return False
        # Check whether the requested slot is not empty
        return self.exam_time_mat[move.new_row][move.new_col] == 0

    def check_unary_days_legal_move(self, move):
        # Check whether we are in the proper bounds
        if move.new_col < 0 or move.new_col >= self.n_times:
            return False
        # Check whether we are moving just one day further
        elif int(self.reverse_times_dict[move.new_col]) - int(self.reverse_times_dict[move.old_col]) != 0:
            return False
















    def check_tile_legal(self, player, x, y):
        """
        Check if it's legal for <player> to place one tile at (<x>, <y>).

        Legal tiles:
        - Are in bounds
        - Don't intersect with existing tiles
        - Aren't adjacent to the player's existing tiles

        Returns True if legal or False if not.
        """

        # Make sure tile in bounds
        if x < 0 or x >= self.board_w or y < 0 or y >= self.board_h:
            return False

        # Otherwise, it's in the lookup table
        return self._legal[player, y, x]

    def get_position(self, x, y):
        return self.state[y, x]

    def score(self, player):
        return self.scores[player]

    def __eq__(self, other):
        return np.array_equal(self.state, other.state) and np.array_equal(self.pieces, other.pieces)

    def __hash__(self):
        return hash(str(self.state))

    def __str__(self):
        out_str = []
        for row in range(self.board_h):
            for col in range(self.board_w):
                if self.state[col, row] == -1:
                    out_str.append('_')
                else:
                    out_str.append(str(self.state[col, row]))
            out_str.append('\n')
        return ''.join(out_str)

    def __copy__(self):
        cpy_board = Board(self.board_w, self.board_h, self.num_players, self.piece_list)
        cpy_board.state = np.copy(self.state)
        cpy_board._legal = np.copy(self._legal)
        cpy_board.connected = np.copy(self.connected)
        cpy_board.pieces = np.copy(self.pieces)
        cpy_board.scores = self.scores[:]
        return cpy_board


class UnaryMove:

    def __init__(self, old_row, old_col, new_row, new_col, move_type)
        self.old_row = old_row
        self.old_col = old_col
        self.new_row = new_row
        self.new_col = new_col
        self.type = move_type # Determines whether the move is between periods or days

    def __str__(self):
        return f"({self.old_row, self.old_col} -> {self.new_row, self.new_col}"

class BinaryMove:

    def __init__(self, first_row, first_col, second_row, second_col, move_type)
        self.first_row = first_row
        self.first_col = first_col
        self.second_row = second_row
        self.second_col = second_col
        self.type = move_type # Binary move type

    def __str__(self):
        return f"({self.first_row, self.first_col} <-> {self.second_row, self.second_col}"