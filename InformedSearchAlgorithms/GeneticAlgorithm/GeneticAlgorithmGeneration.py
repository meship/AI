from InformedSearchAlgorithms.ISAState import *


class GeneticAlgorithmGeneration:
    def __init__(self, n_courses, n_times, courses_to_rows_dict, reverse_courses_dict,
                 times_to_cols_dict, reverse_times_to_cols_dict,
                 times_to_dates_dict, population_size):
        self.n_courses_ = n_courses
        self.n_times_ = n_times
        self.course_to_rows_dict_ = courses_to_rows_dict
        self.reverse_courses_dict_ = reverse_courses_dict
        self.times_to_cols_dict_ = times_to_cols_dict
        self.reverse_times_to_cols_dict_ = reverse_times_to_cols_dict
        self.times_to_dates_dict_ = times_to_dates_dict
        self.population_size_ = population_size
        self.population_ = self.create_initial_population(n_courses, n_times, courses_to_rows_dict,
                                                          reverse_courses_dict, times_to_cols_dict,
                                                          reverse_times_to_cols_dict, {}, times_to_dates_dict)

    def create_initial_population(self, n_courses, n_times, courses_to_rows_dict, reverse_courses_dict,
                                  times_to_cols_dict, reverse_times_to_cols_dict, assignment_dict,
                                  times_to_dates_dict):
        population = list()
        for i in range(self.population_size_):
            # print(f"Creating child {i}")
            new_child = ISAState(n_courses, n_times, courses_to_rows_dict, reverse_courses_dict, times_to_cols_dict,
                                 reverse_times_to_cols_dict, assignment_dict, None, times_to_dates_dict, True)
            for child in population:
                while child == new_child:
                    new_child = ISAState(n_courses, n_times, courses_to_rows_dict, reverse_courses_dict,
                                         times_to_cols_dict, reverse_times_to_cols_dict, assignment_dict, None,
                                         times_to_dates_dict, True)
            population.append(new_child)
        return population

    def create_new_generation(self):
        new_population = list()
        probabilities = np.empty(self.population_size_)
        # print(f"Size is:{probabilities.shape}")
        # print(f"len is: {len(self.population_)}")
        for i, element in enumerate(self.population_):
            probabilities[i] = -element.get_value() # [-10, -4 , -2] -> [0, 6, 8]
        probabilities -= probabilities.min()
        probabilities = probabilities / sum(probabilities)
        children_amount = 0
        while children_amount < self.population_size_:
            parents = np.random.choice(a=self.population_, size=2, replace=False, p=probabilities)
            if np.random.choice(PROB_DOMAIN) <= CROSSOVER_PROB:
                child = self.reproduce(parents[0], parents[1], N_ATTEMPTS_TO_REPRODUCE)
                if child is not None:
                    new_population.append(self.mutate(child))
                    children_amount += 1
            else:
                new_population.append(parents[0])
                children_amount += 1
        self.population_ = new_population

    def reproduce(self, parent1, parent2, n_attempts):
        valid_child_1, valid_child_2 = False, False
        attempt = 0
        while not valid_child_1 and not valid_child_2 and attempt < n_attempts:
            cross_over_point = np.random.choice(self.n_courses_)
            assignment1, assignment2 = dict(), dict()
            reverse_assignment1, reverse_assignment2 = dict(), dict()
            for i in range(self.n_courses_):
                if i <= cross_over_point:
                    assignment1[i] = parent1.assignment_dict[i]
                    assignment2[i] = parent2.assignment_dict[i]
                else:
                    assignment1[i] = parent2.assignment_dict[i]
                    assignment2[i] = parent1.assignment_dict[i]

            for course_ind, course_time in assignment1.items():
                update_dict(course_time, course_ind, reverse_assignment1)

            for course_ind, course_time in assignment2.items():
                update_dict(course_time, course_ind, reverse_assignment2)

            valid_child_1 = self.check_valid_assignment(assignment1, reverse_assignment1)
            valid_child_2 = self.check_valid_assignment(assignment2, reverse_assignment2)
            if valid_child_1 and valid_child_2:
                state_child1 = ISAState(self.n_courses_, self.n_times_, self.course_to_rows_dict_,
                                        self.reverse_courses_dict_,self.times_to_cols_dict_,
                                        self.reverse_times_to_cols_dict_,assignment1,reverse_assignment1,
                                        self.times_to_dates_dict_, False)
                state_child2 = ISAState(self.n_courses_, self.n_times_, self.course_to_rows_dict_,
                                        self.reverse_courses_dict_, self.times_to_cols_dict_,
                                        self.reverse_times_to_cols_dict_, assignment2,reverse_assignment2,
                                        self.times_to_dates_dict_, False)
                return state_child1 if -state_child1.get_value() > -state_child2.get_value() else state_child2
            elif valid_child_1:
                return ISAState(self.n_courses_, self.n_times_, self.course_to_rows_dict_, self.reverse_courses_dict_,
                                self.times_to_cols_dict_, self.reverse_times_to_cols_dict_,
                                assignment1, reverse_assignment1,self.times_to_dates_dict_, False)
            elif valid_child_2:
                return ISAState(self.n_courses_, self.n_times_, self.course_to_rows_dict_, self.reverse_courses_dict_,
                                self.times_to_cols_dict_, self.reverse_times_to_cols_dict_,
                                assignment2, reverse_assignment2, self.times_to_dates_dict_, False)
            else:
                attempt += 1

    def check_valid_assignment(self, assignment_to_check, reverse_assignment_to_check):
        # Check whether there are no equal assignments
        # assignment_vals = assignment_to_check.values()
        # if len(assignment_vals) != len(np.unique(np.array(list(assignment_vals)))):
        #     return False
        reverse_assignment_dict = dict()
        for course_ind, course_time in assignment_to_check.items():
            if course_time not in reverse_assignment_dict.keys():
                reverse_assignment_dict[course_time] = [course_ind]
            else:
                for already_in_course in reverse_assignment_dict[course_time]:
                    if set(self.reverse_courses_dict_[already_in_course].get_faculties()).\
                            intersection(set(self.reverse_courses_dict_[course_ind].get_faculties())):
                        return False
                reverse_assignment_dict[course_time].append(course_ind)

        # Check whether all the difference between two attempts remains
        for course_ind in range(self.n_courses_ // 2):
            if assignment_to_check[course_ind + self.n_courses_ // 2] - assignment_to_check[course_ind] < ATTEMPTS_DIFF:
                return False

        for time_ind in reverse_assignment_to_check.keys():
            if sum([self.reverse_courses_dict_[course_ind].get_n_students() for course_ind in
                    reverse_assignment_to_check[time_ind]]) \
                    > MAX_STUDENTS_PER_TIME:
                return False
        return True

    def mutate(self, child):
        if np.random.choice(PROB_DOMAIN) <= MUTAION_PROB:
            # randomly choosing how many courses will be mutated
            number_of_genes = np.random.choice(range(self.n_courses_//4, self.n_courses_//2))
            chosen_courses_ind = np.random.choice(range(self.n_courses_), size=number_of_genes, replace=False)
            for course_ind in chosen_courses_ind:
                # make the mutation
                move = np.random.choice([BINARY_MOVE, UNARY_PERIODS_MOVE])
                if move == UNARY_PERIODS_MOVE:
                    child.apply_unary_periods_move(course_ind, child.assignment_dict[course_ind])
                else:
                    child.apply_binary_move(course_ind, child.assignment_dict[course_ind])
        return child









