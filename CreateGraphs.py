from PureConstraintProblem.SolvePureCSP import *
import time

if __name__ == '__main__':
    domain, number_to_real_date_dict = make_domain(sys.argv[-2], sys.argv[-1])
    change_periods_date = int(MOED_A_RATIO * len(domain))
    if sys.argv[1] == CHOICE_CSP:
        for n_courses in range(1, 15):
            variables = make_variables(change_periods_date, n_courses)
            start = time.time()
            print(solve_CSP(variables, domain, change_periods_date))
            end = time.time()
            print(end - start)
    else:
        for n_courses in range(1, 15):
            variables = make_variables(change_periods_date, n_courses)
            start = time.time()
            solve_WCSP(variables, domain, change_periods_date)
            end = time.time()
            print(end - start)




