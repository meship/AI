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


def check_solution_quality(state, export_to_graph=False):
	to_print = "Results: \n"
	# to_print += f"Duplicate status: {self.best_child.check_duplicates()}")
	to_print += f"Difference status: \n"
	diff_results = state.check_exams_diff()
	for pair, diff in diff_results.items():
		to_print += f"({pair[0]}, {pair[1]}): {diff}\n"
	to_print += f"Number of Friday exams: {state.exam_on_friday_constraint()}\n"
	to_print += f"Number of Sunday morning exams: {state.exam_on_sunday_morning_constraint()}\n"
	to_print += f"Number of evening exams: {state.exam_on_evening_constraint()}\n"
	to_print += f"Number of Math NOT morning exams: {state.math_exam_on_morning_constraint()}\n"

	if export_to_graph:
		return diff_results, state.exam_on_evening_constraint()
	else:
		print(to_print)


def check_halls_solution_quality(state, export_to_graph=False):
	to_print = "Results: \n"
	to_print += "Number of unfair assignments with different chair types: \n"
	course_to_unfair_assignment = dict()
	num_of_unfair_courses = 0
	for course, halls in state.halls_assignment_dict.items():
		r, s = 0, 0
		for hall_ind in halls:
			if state.reverse_halls_dict[hall_ind].get_chair_type() == "s":
				s += 1
			# s += self.best_child.reverse_halls_dict[hall_ind].get_capacity()
			elif state.reverse_halls_dict[hall_ind].get_chair_type() == "r":
				r += 1
			# r += self.best_child.reverse_halls_dict[hall_ind].get_capacity()
			else:
				break
		else:
			unfair_assignment = min(r, s)
			if unfair_assignment:
				to_print += f"{state.reverse_courses_dict[course]}: student: {s}, regular: {r}\n"
				course_to_unfair_assignment[state.reverse_courses_dict[course]] = (s, r)
				num_of_unfair_courses += 1

	total_halls_assigned = 0
	student_chair_halls = 0
	for course, halls in state.halls_assignment_dict.items():
		total_halls_assigned += len(halls)
		for hall_ind in halls:
			# total_halls_assigned += self.best_child.reverse_halls_dict[hall_ind].get_capacity()
			if state.reverse_halls_dict[hall_ind].get_chair_type() == "s":
				student_chair_halls += 1
			# student_chair_halls += self.best_child.reverse_halls_dict[hall_ind].get_capacity()
	to_print += f"\nNumber of halls with student chairs assigned {student_chair_halls} out " \
				f"of {total_halls_assigned} halls\n"
	to_print += f"\nRatio number between halls capacity assigned and exam number of students: \n"

	for course, halls, in state.halls_assignment_dict.items():
		capacity = sum([state.reverse_halls_dict[hall].get_capacity() for hall in halls])
		ratio = capacity / state.reverse_courses_dict[course].get_n_students()
		if ratio > SQUEEZE_RATIO:
			to_print += f"{state.reverse_courses_dict[course]}: {ratio}\n"
	to_print += "\nAreas of each course assigned: \n"
	course_to_areas_dict = dict()
	for course, halls in state.halls_assignment_dict.items():
		course_obj = state.reverse_courses_dict[course]
		course_to_areas_dict[course_obj] = [state.reverse_halls_dict[hall].get_area() for hall in halls]
		to_print += f"{course_obj}: {course_to_areas_dict[course_obj]}\n"

	if export_to_graph:
		return course_to_unfair_assignment, num_of_unfair_courses, student_chair_halls, total_halls_assigned, \
			   course_to_areas_dict
	else:
		print(to_print)


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