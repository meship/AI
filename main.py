import pandas as pd
import numpy as np
from Course import Course
from CSPExams import CSPExams
import datetime

COURSE_DATABASE = "Courses_Data.csv"
COURSE_ATTRIBUTES = ['name', 'number', 'faculties', 'type', 'credits', 'attempt']


def make_variables():
    course_data = pd.read_csv(COURSE_DATABASE)

    courses_list = list()
    for index in course_data.index:
        courses_list.append(Course(course_data[COURSE_ATTRIBUTES[0]][index] + ' - A',
                                   course_data[COURSE_ATTRIBUTES[1]][index],
                                   course_data[COURSE_ATTRIBUTES[2]][index],
                                   course_data[COURSE_ATTRIBUTES[3]][index],
                                   course_data[COURSE_ATTRIBUTES[4]][index],
                                   1))

        courses_list.append(Course(course_data[COURSE_ATTRIBUTES[0]][index] + ' - B',
                                   course_data[COURSE_ATTRIBUTES[1]][index],
                                   course_data[COURSE_ATTRIBUTES[2]][index],
                                   course_data[COURSE_ATTRIBUTES[3]][index],
                                   course_data[COURSE_ATTRIBUTES[4]][index],
                                   2))
    return courses_list


def make_domain(start_date, end_date):
    #todo: if time premits - maybe import google calender?
    #todo: add hagi israel and

    # 1/7/2022 - 10/8/2022

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
        if d1.weekday() == 5:
            d1 = d1 + datetime.timedelta(days=1)
            continue
        number_to_real_date_dict[number + 0.1] = d1
        domain.append(number + 0.1)

        if d1.weekday() != 4:
            number_to_real_date_dict[number + 0.2] = d1
            number_to_real_date_dict[number + 0.3] = d1
            domain.append(number + 0.2)
            domain.append(number + 0.3)
        d1 = d1 + datetime.timedelta(days=1)
    return domain, number_to_real_date_dict


if __name__ == '__main__':
    variables = make_variables()
    domain, number_to_real_date_dict = make_domain('2024/01/15', '2024/01/28')
    CSP_Exam = CSPExams(variables, domain)
    CSP_Exam.create_constraints()
    result = CSP_Exam.backtracking_search()
    print(result)

