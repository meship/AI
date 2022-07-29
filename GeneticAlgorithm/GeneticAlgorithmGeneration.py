import numpy as np
from GeneticAlgorithmState import *


class GeneticAlgorithmGeneration:
    def __init__(self, n_courses, n_times, courses_to_rows_dict,
                 times_to_cols_dict, reverse_times_to_cols_dict,
                 times_to_dates_dict, population_size, generation_number=0):
        self.n_courses_ = n_courses
        self.n_times_ = n_times
        self.course_to_rows_dict_ = courses_to_rows_dict
        self.times_to_cols_dict_ = times_to_cols_dict
        self.reverse_times_to_cols_dict_ = reverse_times_to_cols_dict
        self.times_to_dates_dict_ = times_to_dates_dict
        self.population_size_ = population_size
        self.generation_num_ = generation_number
        self.population_ = self.create_initial_population(n_courses, n_times, courses_to_rows_dict,
                                                          times_to_cols_dict, reverse_times_to_cols_dict,
                                                          {}, times_to_dates_dict)

    def create_initial_population(self, n_courses, n_times, courses_to_rows_dict,
                                  times_to_cols_dict, reverse_times_to_cols_dict, assignment_dict,
                                  times_to_dates_dict):
        population = list()
        for i in range(self.population_size_):
            new_child = GeneticAlgorithmState(n_courses, n_times, courses_to_rows_dict, times_to_cols_dict,
                                              reverse_times_to_cols_dict, assignment_dict, True, times_to_dates_dict)
            for child in population:
                while child == new_child:
                    new_child = GeneticAlgorithmState(n_courses, n_times, courses_to_rows_dict, times_to_cols_dict,
                                                      reverse_times_to_cols_dict, assignment_dict, True,
                                                      times_to_dates_dict)
            population.append(new_child)
        return population

    def create_new_generation(self):
        new_population = list()
        probabilities = np.empty(self.population_size_)
        for i, element in enumerate(self.population_):
            probabilities[i] = element.calculate_fitness()
        probabilities = probabilities / sum(probabilities)
        children_amount = 0
        while children_amount < self.population_size_:
            parents = np.random.choice(a=self.population_, size=2, replace=True, p=probabilities)
            child = self.reproduce(parents[0], parents[1], N_ATTEMPTS_TO_REPRODUCE)
            if child is not None:
                new_population.append(child)
                children_amount += 1
        self.population_ = new_population

    def reproduce(self, parent1, parent2, n_attempts):
        valid_child_1, valid_child_2 = False, False
        attempt = 0
        while not valid_child_1 and not valid_child_2 and attempt < n_attempts:
            cross_over_point = np.random.choice(self.n_courses_)
            assignment1, assignment2 = dict(), dict()
            for i in range(self.n_courses_):
                if i <= cross_over_point:
                    assignment1[i] = parent1.assignment_dict[i]
                    assignment2[i] = parent2.assignment_dict[i]
                else:
                    assignment1[i] = parent2.assignment_dict[i]
                    assignment2[i] = parent1.assignment_dict[i]
            valid_child_1 = self.check_valid_assignment(assignment1)
            valid_child_2 = self.check_valid_assignment(assignment2)
            if valid_child_1 and valid_child_2:
                state_child1 = GeneticAlgorithmState(self.n_courses_, self.n_times_, self.course_to_rows_dict_,
                                                     self.times_to_cols_dict_, self.reverse_times_to_cols_dict_,
                                                     assignment1, False, self.times_to_dates_dict_)
                state_child2 = GeneticAlgorithmState(self.n_courses_, self.n_times_, self.course_to_rows_dict_,
                                                     self.times_to_cols_dict_, self.reverse_times_to_cols_dict_,
                                                     assignment2, False, self.times_to_dates_dict_)
                return state_child1 if state_child1.get_fitness() > state_child2.get_fitness() else state_child2
            elif valid_child_1:
                return GeneticAlgorithmState(self.n_courses_, self.n_times_, self.course_to_rows_dict_,
                                             self.times_to_cols_dict_, self.reverse_times_to_cols_dict_,
                                             assignment1, False, self.times_to_dates_dict_)
            elif valid_child_2:
                return GeneticAlgorithmState(self.n_courses_, self.n_times_, self.course_to_rows_dict_,
                                             self.times_to_cols_dict_, self.reverse_times_to_cols_dict_,
                                             assignment2, False, self.times_to_dates_dict_)
            else:
                attempt += 1

    def check_valid_assignment(self, assignment_to_check):
        # Check whether there are no equal assignments
        assignment_vals = assignment_to_check.values()
        if len(assignment_vals) != len(np.unique(np.array(list(assignment_vals)))):
            return False
        # Check whether all first attempts are prior to all the second attempts
        for course_ind in range(self.n_courses_ // 2):
            if assignment_to_check[course_ind + self.n_courses_ // 2] - assignment_to_check[course_ind] < ATTEMPTS_DIFF:
                return False
        return True






