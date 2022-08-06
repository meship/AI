from PureConstraintProblem.SolvePureCSP import *
from InformedSearchAlgorithms.ISASolver import *
import time
import plotly.graph_objects as go
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


if __name__ == '__main__':
    domain, number_to_real_date_dict = make_domain(sys.argv[-2], sys.argv[-1])
    change_periods_date = int(MOED_A_RATIO * len(domain))
    times_list = list()
    if sys.argv[1] == CHOICE_CSP:
        create_pure_constraint_problem_graphs(11, solve_CSP, "CSP")
    elif sys.argv[1] == CHOICE_WCSP:
        create_pure_constraint_problem_graphs(8, solve_WCSP, "WCSP")
    elif sys.argv[1] == GENETIC_ALGORITHM:
        courses_data = pd.read_csv(ISA_COURSE_DATABASE3)
        courses = get_courses(courses_data)
        representative_times, number_to_real_date_dict = make_domain(sys.argv[2], sys.argv[3])
        n_courses, n_times, courses_to_rows_dict, reverse_courses_dict, times_to_cols_dict, reverse_times_to_cols_dict = \
            preprocess_courses(courses, representative_times)
        hours_dict = {MORNING_EXAM: (9, 0), NOON_EXAM: (13, 30), EVENING_EXAM: (17, 0)}
        average_values, best_values = list(), list()


        def record_values(avg_value, best_val):
            average_values.append(avg_value)
            best_values.append(best_val)

        solve_GA(n_courses, n_times, courses_to_rows_dict, reverse_courses_dict, times_to_cols_dict,
             reverse_times_to_cols_dict, number_to_real_date_dict, hours_dict, courses, record_values)

        fig = go.Figure(data=[go.Scatter(x=np.arange(len(average_values)), y=average_values, mode='markers + lines', )],
                        layout=go.Layout(title=f"GA Average and Best as a Function of Gen Number",
                                         xaxis=dict(title=r"iteration number"),
                                         yaxis=dict(title=r"fitness value")))
        fig.show()






