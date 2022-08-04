import itertools
import math
import copy

from Utils.Constants import *
from Utils.utils import update_dict

class ISAHallState:
    def __init__(self, n_courses, n_times, n_halls, courses_to_rows_dict, reverse_courses_dict, halls_to_cols_dict,
                 reverse_halls_to_cols_dict, time_assignment_dict, should_initialize, halls_assignment_dict={},
                 time_to_halls_dict={}):
        self.n_courses = n_courses
        self.n_times = n_times
        self.n_halls = n_halls
        self.courses_dict = courses_to_rows_dict  # mapping courses objects to their indices
        self.reverse_courses_dict = reverse_courses_dict
        self.halls_dict = halls_to_cols_dict  # mapping halls to their indices
        self.reverse_halls_dict = reverse_halls_to_cols_dict  # mapping indices to halls
        self.time_assignment_dict = time_assignment_dict
        if should_initialize:
            self.halls_assignment_dict = dict()  # mapping exam to class
            self.time_to_halls = dict()
            self.initialize_state()
        else:
            self.halls_assignment_dict = halls_assignment_dict
            self.time_to_halls = time_to_halls_dict


    def initialize_state(self):
        n_courses_assigned = 0
        available_moed_a_courses = np.array(range(self.n_courses // 2))
        self.make_halls_dict()
        while n_courses_assigned < self.n_courses // 2:
            current_moed_a = np.random.choice(available_moed_a_courses)
            halls_list_a = self.assign_halls(current_moed_a, self.time_assignment_dict[current_moed_a])
            current_moed_b = current_moed_a + self.n_courses // 2
            halls_list_b = self.assign_halls(current_moed_b, self.time_assignment_dict[current_moed_b])
            self.halls_assignment_dict[current_moed_a] = halls_list_a
            self.halls_assignment_dict[current_moed_b] = halls_list_b

            # updating the dicts
            moed_a_ind = np.argwhere(available_moed_a_courses == current_moed_a)
            available_moed_a_courses = np.delete(available_moed_a_courses, moed_a_ind)
            n_courses_assigned += 1
        # self.time_to_halls = unavailable_halls_dict.copy()
        # return 1 #todo: think more
        a=1

    def make_halls_dict(self):
        for day_time in range(self.n_times):
            self.time_to_halls[day_time] = []

    def assign_halls(self, course_ind, time_sloth):
        students_count = self.reverse_courses_dict[course_ind].get_n_students()
        course_halls_idxs = []
        while students_count > 0:
            hall_idx = self.find_hall(course_ind, time_sloth)
            students_count -= self.reverse_halls_dict[hall_idx].get_capacity()
            course_halls_idxs.append(hall_idx)
        return course_halls_idxs

    def find_hall(self, course_ind, time_sloth):
        hall_idx = np.random.choice(np.array(list(set(range(self.n_halls)) - set(self.time_to_halls[time_sloth]))))

        while self.reverse_courses_dict[course_ind].get_hall_type() != \
                self.reverse_halls_dict[hall_idx].get_hall_type():
            hall_idx = np.random.choice(np.array(list(set(range(self.n_halls)) - set(self.time_to_halls[time_sloth]))))
            # print(f"new hall index {hall_idx}")
            # print(unavailable_halls[time_sloth])
        # unavailable_halls[time_sloth].append(hall_idx)
        update_dict(time_sloth, hall_idx, self.time_to_halls)
        return hall_idx

    # def generate_successor(self):
    #     successor_state = self.__copy__()
    #     # Generate all legal moves
    #     for course_ind in range(self.n_courses):
    #         time_ind = successor_state.time_assignment_dict[course_ind]
    #         action_to_apply = np.random.choice(a=[UNARY_PERIODS_MOVE, BINARY_MOVE, ADD_HALL, REMOVE_HALL], size=1, replace=True,
    #                                            p=np.array([0.1, 0.7, 0.1, 0.1])) #todo: maybe add another move - stay in place
    #         if action_to_apply == UNARY_PERIODS_MOVE:
    #             successor_state.apply_hall_unary_move(course_ind, time_ind)
    #         elif action_to_apply == BINARY_MOVE:
    #             successor_state.apply_hall_binary_move(course_ind, time_ind)
    #         elif action_to_apply == ADD_HALL:
    #             successor_state.apply_hall_add_move(course_ind, time_ind)
    #         else:
    #             successor_state.apply_hall_remove_move(course_ind, time_ind)
    #
    #     return successor_state

    def apply_try_move(self, course_row, course_col):
        r = 0
        s = 0
        r_hall, s_hall = [], []
        for hall in self.halls_assignment_dict[course_row]:
            if self.reverse_halls_dict[hall].get_hall_type == 'r':
                r += 1
                r_hall.append(hall)
            else:
                s += 1
                s_hall.append(hall)
        if not r_hall or not s_hall:
            return
        available_halls = list(set(range(self.n_halls)) - set(self.time_to_halls[course_col]))
        if r > s:
            new_list = []
            for hall in available_halls:
                if self.reverse_halls_dict[hall].get_hall_type() == 'r':
                    new_list.append(hall)
            chosen_hall = np.random.choice(new_list)
            hall_to_replace = np.random.choice(s_hall)
        else:
            new_list = []
            for hall in available_halls:
                if self.reverse_halls_dict[hall].get_hall_type() == 's':
                    new_list.append(hall)
            chosen_hall = np.random.choice(new_list)
            hall_to_replace = np.random.choice(r_hall)
        move = HallUnaryMove(course_row, course_col, hall_to_replace, chosen_hall, UNARY_HALL_MOVE)
        if self.check_hall_unary_legal_move(move):
            self.apply_move(move)


    def apply_hall_unary_move(self, course_row, course_col):
        number_of_halls = (math.ceil((1/3) * len(self.halls_assignment_dict[course_row])))
        available_halls = list(set(range(self.n_halls)) - set(self.time_to_halls[course_col]))
        halls_to_move = np.random.choice(self.halls_assignment_dict[course_row], number_of_halls, replace=False)
        for chosen_hall in halls_to_move:
            for try_ind in range(1, N_TRIES + 1):
                # chosen_hall = np.random.choice(self.halls_assignment_dict[course_row])
                hall_to_switch = np.random.choice(available_halls)
                move = HallUnaryMove(course_row, course_col, chosen_hall, hall_to_switch, UNARY_HALL_MOVE) #todo: add constants
                if self.check_hall_unary_legal_move(move):
                    self.apply_move(move)
                    break

    def apply_hall_remove_move(self, course_row, course_col):
        for try_ind in range(len(self.halls_assignment_dict[course_row])):
            hall_to_remove = np.random.choice(self.halls_assignment_dict[course_row])
            updated_capacity = 0
            for hall in self.halls_assignment_dict[course_row]:
                if hall != hall_to_remove:
                    updated_capacity += self.reverse_halls_dict[hall].get_capacity()
            if updated_capacity >= self.reverse_courses_dict[course_row].get_n_students():
                self.halls_assignment_dict[course_row].remove(hall_to_remove)
                self.time_to_halls[course_col].remove(hall_to_remove)
                return


    def apply_hall_binary_move(self, course_row, course_col):
        friend_row = np.random.choice(range(self.n_courses))
        while course_row == friend_row:
            friend_row = np.random.choice(range(self.n_courses))

        chosen_hall = np.random.choice(self.halls_assignment_dict[course_row])
        hall_to_switch = np.random.choice(self.halls_assignment_dict[friend_row])

        move = HallBinaryMove(course_row, course_col, chosen_hall, friend_row, self.time_assignment_dict[friend_row],
                          hall_to_switch, BINARY_HALL_MOVE)

        if self.check_binary_legal_move(move):
            self.apply_move(move)

    def apply_hall_add_move(self, course_row, course_col):
        for try_ind in range(1, N_TRIES + 1):
            available_halls = list(set(range(self.n_halls)) - set(self.time_to_halls[course_col]))
            hall_to_add = np.random.choice(available_halls)
            if self.reverse_halls_dict[hall_to_add].get_hall_type() == self.reverse_courses_dict[course_row].get_hall_type():
                update_dict(course_row, hall_to_add, self.halls_assignment_dict)
                update_dict(course_col, hall_to_add, self.time_to_halls)
                return

    def check_hall_unary_legal_move(self, move):
        # Check whether we are in the proper bounds
        if move.new_hall < 0 or move.new_hall >= self.n_halls:
            return False
        # Check whether the hard constraint between 2 attempts remains satisfied
        elif not self.check_legal_transfer(move.course_row, move.course_time, move.new_hall):
            return False
        return True


    def check_binary_legal_move(self, move):
        if not self.check_legal_transfer(move.first_row, move.first_col, move.second_hall):
            return False
        if not self.check_legal_transfer(move.second_row, move.second_col, move.first_hall):
            return False
        return True


    def check_legal_transfer(self, course_ind, course_time, new_hall):
        # check capacity
        space_in_halls = 0
        for hall in self.halls_assignment_dict[course_ind]:
            space_in_halls += self.reverse_halls_dict[hall].get_capacity()
        if space_in_halls < self.reverse_courses_dict[course_ind].get_n_students():
            return False
        # check that each hall holds no more than one exam in each time slot
        if new_hall in self.time_to_halls[course_time]:
            return False
        # check if the course needs more than 1 halls, that all halls are different from each other
        if new_hall in self.halls_assignment_dict[course_ind]:
            return False
        # check that if the course needs a computer type
        if self.reverse_courses_dict[course_ind].get_hall_type() != self.reverse_halls_dict[new_hall].get_hall_type():
            return False
        return True


    def apply_move(self, move):
        if move.type == UNARY_HALL_MOVE:
            self.halls_assignment_dict[move.course_row].remove(move.old_hall)
            update_dict(move.course_row, move.new_hall, self.halls_assignment_dict)
            self.time_to_halls[move.course_time].remove(move.old_hall)
            update_dict(move.course_time, move.new_hall, self.time_to_halls)
        else:
            self.halls_assignment_dict[move.first_row].remove(move.first_hall)
            update_dict(move.first_row, move.second_hall, self.halls_assignment_dict)
            self.time_to_halls[move.first_col].remove(move.first_hall)
            update_dict(move.first_col, move.second_hall, self.time_to_halls)

            self.halls_assignment_dict[move.second_row].remove(move.second_hall)
            update_dict(move.second_row, move.first_hall, self.halls_assignment_dict)
            self.time_to_halls[move.second_col].remove(move.second_hall)
            update_dict(move.second_col, move.first_hall, self.time_to_halls)


    def get_value(self):
        # value_to_return = self.unfair_assignment()  + self.uncomfortable_assignment() + self.far_locations()[0]
        value_to_return = self.unfair_assignment() + self.squeeze()
        # maybe check difference between needed space to chosen hall space
        print(value_to_return)
        return value_to_return

    def unfair_assignment(self):
        # noraml vs students chairs
        value = 0
        s = 0
        r = 0
        for course_ind, halls in self.halls_assignment_dict.items():
            if self.reverse_courses_dict[course_ind].get_hall_type() == 'c':
                continue
            for hall in halls:
                if self.reverse_halls_dict[hall].get_chair_type() == 'r':
                    r += 1
                else:
                    s += 1
            value += min(r,s)
            # type_array = np.array(list(map(lambda x:self.reverse_halls_dict[x].get_chair_type(), halls)))
            # if np.unique(type_array).shape[0] == 2:
            #     value += 1
        print(f"value is:{value}")
        return value

    def uncomfortable_assignment(self):
        # preference to regular chair over student chair
        count = 0
        for course_ind, halls in self.halls_assignment_dict.items():
            if self.reverse_courses_dict[course_ind].get_hall_type() == 'c':
                continue
            count += sum([1 if self.reverse_halls_dict[hall].get_chair_type() == 's' else 0 for hall in halls])
        return count

    def far_locations(self):
        # close hall to same exam
        count = 0
        quality_check = []
        for halls in self.halls_assignment_dict.values():
            area_array = np.array([self.reverse_halls_dict[hall].get_area() for hall in halls])
            cal = np.sum(np.abs(area_array-np.median(area_array)))
            count += cal
            quality_check.append(cal)
        return count, quality_check

    def squeeze(self):
        val = 0
        for course, halls in self.halls_assignment_dict.items():
            places = 0
            for hall in halls:
                places += self.reverse_halls_dict[hall].get_capacity()
            if places/self.reverse_courses_dict[course].get_n_students() > 1.25:
                val += 1
        return val

    def __copy__(self):
        c_n_courses = self.n_courses
        c_n_halls = self.n_halls
        c_course_dict = self.courses_dict
        c_reverse_course_dict = self.reverse_courses_dict
        c_halls_dict = self.halls_dict
        c_time_assignment_dict = self.time_assignment_dict
        c_halls_assignment_dict = copy.deepcopy(self.halls_assignment_dict)
        c_time_to_halls_dict = copy.deepcopy(self.time_to_halls)
        return ISAHallState(c_n_courses, c_n_halls, c_course_dict, c_reverse_course_dict, c_halls_dict,
                            c_time_assignment_dict, False, c_halls_assignment_dict, c_time_to_halls_dict)

    def __repr__(self):
        repr_val = "Exam Hall Scheduling Is:\n"
        for course, course_halls in self.halls_assignment_dict.items():
            repr_val += f"{course}: {course_halls}\n"
        return repr_val

    def __eq__(self, other):
        eq_count = 0
        for course_ind in self.halls_assignment_dict.keys():
            if set(self.halls_assignment_dict[course_ind]).intersection(set(other.halls_assignment_dict[course_ind])):
                return False
        return True


class HallUnaryMove:

    def __init__(self, course_row, course_time, old_hall, new_hall, move_type):
        self.course_row = course_row
        self.course_time = course_time
        self.old_hall = old_hall
        self.new_hall = new_hall
        self.type = move_type # Determines whether the move is between periods or days

    # def __str__(self):
    #     return f"({self.old_row, self.old_col} -> {self.new_row, self.new_col})"


class HallBinaryMove:

    def __init__(self, first_row, first_col, first_hall, second_row, second_col, second_hall, move_type):
        self.first_row = first_row
        self.first_col = first_col
        self.first_hall = first_hall
        self.second_row = second_row
        self.second_col = second_col
        self.second_hall = second_hall
        self.type = move_type # Binary move type
    #
    # def __str__(self):
    #     return f"({self.first_row, self.first_col} <-> {self.second_row, self.second_col})"

