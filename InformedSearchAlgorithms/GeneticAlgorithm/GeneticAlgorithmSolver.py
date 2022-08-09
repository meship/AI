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


