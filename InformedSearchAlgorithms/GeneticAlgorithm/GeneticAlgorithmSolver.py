from InformedSearchAlgorithms.GeneticAlgorithm.GeneticAlgorithmGeneration import *
from InformedSearchAlgorithms.GeneticAlgorithm.GeneticAlgorithmComplexGeneration import *


class GeneticAlgorithmSolver:

    def __init__(self, n_courses, n_times, courses_to_rows_dict, reverse_courses_dict,
                 times_to_cols_dict, reverse_times_to_cols_dict, times_to_days_dict,
                 population_size, generations_num,
                 complex_problem=False, n_halls=None, halls_to_cols_dict=None, reverse_halls_to_col_dict=None,
                 time_assignment_dict={}):

        if not complex_problem:
            self.generation = GeneticAlgorithmGeneration(n_courses, n_times, courses_to_rows_dict, reverse_courses_dict,
                                                         times_to_cols_dict, reverse_times_to_cols_dict,
                                                         times_to_days_dict, population_size, complex_problem,
                                                         n_halls, halls_to_cols_dict, reverse_halls_to_col_dict)
        else:
            self.generation = GeneticAlgorithmComplexGeneration(n_courses, n_times, n_halls, courses_to_rows_dict,
                                                                reverse_courses_dict, halls_to_cols_dict,
                                                                reverse_halls_to_col_dict, time_assignment_dict,
                                                                population_size)
        self.generation_num = generations_num
        self.best_child = None

    def solve(self):
        for generation in range(self.generation_num):
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

    def check_solution_quality(self):
        print("Results: ")
        print(f"Duplicate status: {self.best_child.check_duplicates()}")
        print(f"Difference status: ")
        diff_results = self.best_child.check_exams_diff()
        for pair, diff in diff_results.items():
            print(f"({pair[0]}, {pair[1]}): {diff}")
        print(f"Number of Friday exams: {self.best_child.exam_on_friday_constraint()}")
        print(f"Number of Sunday morning exams: {self.best_child.exam_on_sunday_morning_constraint()}")
        print(f"Number of evening exams: {self.best_child.exam_on_evening_constraint()}")
        print(f"Number of Math NOT morning exams: {self.best_child.math_exam_on_morning_constraint()}")

    def check_hall_solution_quality(self):
        print("Results: ")
        print(f"Number of unfair assignments with differyent chair types: {self.best_child.unfair_assignment()}")
        average_ratio = list()
        for time_slot in range(self.best_child.n_times):
            if time_slot not in self.best_child.time_to_halls.keys():
                continue
            average_ratio.append(sum([1 if self.best_child.reverse_halls_dict[hall].get_chair_type() == 's'
                                     else 0 for hall in self.best_child.time_to_halls[time_slot]]))
        print(f"General ratio between halls assigned with type s to the whole assignment: {np.mean(average_ratio)}")
        print(f"Distance: {self.best_child.far_locations()[1]}")
