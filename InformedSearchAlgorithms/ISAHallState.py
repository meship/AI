import itertools
import math
import copy
import random

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
        # return 1 #todo: think more

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
        update_dict(time_sloth, hall_idx, self.time_to_halls)
        return hall_idx

    def set_operation(self, base, list_to_remove, list_to_add):
        return list((set(base) - set(list_to_remove)).union(set(list_to_add)))

    def unary_move(self, course_ind, course_time):
        halls_len = len(self.halls_assignment_dict[course_ind])
        legal_assignment = False
        try_ind = 0
        while not legal_assignment and try_ind < N_TRIES:
            available_halls = self.set_operation(range(self.n_halls), self.time_to_halls[course_time], [])
            random.shuffle(available_halls)
            amount_of_halls = np.random.choice(range(halls_len // 3, (halls_len // 2) + 1))
            halls_indices = np.random.choice(a=self.halls_assignment_dict[course_ind], size=amount_of_halls,
                                             replace=False)
            new_course_halls = self.set_operation(self.halls_assignment_dict[course_ind], halls_indices, [])
            for available_hall_ind in available_halls:
                new_course_halls.append(available_hall_ind)
                if self.is_legal_hall_addition(course_ind, new_course_halls, available_hall_ind):
                    legal_assignment = True
                    break
            if legal_assignment:
                self.update_new_halls_assignment(course_ind, course_time, new_course_halls, halls_indices)
            try_ind += 1

    def is_legal_hall_addition(self, course_ind, course_halls, new_hall_ind):
        if self.reverse_courses_dict[course_ind].get_hall_type() != \
                self.reverse_halls_dict[new_hall_ind].get_hall_type():
            return False
        new_capacity = sum([self.reverse_halls_dict[hall].get_capacity() for hall in course_halls])
        if new_capacity < self.reverse_courses_dict[course_ind].get_n_students():
            return False
        return True

    def update_new_halls_assignment(self, course_ind, course_time, halls_to_add, halls_to_remove):
        self.halls_assignment_dict[course_ind] = halls_to_add.copy()
        self.time_to_halls[course_time] = self.set_operation(self.time_to_halls[course_time], halls_to_remove,
                                                             halls_to_add)

    def binary_move(self, course_ind, course_time):
        possible_friend_courses = list(filter(lambda x: self.reverse_courses_dict[x].get_hall_type() ==
                                                        self.reverse_courses_dict[course_ind].get_hall_type(),
                                              range(self.n_courses)))
        possible_friend_courses.remove(course_ind)
        legal_swap = False
        try_ind = 0
        while not legal_swap and try_ind < N_TRIES:
            friend_course = np.random.choice(possible_friend_courses)
            max_amount = min(len(self.halls_assignment_dict[course_ind]), len(self.halls_assignment_dict[friend_course]))
            amount_to_switch = np.random.choice(max_amount)
            indices_to_switch = np.random.choice(a=self.halls_assignment_dict[course_ind], size=amount_to_switch,
                                                 replace=False)
            friend_indices_to_switch = np.random.choice(a=self.halls_assignment_dict[friend_course],
                                                        size=amount_to_switch, replace=False)
            my_new_indices = self.set_operation(self.halls_assignment_dict[course_ind], indices_to_switch,
                                                friend_indices_to_switch)
            friend_new_indices = self.set_operation(self.halls_assignment_dict[friend_course], friend_indices_to_switch,
                                                    indices_to_switch)
            if self.check_legal_swap(course_ind, friend_course, my_new_indices, friend_new_indices):
                self.apply_binary_action(course_ind, course_time, indices_to_switch, my_new_indices,
                                         friend_course, friend_indices_to_switch, friend_new_indices)
                legal_swap = True
            try_ind += 1

    def check_legal_swap(self, course_ind, friend_course, my_new_indices, friend_new_indices):
        course_time = self.time_assignment_dict[course_ind]
        for hall_ind in my_new_indices:
            if hall_ind in self.time_to_halls[course_time] and hall_ind not in self.halls_assignment_dict[course_ind]:
                return False
        friend_time = self.time_assignment_dict[friend_course]
        for hall_ind in friend_new_indices:
            if hall_ind in self.time_to_halls[friend_time] and hall_ind not in self.halls_assignment_dict[friend_course]:
                return False
        new_capacity = sum([self.reverse_halls_dict[hall].get_capacity() for hall in my_new_indices])
        if new_capacity < self.reverse_courses_dict[course_ind].get_n_students():
            return False
        new_capacity = sum([self.reverse_halls_dict[hall].get_capacity() for hall in friend_new_indices])
        if new_capacity < self.reverse_courses_dict[friend_course].get_n_students():
            return False
        return True

    def apply_binary_action(self, course_ind, course_time, indices_to_switch, my_new_indices, friend_course,
                            friend_indices_to_switch, friend_new_indices):
        self.halls_assignment_dict[course_ind] = my_new_indices.copy()
        self.halls_assignment_dict[friend_course] = friend_new_indices.copy()
        self.time_to_halls[course_time] = self.set_operation(self.time_to_halls[course_time], indices_to_switch,
                                                             friend_indices_to_switch)
        friend_time = self.time_assignment_dict[friend_course]
        self.time_to_halls[friend_time] = self.set_operation(self.time_to_halls[friend_time], friend_indices_to_switch,
                                                             indices_to_switch)

    def get_value(self):
        value_to_return = self.unfair_assignment() + self.squeeze() + self.uncomfortable_assignment() + \
                          1.5 * self.far_locations()
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
            value += min(r, s) / (r + s)
        return value

    def uncomfortable_assignment(self):
        # preference to regular chair over student chair
        count = 0
        for course_ind, halls in self.halls_assignment_dict.items():
            if self.reverse_courses_dict[course_ind].get_hall_type() == 'c':
                continue
            count += (sum([1 if self.reverse_halls_dict[hall].get_chair_type() == 's' else 0 for hall in halls])) / \
                     len(halls)
        return count

    def far_locations(self):
        # close hall to same exam
        count = 0
        for halls in self.halls_assignment_dict.values():
            area_array = np.array([self.reverse_halls_dict[hall].get_area() for hall in halls])
            cal = np.mean(np.abs(area_array-np.median(area_array))) / np.max(area_array)
            count += cal
        return count

    def squeeze(self):
        val = 0
        for course, halls in self.halls_assignment_dict.items():
            places = 0
            for hall in halls:
                places += self.reverse_halls_dict[hall].get_capacity()
            if places/self.reverse_courses_dict[course].get_n_students() > SQUEEZE_RATIO:
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
        for course_ind in self.halls_assignment_dict.keys():
            if set(self.halls_assignment_dict[course_ind]).intersection(set(other.halls_assignment_dict[course_ind])):
                return False
        return True

