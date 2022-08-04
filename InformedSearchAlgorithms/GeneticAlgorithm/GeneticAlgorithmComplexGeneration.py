from InformedSearchAlgorithms.ISAHallState import *
from Utils.utils import add_list_to_dict


class GeneticAlgorithmComplexGeneration:
    def __init__(self, n_courses, n_times, n_halls, course_to_row_dict, reverse_courses_dict,
                 halls_to_cols_dict, reverse_halls_to_col_dict, time_assignment_dict,
                 population_size):

        self.n_courses = n_courses
        self.n_times = n_times
        self.n_halls = n_halls
        self.course_to_row_dict = course_to_row_dict
        self.reverse_courses_dict = reverse_courses_dict
        self.halls_to_cols_dict = halls_to_cols_dict
        self.reverse_halls_to_col_dict = reverse_halls_to_col_dict
        self.time_assignment_dict = time_assignment_dict
        self.population_size_ = population_size
        self.population_ = self.create_initial_population(n_courses, n_times, n_halls, course_to_row_dict, reverse_courses_dict,
                                                          halls_to_cols_dict, reverse_halls_to_col_dict,
                                                          time_assignment_dict)

    def create_initial_population(self, n_courses, n_times, n_halls, course_to_row_dict, reverse_courses_dict,
                                     halls_to_cols_dict, reverse_halls_to_col_dict, time_assignment_dict):
        population = list()
        for i in range(self.population_size_):
            print(f"Creating child {i}")
            new_child = ISAHallState(n_courses, n_times, n_halls, course_to_row_dict, reverse_courses_dict,
                                     halls_to_cols_dict, reverse_halls_to_col_dict, time_assignment_dict,
                                     True)
            for child in population:
                while child == new_child:
                    new_child = ISAHallState(n_courses, n_times, n_halls, course_to_row_dict, reverse_courses_dict,
                                     halls_to_cols_dict, reverse_halls_to_col_dict, time_assignment_dict,
                                     True)
            population.append(new_child)
        return population

    def create_new_generation(self):
        new_population = list()
        probabilities = np.empty(self.population_size_)
        for i, element in enumerate(self.population_):
            probabilities[i] = -element.get_value()
        probabilities -= probabilities.min()
        if sum(probabilities) == 0:
            for course, halls in self.population_[0].halls_assignment_dict.items():
                str = f"({self.time_assignment_dict[course]}) {self.reverse_courses_dict[course]}: "
                for hall in halls:
                    str += self.reverse_halls_to_col_dict[hall].get_name() + " "
                print(str)
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
                # new_population.append(parents[1])
                children_amount += 1
        self.population_ = new_population

    def reproduce(self, parent1, parent2, n_attempts):
        valid_child_1, valid_child_2 = False, False
        attempt = 0
        while not valid_child_1 and not valid_child_2 and attempt < n_attempts:
            cross_over_point = np.random.choice(self.n_courses)
            assignment1, assignment2 = dict(), dict()
            time_to_halls_dict1, time_to_halls_dict2 = dict(), dict()
            for i in range(self.n_courses):
                if i <= cross_over_point:
                    assignment1[i] = parent1.halls_assignment_dict[i]
                    assignment2[i] = parent2.halls_assignment_dict[i]
                else:
                    assignment1[i] = parent2.halls_assignment_dict[i]
                    assignment2[i] = parent1.halls_assignment_dict[i]

            for course_ind, course_halls in assignment1.items():
                add_list_to_dict(self.time_assignment_dict[course_ind], course_halls, time_to_halls_dict1)

            for course_ind, course_halls in assignment2.items():
                add_list_to_dict(self.time_assignment_dict[course_ind], course_halls, time_to_halls_dict2)

            valid_child_1 = self.check_valid_assignment(time_to_halls_dict1)
            valid_child_2 = self.check_valid_assignment(time_to_halls_dict2)

            if valid_child_1 and valid_child_2:
                state_child1 = ISAHallState(self.n_courses, self.n_times, self.n_halls, self.course_to_row_dict,
                                            self.reverse_courses_dict, self.halls_to_cols_dict,
                                            self.reverse_halls_to_col_dict, self.time_assignment_dict,
                                            False, assignment1, time_to_halls_dict1.copy())

                state_child2 = ISAHallState(self.n_courses, self.n_times, self.n_halls, self.course_to_row_dict,
                                            self.reverse_courses_dict, self.halls_to_cols_dict,
                                            self.reverse_halls_to_col_dict, self.time_assignment_dict,
                                            False, assignment2, time_to_halls_dict2.copy())
                return state_child1 if -state_child1.get_value() > -state_child2.get_value() else state_child2
            elif valid_child_1:
                return ISAHallState(self.n_courses, self.n_times, self.n_halls, self.course_to_row_dict,
                                            self.reverse_courses_dict, self.halls_to_cols_dict,
                                            self.reverse_halls_to_col_dict, self.time_assignment_dict,
                                            False, assignment1, time_to_halls_dict1.copy())
            elif valid_child_2:
                return ISAHallState(self.n_courses, self.n_times, self.n_halls, self.course_to_row_dict,
                                            self.reverse_courses_dict, self.halls_to_cols_dict,
                                            self.reverse_halls_to_col_dict, self.time_assignment_dict,
                                            False, assignment2, time_to_halls_dict2.copy())
            else:
                attempt += 1

    def check_valid_assignment(self, time_to_halls_dict):
        # check that each hall holds no more than one exam in each time slot
        for halls_list in time_to_halls_dict.values():
            if len(set(halls_list)) != len(halls_list):
                return False
        return True

    def mutate(self, child):
        if np.random.choice(PROB_DOMAIN) <= MUTAION_PROB:
            # randomly choosing how many courses will be mutated
            number_of_genes = np.random.choice(range(self.n_courses//2, self.n_courses))
            chosen_courses_ind = np.random.choice(range(self.n_courses), size=number_of_genes, replace=False)
            for course_ind in chosen_courses_ind:
                # make the mutate
                # child.apply_try_move(course_ind, child.time_assignment_dict[course_ind])
                move = np.random.choice([0, 1, ADD_HALL, REMOVE_HALL],
                                        p=[0.5, 0.5, 0, 0])
                if move == 0:
                    child.apply_hall_unary_move(course_ind, child.time_assignment_dict[course_ind])
                elif move == 1:
                    child.apply_hall_binary_move(course_ind, child.time_assignment_dict[course_ind])
                elif move == ADD_HALL:
                    child.apply_hall_add_move(course_ind, child.time_assignment_dict[course_ind])
                else:
                    child.apply_hall_remove_move(course_ind, child.time_assignment_dict[course_ind])
        return child







