import uuid
from datetime import datetime, timedelta
from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

import pandas as pd
from main import make_domain
from simulated_annealing_solver import SimulatedAnnealingSolver
from Course import *
from Constants import *


def get_courses(given_data):
    courses = list()
    for moed in [(MOED_A, 'A'), (MOED_B, 'B')]:
        for index in given_data.index:
            courses.append(Course(given_data[COURSE_ATTRIBUTES[0]][index] + f' - {moed[1]}',
                                  given_data[COURSE_ATTRIBUTES[1]][index],
                                  given_data[COURSE_ATTRIBUTES[2]][index],
                                  given_data[COURSE_ATTRIBUTES[3]][index],
                                  given_data[COURSE_ATTRIBUTES[4]][index],
                                  moed[0]))
    return courses


def preprocess_courses(courses_list, times_list):
    n_courses = len(courses_list)
    n_times = len(times_list)
    courses_to_rows_dict = dict()
    times_to_cols_dict = dict()
    reverse_times_to_cols_dict = dict()
    for course_index, course in enumerate(courses_list):
        courses_to_rows_dict[course] = course_index
    for time_index, time in enumerate(times_list):
        times_to_cols_dict[time] = time_index
        reverse_times_to_cols_dict[time_index] = time
    return n_courses, n_times, courses_to_rows_dict, times_to_cols_dict, reverse_times_to_cols_dict


def cooling_function(temp, alpha, t):
    return temp*(alpha**t)


def update_course_data(courses_dict, result_assignment_dict, reverse_time_dict, dates_dict, hours):
    for course, course_ind in courses_dict.items():
        repr_time = reverse_time_dict[result_assignment_dict[course_ind]]
        real_date = dates_dict[repr_time]
        year = real_date.year
        month = real_date.month
        day = real_date.day
        repr_time = round(repr_time - int(repr_time), 1)
        course.set_exam_time(datetime(year, month, day, hours[repr_time][0], hours[repr_time][1], 0))


def export_to_calendar(courses_list):
    credentials = pickle.load(open("token.pkl", "rb"))
    service = build("calendar", "v3", credentials=credentials)
    result = service.calendarList().list().execute()
    calendar_id = result["items"][0]['id']
    for course in courses_list:
        exam_event = create_event(course)
        service.events().insert(calendarId=calendar_id, body=exam_event).execute()
    save_decision = input(DECISION_MESSAGE)
    if save_decision != 'y':
        print(DELETE_MESSAGE)
        for course in courses_list:
            service.events().delete(calendarId=calendar_id, eventId=course.get_exam_id()).execute()
    return


def create_event(course):
    start_time = course.get_exam_time()
    end_time = start_time + timedelta(hours=3)
    course.set_exam_id("".join(str(uuid.uuid4()).split("-")))
    return {
        'summary': course.get_name(),
        'id': course.get_exam_id(),
        'location': 'A100',
        'colorId': str(course.get_number())[0],
        'description': 'Exam',
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': TIMEZONE,
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': TIMEZONE,
        },
    }


if __name__ == '__main__':
    data = pd.read_csv(COURSE_DATABASE2).iloc[:3, :]
    courses = get_courses(data)
    representative_times, number_to_real_date_dict = make_domain('2022/01/15', '2022/03/08')
    n_courses, n_times, courses_to_rows_dict, times_to_cols_dict, reverse_times_to_cols_dict = preprocess_courses(
        courses, representative_times)
    hours_dict = {MORNING_EXAM: (9, 0), NOON_EXAM: (13, 30), EVENING_EXAM: (17, 0)}
    solver = SimulatedAnnealingSolver(n_courses, n_times, courses_to_rows_dict, times_to_cols_dict,
                                      reverse_times_to_cols_dict, None, number_to_real_date_dict,
                                      0.85, cooling_function)
    solver.solve()
    print(solver.get_state())
    update_course_data(courses_to_rows_dict, solver.get_state().assignment_dict, reverse_times_to_cols_dict,
                       number_to_real_date_dict, hours_dict)
    solver.check_solution_quality()
    # scopes = ["https://www.googleapis.com/auth/calendar"]
    # flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
    # credentials = flow.run_console()
    # pickle.dump(credentials, open("token.pkl", "wb"))
    # credentials = pickle.load(open("token.pkl", "rb"))
    # service = build("calendar", "v3", credentials=credentials)
    # result = service.calendarList().list().execute()
    # calendar_id = result["items"][0]['id']
    export_to_calendar(courses)
    # scopes = ["https://www.googleapis.com/auth/calendar"]
    # flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
    # flow.run_console()
