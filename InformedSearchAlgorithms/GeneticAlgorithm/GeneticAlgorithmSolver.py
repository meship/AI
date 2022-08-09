from InformedSearchAlgorithms.GeneticAlgorithm.GeneticAlgorithmGeneration import *
from InformedSearchAlgorithms.GeneticAlgorithm.GeneticAlgorithmComplexGeneration import *


class GeneticAlgorithmSolver:

    def __init__(self, n_courses, n_times, courses_to_rows_dict, reverse_courses_dict,
                 times_to_cols_dict, reverse_times_to_cols_dict, times_to_days_dict,
                 population_size, generations_num, callback=None, complex_callback=None,
                 complex_problem=False, n_halls=None, halls_to_cols_dict=None, reverse_halls_to_col_dict=None,
                 time_assignment_dict={}):

        self.complex_problem = complex_problem

        if not complex_problem:
            self.generation = GeneticAlgorithmGeneration(n_courses, n_times, courses_to_rows_dict, reverse_courses_dict,
                                                         times_to_cols_dict, reverse_times_to_cols_dict,
                                                         times_to_days_dict, population_size)
        else:
            self.generation = GeneticAlgorithmComplexGeneration(n_courses, n_times, n_halls, courses_to_rows_dict,
                                                                reverse_courses_dict, halls_to_cols_dict,
                                                                reverse_halls_to_col_dict, time_assignment_dict,
                                                                population_size)

        self.generation_num = generations_num
        self.callback = callback
        self.complex_callback = complex_callback
        self.best_child = None

    def solve(self):
        for generation in range(self.generation_num):
            if self.callback:
                gen_values = np.array([child.get_value() for child in self.generation.population_])
                gen_average_value = np.mean(gen_values)
                gen_best_value = gen_values.min()
                self.callback(gen_average_value, gen_best_value)
            if self.complex_callback:
                gen_values = np.array([child.get_value() for child in self.generation.population_])
                gen_average_value = np.mean(gen_values)
                gen_best_value = gen_values.min()
                self.complex_callback(gen_average_value, gen_best_value)

            self.generation.create_new_generation()

        best_value, best_child = np.Inf, None
        for child in self.generation.population_:
            current_value = child.get_value()
            if current_value < best_value:
                best_value = current_value
                best_child = child
        self.best_child = best_child

    def get_best_child(self):
        return self.best_child

    def check_solution_quality(self, export_to_graph=False):
        to_print = "Results: \n"
        # to_print += f"Duplicate status: {self.best_child.check_duplicates()}")
        to_print += f"Difference status: \n"
        diff_results = self.best_child.check_exams_diff()
        # diff_results_to_graph = dict()
        # for pair, diff in diff_results.items():
        #     to_print += f"({pair[0]}, {pair[1]}): {diff}\n"
        #     if pair[0].get_name() != pair[1].get_name():
        #         diff_results_to_graph[pair[0].get_name(), pair[1].get_name()] = diff
        to_print += f"Number of Friday exams: {self.best_child.exam_on_friday_constraint()}\n"
        to_print += f"Number of Sunday morning exams: {self.best_child.exam_on_sunday_morning_constraint()}\n"
        to_print += f"Number of evening exams: {self.best_child.exam_on_evening_constraint()}\n"
        to_print += f"Number of Math NOT morning exams: {self.best_child.math_exam_on_morning_constraint()}\n"

        if not export_to_graph:
            print(to_print)
        else:
            return diff_results, self.best_child.exam_on_evening_constraint()

    def check_hall_solution_quality(self, export_to_graph=False):

        to_print = "Results: \n"
        to_print += "Number of unfair assignments with different chair types: \n"
        course_to_unfair_assignment = dict()
        num_of_unfair_courses = 0
        for course, halls in self.best_child.halls_assignment_dict.items():
            r, s = 0, 0
            for hall_ind in halls:
                if self.best_child.reverse_halls_dict[hall_ind].get_chair_type() == "s":
                    s += 1
                    # s += self.best_child.reverse_halls_dict[hall_ind].get_capacity()
                elif self.best_child.reverse_halls_dict[hall_ind].get_chair_type() == "r":
                    r += 1
                    # r += self.best_child.reverse_halls_dict[hall_ind].get_capacity()
                else:
                    break
            else:
                unfair_assignment = min(r, s)
                if unfair_assignment:
                    to_print += f"{self.best_child.reverse_courses_dict[course]}: student: {s}, regular: {r}\n"
                    course_to_unfair_assignment[self.best_child.reverse_courses_dict[course]] = (s,r)
                    num_of_unfair_courses += 1

        total_halls_assigned = 0
        student_chair_halls = 0
        for course, halls in self.best_child.halls_assignment_dict.items():
            total_halls_assigned += len(halls)
            for hall_ind in halls:
                # total_halls_assigned += self.best_child.reverse_halls_dict[hall_ind].get_capacity()
                if self.best_child.reverse_halls_dict[hall_ind].get_chair_type() == "s":
                    student_chair_halls += 1
                    # student_chair_halls += self.best_child.reverse_halls_dict[hall_ind].get_capacity()
        to_print += f"\nNumber of halls with student chairs assigned {student_chair_halls} out " \
                    f"of {total_halls_assigned} halls\n"
        to_print += f"\nRatio number between halls capacity assigned and exam number of students: \n"

        for course, halls, in self.best_child.halls_assignment_dict.items():
            capacity = sum([self.best_child.reverse_halls_dict[hall].get_capacity() for hall in halls])
            ratio = capacity/self.best_child.reverse_courses_dict[course].get_n_students()
            if ratio > SQUEEZE_RATIO:
                to_print += f"{self.best_child.reverse_courses_dict[course]}: {ratio}\n"
        to_print += "\nAreas of each course assigned: \n"
        course_to_areas_dict = dict()
        for course, halls in self.best_child.halls_assignment_dict.items():
            course_obj = self.best_child.reverse_courses_dict[course]
            course_to_areas_dict[course_obj] = [self.best_child.reverse_halls_dict[hall].get_area() for hall in halls]
            to_print += f"{course_obj}: {course_to_areas_dict[course_obj]}\n"

        if export_to_graph:
            return course_to_unfair_assignment, num_of_unfair_courses, student_chair_halls, total_halls_assigned,\
                   course_to_areas_dict
        else:
            print(to_print)

