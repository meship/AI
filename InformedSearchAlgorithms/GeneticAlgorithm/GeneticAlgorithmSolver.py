from InformedSearchAlgorithms.GeneticAlgorithm.GeneticAlgorithmGeneration import *
from InformedSearchAlgorithms.GeneticAlgorithm.GeneticAlgorithmComplexGeneration import *


class GeneticAlgorithmSolver:

    def __init__(self, n_courses, n_times, courses_to_rows_dict, reverse_courses_dict,
                 times_to_cols_dict, reverse_times_to_cols_dict, times_to_days_dict,
                 population_size, generations_num, callback=None,
                 complex_problem=False, n_halls=None, halls_to_cols_dict=None, reverse_halls_to_col_dict=None,
                 time_assignment_dict={}):

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
        self.best_child = None

    def solve(self):
        for generation in range(self.generation_num):
            if self.callback:
                gen_values = np.array([child.get_value() for child in self.generation.population_])
                gen_average_value = np.mean(gen_values)
                gen_best_value = gen_values.min()
                self.callback(gen_average_value, gen_best_value)
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
        print(f"Number of unfair assignments with different chair types: ")
        for course, halls in self.best_child.halls_assignment_dict.items():
            r, s = 0, 0
            for hall_ind in halls:
                if self.best_child.reverse_halls_dict[hall_ind].get_chair_type() == "s":
                    s += 1
                elif self.best_child.reverse_halls_dict[hall_ind].get_chair_type() == "r":
                    r += 1
                else:
                    break
            else:
                unfair_assignment = min(r, s)
                if unfair_assignment:
                    print(f"{self.best_child.reverse_courses_dict[course]}: student: {s}, regular: {r}")
        total_halls_assigned = 0
        student_chair_halls = 0
        for course, halls in self.best_child.halls_assignment_dict.items():
            total_halls_assigned += len(halls)
            for hall_ind in halls:
                if self.best_child.reverse_halls_dict[hall_ind].get_chair_type() == "s":
                    student_chair_halls += 1
        print(f"\nNumber of halls with student chairs assigned {student_chair_halls} out of {total_halls_assigned} halls")
        print(f"\nRatio number between halls capacity assigned and exam number of students: ")
        for course, halls, in self.best_child.halls_assignment_dict.items():
            capacity = sum([self.best_child.reverse_halls_dict[hall].get_capacity() for hall in halls])
            ratio = capacity/self.best_child.reverse_courses_dict[course].get_n_students()
            if ratio > SQUEEZE_RATIO:
                print(f"{self.best_child.reverse_courses_dict[course]}: {ratio}")
        print("\nAreas of each course assigned: ")
        for course, halls in self.best_child.halls_assignment_dict.items():
            print(f"{self.best_child.reverse_courses_dict[course]}: "
                  f"{[self.best_child.reverse_halls_dict[hall].get_area() for hall in halls]}")
        # print(f"Distance: {self.best_child.far_locations()[1]}")
