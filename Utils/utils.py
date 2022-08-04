import uuid
from datetime import timedelta
from googleapiclient.discovery import build
import pickle
from Utils.Course import Course
from Utils.Constants import *
from InformedSearchAlgorithms.Hall import Hall
import pandas as pd
import datetime
import numpy as np


# Google Calendar functions


def export_to_calendar(courses_list, complex):
	credentials = pickle.load(open("Utils/token.pkl", "rb"))
	service = build("calendar", "v3", credentials=credentials)
	result = service.calendarList().list().execute()
	calendar_id = result["items"][0]['id']
	for course in courses_list:
		exam_event = create_event(course, complex)
		service.events().insert(calendarId=calendar_id, body=exam_event).execute()
	save_decision = input(DECISION_MESSAGE)
	if save_decision != 'y':
		print(DELETE_MESSAGE)
		for course in courses_list:
			service.events().delete(calendarId=calendar_id, eventId=course.get_exam_id()).execute()
	return


def create_event(course, complex):
	start_time = course.get_exam_time()
	end_time = start_time + timedelta(hours=3)
	course.set_exam_id("".join(str(uuid.uuid4()).split("-")))
	course_list = ",".join(course.get_halls_assigned()) if complex == 'y' else ''
	return {
		'summary': course.get_name(),
		'id': course.get_exam_id(),
		'location': course_list,
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


#######################################################################

# ISA solver functions


def get_courses(given_data):
	courses = list()
	for moed in [(MOED_A, 'A'), (MOED_B, 'B')]:
		for index in given_data.index:
			courses.append(Course(given_data[COURSE_ATTRIBUTES[0]][index] + f' - {moed[1]}',
								  given_data[COURSE_ATTRIBUTES[1]][index],
								  given_data[COURSE_ATTRIBUTES[2]][index],
								  given_data[COURSE_ATTRIBUTES[3]][index],
								  given_data[COURSE_ATTRIBUTES[4]][index],
								  given_data[COURSE_ATTRIBUTES[5]][index],
								  moed[0]))
	return courses


def get_halls(given_data):
	halls = list()
	for index in given_data.index:
		halls.append(Hall(given_data[CLASSROOMS_ATTRIBUTES[0]][index],
						  given_data[CLASSROOMS_ATTRIBUTES[1]][index],
						  given_data[CLASSROOMS_ATTRIBUTES[2]][index],
						  given_data[CLASSROOMS_ATTRIBUTES[3]][index],
						  given_data[CLASSROOMS_ATTRIBUTES[4]][index]))
	return halls


#######################################################################

# General functions


def make_variables(change_periods_date, n_courses=None):
	if n_courses is not None:
		course_data = pd.read_csv(PURE_CONSTRAINT_COURSE_DATABASE).iloc[:n_courses, :]
	else:
		course_data = pd.read_csv(PURE_CONSTRAINT_COURSE_DATABASE)

	courses = list()
	for moed in [(MOED_A, 'A'), (MOED_B, 'B')]:
		for index in course_data.index:
			courses.append(Course(course_data[COURSE_ATTRIBUTES[0]][index] + f' - {moed[1]}',
								  course_data[COURSE_ATTRIBUTES[1]][index],
								  course_data[COURSE_ATTRIBUTES[2]][index],
								  course_data[COURSE_ATTRIBUTES[3]][index],
								  course_data[COURSE_ATTRIBUTES[4]][index],
								  course_data[COURSE_ATTRIBUTES[5]][index],
								  moed[0],
								  change_periods_date))
	return courses


def make_domain(start_date, end_date):
	# dates in string format
	start_date = start_date
	end_date = end_date

	# convert string to date object
	d1 = datetime.datetime.strptime(start_date, "%Y/%m/%d")
	d2 = datetime.datetime.strptime(end_date, "%Y/%m/%d")
	# difference between dates in timedelta
	delta = d2 - d1

	number_to_real_date_dict = dict()
	# domain = [0]
	domain = list()
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

#######################################################################

def update_dict(key, value, dict):
	if key not in dict.keys():
		dict[key] = [value]
	else:
		dict[key].append(value)


def add_list_to_dict(key, list, dict):
	if key not in dict.keys():
		dict[key] = list.copy()
	else:
		dict[key] += list