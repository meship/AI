import pandas as pd
import numpy as np
from Course import Course
from CSPExams import CSPExams
import datetime
from Constants import *


def make_variables(change_periods_date):
    course_data = pd.read_csv(COURSE_DATABASE)

    courses_list = list()
    for index in course_data.index:
        courses_list.append(Course(course_data[COURSE_ATTRIBUTES[0]][index] + ' - A',
                                   course_data[COURSE_ATTRIBUTES[1]][index],
                                   course_data[COURSE_ATTRIBUTES[2]][index],
                                   course_data[COURSE_ATTRIBUTES[3]][index],
                                   course_data[COURSE_ATTRIBUTES[4]][index],
                                   MOED_A,
                                   change_periods_date))

        courses_list.append(Course(course_data[COURSE_ATTRIBUTES[0]][index] + ' - B',
                                   course_data[COURSE_ATTRIBUTES[1]][index],
                                   course_data[COURSE_ATTRIBUTES[2]][index],
                                   course_data[COURSE_ATTRIBUTES[3]][index],
                                   course_data[COURSE_ATTRIBUTES[4]][index],
                                   MOED_B,
                                   change_periods_date))
    return courses_list


def make_domain(start_date, end_date):
    #todo: if time premits - maybe import google calender?
    #todo: add hagi israel and

    # dates in string format
    start_date = start_date
    end_date = end_date

    # convert string to date object
    d1 = datetime.datetime.strptime(start_date, "%Y/%m/%d")
    d2 = datetime.datetime.strptime(end_date, "%Y/%m/%d")
    # difference between dates in timedelta
    delta = d2 - d1

    number_to_real_date_dict = dict()
    domain = [0]
    for number in range(1, delta.days + 2):
        if d1.weekday() == SATURDAY:
            d1 = d1 + datetime.timedelta(days=1)
            continue
        number_to_real_date_dict[number + MORNING_EXAM] = d1
        domain.append(number + MORNING_EXAM)

        if d1.weekday() != FRIDAY:
            number_to_real_date_dict[number + NOON_EXAM] = d1
            number_to_real_date_dict[number + EVENING_EXAM] = d1
            domain.append(number + NOON_EXAM)
            domain.append(number + EVENING_EXAM)
        d1 = d1 + datetime.timedelta(days=1)
    return np.array(domain), number_to_real_date_dict


if __name__ == '__main__':
    domain, number_to_real_date_dict = make_domain('2022/01/15', '2022/04/08')
    change_periods_date = int(MOED_A_RATIO * len(domain))
    variables = make_variables(change_periods_date)
    # variables.sort(key=lambda x: x.get_attempt())
    CSP_Exam = CSPExams(variables, domain, change_periods_date)
    CSP_Exam.create_constraints()
    CSP_Exam.arc3()
    print("finished arc3")
    # result = CSP_Exam.backtracking_search()
    # result = CSP_Exam.degree_heuristic({})
    # result = CSP_Exam.minimum_remaining_vars({}, CSP_Exam.domains)
    # result = CSP_Exam.least_constraining_value({})
    result = CSP_Exam.both_heuristics({}, CSP_Exam.domains)
    for key, value in result.items():
        print(f"{key}: {value}, {number_to_real_date_dict[value]}")

