import numpy as np
import pandas as pd
from termcolor import colored

NO = 'n'

YES = 'y'

QUESTION_COLOR = 'blue'
DATA_HEB_CSV = "ID3/exam_data_heb.csv"

ANSWER_COLOR = 'cyan'

NEGATIVE_ANSWER_MSG = "you shouldn't take the moed b exam"

POSITIVE_ANSWER_MSG = "you should take the moed b exam"

UNRECOGNIZED_ANSWER_MSG = "looks like you are the first one to face this condition \nwe'll be happy if you'll help us expand our " \
		  "data and fill this form to let us know what you have chossen\n" \
		  "https://docs.google.com/forms/d/e/1FAIpQLSfDaM7w2vvG9KHpyixrz2HfPhZx_0nO1T5RpRPNC-H2UQtFAg/viewform?usp=sf_link"

eps = np.finfo(float).eps
ATTRIBUTE_TO_QUESTION_DICT = {'did fail': "have you failed the exam? (yes, no)\n",
							  'exam grade': "what is your exam grade? (54-, 55-69, 70-79, 80-89, 90-100)\n",
							  'final grade': "what is your final grade? (59-, 60-69, 70-79, 80-89, 90-100)\n",
							  'did moed b before': "have you done moed b before? (yes, no)\n",
							  'improve moed b before': "have you improved your grade in moed b before? (yes, no)\n",
							  'confident in improvement': "are you confident that you can improve the exam score?"
														  "(yes, no, don't know)\n",
							  'time to study': "how much time do you have to study? (1,2,3,4,5,6,7+)\n",
							  'exam difficulty': "what is the exam difficulty? (easy, medium, hard, very hard)\n",
							  'exam type 1': "what is the type of the exam? (open, close, both)\n",
							  'exam type 2': "how do you take the exam? (comp, write)\n",
							  'factor in moed a': "did you have factor in moed a? (yes, no)\n",
							  'harder then moed a': "is moed-b usually more difficult then moed-a?(yes, no, don't know)\n"
							  }


def hebrew_to_english_database(data_file):
	df = pd.read_csv(data_file)
	df = df.iloc[:, 1:].reset_index(drop=True)
	english_keys_list = list(ATTRIBUTE_TO_QUESTION_DICT.keys())
	english_keys_list.append('decision')
	hebrew_to_english_keys = {df.keys()[i]: english_keys_list[i] for i in range(len(english_keys_list))}
	df = df.rename(columns=hebrew_to_english_keys)
	df[english_keys_list[0]] = np.where(df[english_keys_list[0]] == "לא", "no", "yes")

	df[english_keys_list[1]] = np.where(df[english_keys_list[1]] == "פחות מ 55", "54-", df[english_keys_list[1]])

	df[english_keys_list[2]] = np.where(df[english_keys_list[2]] == "פחות מ 60", "59-", df[english_keys_list[2]])

	df[english_keys_list[3]] = np.where(df[english_keys_list[3]] == "לא", "no", "yes")

	df[english_keys_list[4]] = np.where(df[english_keys_list[4]] == "לא", "no", "yes")

	df[english_keys_list[5]][df[english_keys_list[5]] == "כן"] = "yes"
	df[english_keys_list[5]][df[english_keys_list[5]] == "לא"] = "no"
	df[english_keys_list[5]][df[english_keys_list[5]] == "אולי"] = "don't know"

	df[english_keys_list[7]][df[english_keys_list[7]] == "קל"] = "easy"
	df[english_keys_list[7]][df[english_keys_list[7]] == "בינוני"] = "medium"
	df[english_keys_list[7]][df[english_keys_list[7]] == "קשה"] = "hard"
	df[english_keys_list[7]][df[english_keys_list[7]] == "קשה מאוד"] = "very hard"

	df[english_keys_list[8]][df[english_keys_list[8]] == "פתוח"] = "open"
	df[english_keys_list[8]][df[english_keys_list[8]] == "אמריקאי"] = "close"
	df[english_keys_list[8]][df[english_keys_list[8]] == "שילוב של השניים"] = "both"

	df[english_keys_list[9]] = np.where(df[english_keys_list[9]] == "ידנית", "write", "comp")

	df[english_keys_list[10]] = np.where(df[english_keys_list[10]] == "לא", "no", "yes")

	df[english_keys_list[11]][df[english_keys_list[11]] == "כן"] = "yes"
	df[english_keys_list[11]][df[english_keys_list[11]] == "לא"] = "no"
	df[english_keys_list[11]][df[english_keys_list[11]] == "לא יודע/ת"] = "don't know"

	df[english_keys_list[12]] = np.where(df[english_keys_list[12]] == "לא", "n", "y")

	return df


def find_entropy(df):
	decision = df.keys()[-1]
	entropy = 0
	values = df[decision].unique()
	for value in values:
		fraction = df[decision].value_counts()[value] / len(df[decision])
		entropy += -fraction * np.log2(fraction)
	return entropy


def find_entropy_attribute(df, attribute):
	decision = df.keys()[-1]
	target_variables = df[decision].unique()
	variables = df[attribute].unique()
	total_entropy = 0
	den = 0
	for variable in variables:
		entropy = 0
		for target_variable in target_variables:
			num = len(df[attribute][df[attribute] == variable][df[decision] == target_variable])
			den = len(df[attribute][df[attribute] == variable])
			fraction = num / (den + eps)
			entropy += -fraction * np.log2(fraction + eps)
		fraction2 = den / len(df)
		total_entropy += -fraction2 * entropy
	return abs(total_entropy)


def find_winner(df):
	information_gain = []
	for key in df.keys()[:-1]:
		information_gain.append(find_entropy(df) - find_entropy_attribute(df, key))
	return df.keys()[:-1][np.argmax(information_gain)]


def get_sub_dataframe(df, node, value):
	return df[df[node] == value].reset_index(drop=True)


def build_tree(df, tree=None):
	decision = df.keys()[-1]
	node = find_winner(df)
	attValue = np.unique(df[node])

	if tree is None:
		tree = {}
		tree[node] = {}

	for value in attValue:
		sub_dataframe = get_sub_dataframe(df, node, value)
		unique_values, counts = np.unique(sub_dataframe[decision], return_counts=True)
		if len(counts) == 1:
			tree[node][value] = unique_values[0]
		else:
			tree[node][value] = build_tree(sub_dataframe)

	return tree


def tree_print(tree, add_str=""):
	for key, value in tree.items():
		print(f"{add_str} {key}")
		if value in [YES, NO]:
			print(f"{add_str}\t->{value}")
		else:
			tree_print(value, add_str + "\t")


def predict(tree):
	if tree in [YES, NO]:
		return tree
	ind = list(tree.keys())[0]
	ans = input(colored(ATTRIBUTE_TO_QUESTION_DICT[ind], QUESTION_COLOR, attrs=['bold']))
	if ans not in tree[ind].keys():
		return -1
	return predict(tree[ind][ans])


if __name__ == "__main__":
	df = hebrew_to_english_database(DATA_HEB_CSV)
	tree = build_tree(df)
	result = predict(tree)
	if result == -1:
		print(UNRECOGNIZED_ANSWER_MSG)
	elif result == YES:
		print(colored(POSITIVE_ANSWER_MSG, ANSWER_COLOR))

	else:
		print(colored(NEGATIVE_ANSWER_MSG, ANSWER_COLOR))
