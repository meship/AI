import itertools
import math

from Utils.Constants import *


class ISAState:
    # todo: courses in the requested matrix should be arranged by attempts
    def __init__(self, n_courses, n_times, courses_to_rows_dict,
                 times_to_cols_dict, reverse_times_to_cols_dict, assignment_dict,
                 should_initialize, times_to_dates_dict):
        self.n_courses = n_courses
        self.n_times = n_times
        self.courses_dict = courses_to_rows_dict # mapping courses objects to their indices
        self.times_dict = times_to_cols_dict # mapping "representative times" to their indices
        self.reverse_times_dict = reverse_times_to_cols_dict # mapping indices to their "representative" times
        if should_initialize:
            # self.exam_time_mat = np.zeros(shape=(n_courses, n_times))
            self.assignment_dict = dict() # mapping from courses indices to times indices
            while self.initialize_state() == 0:
                self.assignment_dict = dict()
        else:
            # self.exam_time_mat = exam_time_mat
            self.assignment_dict = assignment_dict # mapping from courses indices to times indices

        self.days_difference = {'CS': (CS_EXAM_DIFFERENCE_A, CS_EXAM_DIFFERENCE_B),
                                'EE': (EE_EXAM_DIFFERENCE_A, EE_EXAM_DIFFERENCE_B),
                                'M': (M_EXAM_DIFFERENCE_A, M_EXAM_DIFFERENCE_B),
                                'CB': (CB_EXAM_DIFFERENCE_A, CB_EXAM_DIFFERENCE_B),
                                'ST': (ST_EXAM_DIFFERENCE_A, ST_EXAM_DIFFERENCE_B),
                                'E': (E_EXAM_DIFFERENCE_A, E_EXAM_DIFFERENCE_B),
                                'P': (P_EXAM_DIFFERENCE_A, P_EXAM_DIFFERENCE_B),
                                'PC': (PC_EXAM_DIFFERENCE_A, PC_EXAM_DIFFERENCE_B),
                                'CSM': (CSM_EXAM_DIFFERENCE_A, CSM_EXAM_DIFFERENCE_B),
                                'CSE': (CSE_EXAM_DIFFERENCE_A, CSE_EXAM_DIFFERENCE_B),
                                'CSP': (CSP_EXAM_DIFFERENCE_A, CSP_EXAM_DIFFERENCE_B),
                                'PSB': (PSB_EXAM_DIFFERENCE_A, PSB_EXAM_DIFFERENCE_B),
                                'CSC': (CSC_EXAM_DIFFERENCE_A, CSC_EXAM_DIFFERENCE_B)}
        pairs_permutations = list(itertools.permutations(self.courses_dict.keys(), 2))
        self.pairs_difference = dict()
        for pair in pairs_permutations:
            self.calculate_days_(pair)
        self.times_to_days_dict = times_to_dates_dict

    def initialize_state(self):
        moed_a_courses_indices = np.array(range(self.n_courses // 2))
        moed_a_final_date = math.floor(self.n_times * MOED_A_RATIO)
        moed_a_times_indices = np.array(range(moed_a_final_date))
        moed_b_times_indices = np.array(range(moed_a_final_date + 1, self.n_times))
        n_courses_assigned = 0
        while n_courses_assigned < self.n_courses // 2:
            current_moed_a = np.random.choice(moed_a_courses_indices)
            current_moed_a_time = np.random.choice(moed_a_times_indices)
            current_moed_b = current_moed_a + self.n_courses // 2
            available_moed_b_times = moed_b_times_indices[moed_b_times_indices >= current_moed_a_time + ATTEMPTS_DIFF]
            if not len(available_moed_b_times):
                return 0
            current_moed_b_time = np.random.choice(available_moed_b_times)
            self.assignment_dict[current_moed_a] = current_moed_a_time
            self.assignment_dict[current_moed_b] = current_moed_b_time
            moed_a_ind = np.argwhere(moed_a_courses_indices == current_moed_a)
            moed_a_courses_indices = np.delete(moed_a_courses_indices, moed_a_ind)
            moed_a_time_ind = np.argwhere(moed_a_times_indices == current_moed_a_time)
            moed_a_times_indices = np.delete(moed_a_times_indices, moed_a_time_ind)
            moed_b_time_ind = np.argwhere(moed_b_times_indices == current_moed_b_time)
            moed_b_times_indices = np.delete(moed_b_times_indices, moed_b_time_ind)
            n_courses_assigned += 1
        return 1

    def calculate_days_(self, pair):
        for faculty in self.days_difference:
            if faculty in pair[0].get_faculties() and faculty in pair[1].get_faculties():
                self.pairs_difference[pair] = max([self.days_difference[val][pair[1].get_attempt()] for val in pair[1].get_faculties()])
                return
        self.pairs_difference[pair] = 0

    def is_legal_moed_b_date(self, moed_a_col, moed_b_col):
        moed_a_rep_time = self.reverse_times_dict[moed_a_col]
        moed_b_rep_time = self.reverse_times_dict[moed_b_col]
        return int(moed_b_rep_time) - int(moed_a_rep_time) >= ATTEMPTS_DIFF # 12 instead of 14 due to 2 Saturdays between moed a and moed b

    def generate_successor(self):
        # todo: add another move option which chooses a random value to be assigned
        successor_state = self.__copy__()
        # Generate all legal moves
        for course_ind in range(self.n_courses):
            time_ind = successor_state.assignment_dict[course_ind]
            action_to_apply = np.random.choice(a=[UNARY_PERIODS_MOVE, BINARY_MOVE, RANDOM_MOVE], size=1, replace=True,
                                               p=np.array([0.45, 0.45, 0.1]))
            if action_to_apply == UNARY_PERIODS_MOVE:
                successor_state.apply_unary_periods_move(course_ind, time_ind)
            elif action_to_apply == BINARY_MOVE:
                successor_state.apply_binary_move(course_ind, time_ind)
            else:
                successor_state.apply_random_move(course_ind, time_ind)
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

    def apply_random_move(self, course_row, course_col):
        moed_a_final_date = math.floor(self.n_times * MOED_A_RATIO)
        if course_row < self.n_courses // 2:
            for try_ind in range(1, N_TRIES + 1):
                new_col = np.random.choice(a=np.array(np.arange(moed_a_final_date + 1)))
                move = UnaryMove(course_row, course_col, course_row, new_col, UNARY_PERIODS_MOVE)
                if self.check_unary_periods_legal_move(move):
                    self.apply_move(move)
                    return
        else:
            for try_ind in range(1, N_TRIES + 1):
                new_col = np.random.choice(a=np.array(np.arange(moed_a_final_date + 1, self.n_times)))
                move = UnaryMove(course_row, course_col, course_row, new_col, UNARY_PERIODS_MOVE)
                if self.check_unary_periods_legal_move(move):
                    self.apply_move(move)
                    return

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
        # Check whether the separation between first and second attempts is still kept
        exam_separation_day = math.floor(self.n_times * MOED_A_RATIO)
        if exam_row < (self.n_courses // 2):
            if exam_new_col > exam_separation_day:
                return False
        else:
            if exam_new_col <= exam_separation_day:
                return False
        # Check whether the requested slot is not empty
        for assignment in self.assignment_dict.values():
            if assignment == exam_new_col:
                return False

        return True

    def apply_move(self, move):
        if move.type == UNARY_PERIODS_MOVE:
            self.assignment_dict[move.new_row] = move.new_col
        else:
            self.assignment_dict[move.first_row] = move.second_col
            self.assignment_dict[move.second_row] = move.first_col

    def get_value(self):
        # Check satisfaction of soft constraints and return the representative value
        # state_val = self.exam_diff_constraint() + 2 * self.exam_on_friday_constraint() + \
        #             2 * self.exam_on_sunday_morning_constraint() + 4 * self.math_exam_on_morning_constraint() + \
        #             7 * self.exam_on_evening_constraint()
        state_val = self.exam_diff_constraint() + 0.75 * self.exam_on_evening_constraint()
        print(state_val)
        return state_val

    def exam_diff_constraint(self):
        state_value = 0
        course_permutations = itertools.permutations(self.courses_dict.keys(), 2)
        for course_pair in course_permutations:
            actual_pair_diff = self.get_course_time_diff(course_pair)
            diff_from_optimal = max(0, self.pairs_difference[course_pair] - actual_pair_diff)
            if diff_from_optimal >= 3:
                diff_from_optimal = diff_from_optimal * 2
            state_value += diff_from_optimal
        return state_value

    def periods_separation_constraint(self):
        moed_a_times = list()
        moed_b_times = list()
        for course_ind, time_ind in self.assignment_dict.items():
            if course_ind < self.n_courses // 2:
                moed_a_times.append(time_ind)
            else:
                moed_b_times.append(time_ind)
        return max(0, max(moed_a_times) - min(moed_b_times))

    def exam_on_friday_constraint(self):
        penalty = 0
        for course, col in self.assignment_dict.items():
            repr_time = self.reverse_times_dict[col]
            day_of_week = self.times_to_days_dict[repr_time]
            if day_of_week.weekday() == FRIDAY:
                penalty += 1
        return penalty

    def exam_on_sunday_morning_constraint(self):
        penalty = 0
        for course, col in self.assignment_dict.items():
            repr_time = self.reverse_times_dict[col]
            day_of_week = self.times_to_days_dict[repr_time]
            if day_of_week.weekday() == SUNDAY and round(repr_time - int(repr_time), 2) == MORNING_EXAM:
                penalty += 1
        return penalty

    def exam_on_evening_constraint(self):
        penalty = 0
        for course, col in self.assignment_dict.items():
            repr_time = self.reverse_times_dict[col]
            if round(repr_time - int(repr_time), 2) == EVENING_EXAM:
                penalty += 1
        return penalty

    def math_exam_on_morning_constraint(self):
        penalty = 0
        for course, course_ind in self.courses_dict.items():
            if 'M' in course.get_faculties():
                repr_time = self.reverse_times_dict[self.assignment_dict[course_ind]]
                if round(round(repr_time, 1) - int(repr_time),1) != MORNING_EXAM:
                    penalty += 1
        return penalty

    def check_duplicates(self):
        assigned_values = self.assignment_dict.values()
        return len(assigned_values) != len(np.unique(np.array(list(assigned_values))))

    def check_exams_diff(self):
        quality_dict = dict()
        course_permutations = itertools.permutations(self.courses_dict.keys(), 2)
        for course_pair in course_permutations:
            actual_pair_diff = self.get_course_time_diff(course_pair)
            diff = max(0, int(self.pairs_difference[course_pair] - actual_pair_diff))
            if diff:
                quality_dict[course_pair] = diff
        return quality_dict

    def get_course_time_diff(self, course_pair):
        course1_ind = self.courses_dict[course_pair[0]]
        course2_ind = self.courses_dict[course_pair[1]]
        course1_time_ind = self.assignment_dict[course1_ind]
        course2_time_ind = self.assignment_dict[course2_ind]
        actual_pair_diff = abs(self.reverse_times_dict[course1_time_ind] -
                               self.reverse_times_dict[course2_time_ind])
        return actual_pair_diff

    def __copy__(self):
        c_n_courses = self.n_courses
        c_n_times = self.n_times
        c_courses_dict = self.courses_dict.copy()
        c_times_dict = self.times_dict
        c_n_reverse_times_dict = self.reverse_times_dict
        c_assignment_dict = self.assignment_dict.copy()
        c_n_times_to_days_dict = self.times_to_days_dict
        return ISAState(c_n_courses, c_n_times, c_courses_dict, c_times_dict,
                        c_n_reverse_times_dict, c_assignment_dict, False, c_n_times_to_days_dict)

    def __repr__(self):
        repr_val = "Exam Scheduling Is:\n"
        for course, course_ind in self.courses_dict.items():
            repr_time = self.reverse_times_dict[self.assignment_dict[course_ind]]
            repr_val += f"{course}: {repr_time}\n"
        return repr_val

    def __eq__(self, other):
        eq_count = 0
        for course_ind in self.assignment_dict.keys():
            if self.assignment_dict[course_ind] == other.assignment_dict[course_ind]:
                eq_count += 1
        return eq_count == self.n_courses



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


# todo:
# check with a big database
# change time difference for second attempts
# export scheduling of courses to a table
