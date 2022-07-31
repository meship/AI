from InformedSearchAlgorithms.GeneticAlgorithm.GeneticAlgorithmGeneration import *

class GeneticAlgorithmSolver:

    def __init__(self, n_courses, n_times, courses_to_rows_dict,
                 times_to_cols_dict, reverse_times_to_cols_dict, times_to_days_dict,
                 population_size, generations_num=300):

        self.generation = GeneticAlgorithmGeneration(n_courses, n_times, courses_to_rows_dict,
                                                     times_to_cols_dict, reverse_times_to_cols_dict,
                                                     times_to_days_dict, population_size)
        self.generation_num = generations_num
        self.best_child = None

    def solve(self):
        for generation in range(self.generation_num):
            self.generation.create_new_generation()

        best_value, best_child = np.Inf, None
        for child in self.generation.population_:
            current_value = child.get_value()
            if current_value < best_value:
                best_value  = current_value
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
