from PureConstraintProblem.ConstriantSatisfactionProblem.CSPExams import CSPExams
from PureConstraintProblem.WeightedConstraintSatisfactionProblem.WCSPExams import WCSPExams
from Utils.Constants import *
import sys
from Utils.utils import make_domain, make_variables




def solve_CSP(variables, domain, change_periods_date):
    variables.sort(key=lambda x: x.get_attempt())
    CSP_Exam = CSPExams(variables, domain, change_periods_date)
    CSP_Exam.create_constraints()
    CSP_Exam.arc3()
    # print("finished arc3")
    if sys.argv[2] == BACKTRACKING:
        return CSP_Exam.backtracking_search()
    elif sys.argv[2] == MINIMUM_REMAINING_VARS:
        return CSP_Exam.minimum_remaining_vars({}, CSP_Exam.get_domains())
    elif sys.argv[2] == DEGREE:
        return CSP_Exam.degree_heuristic({})
    elif sys.argv[2] == LEAST_CONSTRAINING_VALUE:
        return CSP_Exam.least_constraining_value({})
    else:
        return CSP_Exam.both_heuristics({}, CSP_Exam.domains_)


def solve_WCSP(variables, domain, change_periods_date):
    wscp_exams = WCSPExams(variables=variables, domains=domain, change_periods_date=change_periods_date,
                           k=MAXIMUM_COST)
    wscp_exams.create_constraints()
    wscp_exams.arc3()
    # print("finished arc3")
    wscp_exams.branch_and_bound({}, 0, 0)
    return wscp_exams.get_best_assignment()


if __name__ == '__main__':
    # argv[1] = kind, argv[2] = heuristic, argv[3 & 4] = '2022/01/15', '2022/03/08'
    domain, number_to_real_date_dict = make_domain(sys.argv[-2], sys.argv[-1])
    change_periods_date = int(MOED_A_RATIO * len(domain))
    variables = make_variables(change_periods_date, CSP_NUMBER_OF_COURSES)
    if sys.argv[1] == CHOICE_CSP:
        print(solve_CSP(variables, domain, change_periods_date))
    else:
        print(solve_WCSP(variables, domain, change_periods_date))
