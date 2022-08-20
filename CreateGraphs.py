from plotly.subplots import make_subplots

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


def course_to_number(course):
	if course.get_attempt() == MOED_A:
		return str(course.get_number()) + '-A'
	else:
		return str(course.get_number()) + '-B'


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
		data=[go.Scatter(x=np.arange(len(average_course_values)), y=average_course_values, mode='markers + lines',
						 marker=dict(color='mediumorchid'),
						 line=dict(color='mediumorchid'), name="average value"),
			  go.Scatter(x=np.arange(len(best_course_values)), y=best_course_values, mode='markers + lines',
						 marker=dict(color='Navy'),
						 line=dict(color='Navy'), name="best value")],
		layout=go.Layout(title=f"GA Average and Best as a Function of Gen Number in courses",
						 xaxis=dict(title=r"generation number"),
						 yaxis=dict(title=r"fitness value")))
	fig.show()

	diff_dict, evening_exams = solver.check_solution_quality(True)

	# traces = {}
	# for courses, difference in diff_dict.items():
	#     traces[f"{courses[0]}, {courses[1]}"] = go.Box(name=f"{courses[0]}, {courses[1]}", y=[difference],
	#                                     boxpoints='all',
	#                                     pointpos=0,
	#                                     marker=dict(color='rgb(84, 173, 39)'),
	#                                     line=dict(color='rgba(0,0,0,0)'),
	#                                     fillcolor='rgba(0,0,0,0)',
	#                                     showlegend=False)
	# # convert data to form required by plotly
	# data = list(traces.values())
	# fig = go.Figure(data)
	# fig.show()
	diff_dict = dict(sorted(diff_dict.items(), key=lambda item: item[1]))
	x_val = [course_to_number(key[0]) + ", " + course_to_number(key[1]) for key in diff_dict.keys()]
	fig = go.Figure([go.Bar(x=list(diff_dict.values()), y=x_val, orientation='h')],
					layout=go.Layout(title=f"Deviation Form Desired Deference Between Two Courses ",
									 xaxis=dict(title=r"Deviation form difference"),
									 yaxis=dict(title=r"pairs of courses")))
	fig.show()

	fig = px.pie(values=[evening_exams, (n_courses - evening_exams)],
				 names=['evening exams', 'not evening exams'],
				 title=f"Number of Evening Exams", color_discrete_sequence=px.colors.qualitative.Pastel1[1:3])
	fig.show()

	fig = go.Figure(
		data=[go.Scatter(x=np.arange(len(average_halls_values)), y=average_halls_values, mode='markers + lines',
						 marker=dict(color='mediumorchid'),
						 line=dict(color='mediumorchid'), name="average value"),
			  go.Scatter(x=np.arange(len(best_halls_values)), y=best_halls_values, mode='markers + lines',
						 marker=dict(color='navy'),
						 line=dict(color='navy'), name="best value"
						 )],
		layout=go.Layout(title=f"GA Average and Best as a Function of Gen Number in halls",
						 xaxis=dict(title=r"generation number"),
						 yaxis=dict(title=r"fitness value")))
	fig.show()

	course_to_unfair_assignment, num_of_unfair_courses, student_chair_halls, n_halls, course_to_areas_dict = \
		complex_solver.check_hall_solution_quality(True)

	# for course, unfair_assignment in course_to_unfair_assignment.items():
	# 	fig = px.pie(values=list(unfair_assignment), names=['students_chairs', 'regulars_chairs'],
	# 				 title=f"{course}")
	# 	fig.show()

	course_to_unfair_assignment = dict(sorted(course_to_unfair_assignment.items(), key=lambda item: item[1][1]))
	courses = [course_to_number(course) for course in course_to_unfair_assignment.keys()]
	student = [val[0] for val in course_to_unfair_assignment.values()]
	regular = [val[1] for val in course_to_unfair_assignment.values()]
	capacity_title = f"Capacity of Halls with Students Chairs vs Capacity of Halls with Regular Chairs in Unfair Exams"
	number_title = f"Number of Halls with Students Chairs"
	fig = go.Figure(data=[
		go.Bar(name='students chairs', x=student, y=courses, orientation='h', marker_color='mediumseagreen'),
		go.Bar(name='regular chairs', x=regular, y=courses, orientation='h', marker_color='crimson'),
	], layout=go.Layout(title=number_title,
						xaxis=dict(title=r"halls count"),
						yaxis=dict(title=r"course")))
	# Change the bar mode
	fig.update_layout(barmode='group')
	fig.show()

	fig = px.pie(values=[num_of_unfair_courses, (n_courses - num_of_unfair_courses)],
				 names=['students chairs', 'regulars chairs'],
				 title=f"Number of Unfair Exams", color_discrete_sequence=px.colors.qualitative.Pastel1[1:3])
	fig.show()
	#todo chage the title
	fig = px.pie(values=[student_chair_halls, (n_halls - student_chair_halls)],
				 names=['students chairs halls capacity', 'regulars chairs halls capacity'],
				 title=f"Capacity of Halls with Students Chairs",
				 color_discrete_sequence=px.colors.qualitative.Pastel1[1:3])
	fig.show()

	traces = {}
	for course, areas in course_to_areas_dict.items():
		traces[course] = go.Box(name=course_to_number(course), y=areas,
								boxpoints='all',
								pointpos=0,
								marker=dict(color='MediumAquamarine'),
								line=dict(color='rgba(0,0,0,0)'),
								fillcolor='rgba(0,0,0,0)',
								showlegend=False)
	# convert data to form required by plotly
	data = list(traces.values())

	# build figure
	fig = go.Figure(data, layout=go.Layout(title=f"Distance Between Halls that were Assigned to a Certain Exam",
										   xaxis=dict(title=r"exam"),
										   yaxis=dict(title=r"halls area")))
	fig.show()


def create_sa_graphs(algorithm, course_num=None):
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
			 reverse_times_to_cols_dict, number_to_real_date_dict, hours_dict, courses, algorithm, record_progress)
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
		create_ga_graphs()
	elif sys.argv[1] in [SIMULATED_ANNEALING, GRADIENT_DESCENT]:
		create_sa_graphs(sys.argv[1])
