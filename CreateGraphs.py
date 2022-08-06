from PureConstraintProblem.SolvePureCSP import *
from InformedSearchAlgorithms.ISASolver import *
import time
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
pio.templates.default = "simple_white"


def create_pure_constraint_problem_graphs(max_range, solver, problem_name):
    times_list = list()
    for n_courses in range(1, max_range):
        variables = make_variables(change_periods_date, n_courses)
        start = time.time()
        solver(variables, domain, change_periods_date)
        end = time.time()
        times_list.append(end - start)
    fig = go.Figure(data=[go.Scatter(x=np.arange(1, 11), y=times_list, mode='markers + lines', )],
                    layout=go.Layout(title=f"{problem_name} Time as a Function of Iteration Number",
                                     xaxis=dict(title=r"iteration number"),
                                     yaxis=dict(title=r"time")))
    fig.show()


def create_ga_graphs(course_num=None):
    if course_num:
        courses_data = pd.read_csv(ISA_COURSE_DATABASE3).iloc[:course_num, :]
    else:
        courses_data = pd.read_csv(ISA_COURSE_DATABASE3)
    courses = get_courses(courses_data)
    representative_times, number_to_real_date_dict = make_domain(sys.argv[2], sys.argv[3])
    n_courses, n_times, courses_to_rows_dict, reverse_courses_dict, times_to_cols_dict, reverse_times_to_cols_dict = \
        preprocess_courses(courses, representative_times)
    hours_dict = {MORNING_EXAM: (9, 0), NOON_EXAM: (13, 30), EVENING_EXAM: (17, 0)}
    average_course_values, best_course_values = list(), list()

    def record_course_values(avg_value, best_val):
        average_course_values.append(avg_value)
        best_course_values.append(best_val)

    average_halls_values, best_halls_values = list(), list()

    def record_halls_values(avg_value, best_val):
        average_halls_values.append(avg_value)
        best_halls_values.append(best_val)

    solver, complex_solver = solve_GA(n_courses, n_times, courses_to_rows_dict, reverse_courses_dict,
                                      times_to_cols_dict, reverse_times_to_cols_dict, number_to_real_date_dict,
                                      hours_dict, courses, record_course_values, record_halls_values)
    fig = go.Figure(
        data=[go.Scatter(x=np.arange(len(average_course_values)), y=average_course_values, mode='markers + lines'),
              go.Scatter(x=np.arange(len(best_course_values)), y=best_course_values, mode='markers + lines')],
        layout=go.Layout(title=f"GA Average and Best as a Function of Gen Number in courses",
                         xaxis=dict(title=r"generation number"),
                         yaxis=dict(title=r"fitness value")))
    # fig.show()
    fig = go.Figure(
        data=[go.Scatter(x=np.arange(len(average_halls_values)), y=average_halls_values, mode='markers + lines'),
              go.Scatter(x=np.arange(len(best_halls_values)), y=best_halls_values, mode='markers + lines')],
        layout=go.Layout(title=f"GA Average and Best as a Function of Gen Number in halls",
                         xaxis=dict(title=r"generation number"),
                         yaxis=dict(title=r"fitness value")))
    # fig.show()

    course_to_unfair_assignment, num_of_unfair_courses, student_chair_halls, n_halls, course_to_areas_dict = \
        complex_solver.check_hall_solution_quality(True)
    for course, unfair_assignment in course_to_unfair_assignment.items():
        fig = px.pie(values=list(unfair_assignment), names=['students_chairs','regulars_chairs'],
                     title=f"{course}")
        # fig.show()
    fig = px.pie(values=[num_of_unfair_courses, (n_courses - num_of_unfair_courses)],
                 names=['students_chairs','regulars_chairs'],
                     title=f"Number of Unfair Exams")
    # fig.show()

    fig = px.pie(values=[student_chair_halls, (n_halls - student_chair_halls)],
                 names=['students_chairs_halls', 'regulars_chairs_halls'],
                 title=f"Number of Halls with Students Chairs")
    # fig.show()

    traces = {}
    for course, areas in course_to_areas_dict.items():
        traces[course] = go.Box(name=course, y=areas,
                                        boxpoints='all',
                                        pointpos=0,
                                        marker=dict(color='rgb(84, 173, 39)'),
                                        line=dict(color='rgba(0,0,0,0)'),
                                        fillcolor='rgba(0,0,0,0)')
    # convert data to form required by plotly
    data = list(traces.values())

    # build figure
    fig = go.Figure(data)
    fig.show()



def create_sa_graphs(course_num=None):
    if course_num:
        courses_data = pd.read_csv(ISA_COURSE_DATABASE3).iloc[:course_num, :]
    else:
        courses_data = pd.read_csv(ISA_COURSE_DATABASE3)
    courses = get_courses(courses_data)
    representative_times, number_to_real_date_dict = make_domain(sys.argv[2], sys.argv[3])
    n_courses, n_times, courses_to_rows_dict, reverse_courses_dict, times_to_cols_dict, reverse_times_to_cols_dict = \
        preprocess_courses(courses, representative_times)
    hours_dict = {MORNING_EXAM: (9, 0), NOON_EXAM: (13, 30), EVENING_EXAM: (17, 0)}
    values_list, temp_list = list(), list()

    def record_progress(value, temp):
        values_list.append(value)
        temp_list.append(temp)

    solve_SA(n_courses, n_times, courses_to_rows_dict, reverse_courses_dict, times_to_cols_dict,
             reverse_times_to_cols_dict, number_to_real_date_dict, hours_dict, courses, record_progress)
    fig = go.Figure(
        data=[go.Scatter(x=np.arange(len(values_list)), y=values_list, mode='markers + lines')],
        layout=go.Layout(title=f"SA Values as a Function of Iteration Number",
                         xaxis=dict(title=r"iteration number"),
                         yaxis=dict(title=r"value")))
    fig.show()

    fig = go.Figure(
        data=[go.Scatter(x=np.arange(len(temp_list)), y=temp_list, mode='markers + lines')],
        layout=go.Layout(title=f"SA Temperature as a Function of Iteration Number",
                         xaxis=dict(title=r"iteration number"),
                         yaxis=dict(title=r"temp")))
    fig.show()



if __name__ == '__main__':
    domain, number_to_real_date_dict = make_domain(sys.argv[-2], sys.argv[-1])
    change_periods_date = int(MOED_A_RATIO * len(domain))
    times_list = list()
    if sys.argv[1] == CHOICE_CSP:
        create_pure_constraint_problem_graphs(11, solve_CSP, "CSP")
    elif sys.argv[1] == CHOICE_WCSP:
        create_pure_constraint_problem_graphs(8, solve_WCSP, "WCSP")
    elif sys.argv[1] == GENETIC_ALGORITHM:
        create_ga_graphs(8)
    elif sys.argv[1] == SIMULATED_ANNEALING:
        create_sa_graphs()










