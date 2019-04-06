import re
from underthesea import pos_tag

from colorama import Back, Fore

quote_regex = r'"([^"]*)"'

EXACT = 'Exact'
SPLIT = 'Split'
QUOTE = '@'

def same_best_answer(points_dict):
	exact_max_index = max_index(points_dict[EXACT])
	split_max_index = max_index(points_dict[SPLIT])

	return exact_max_index == split_max_index

def max_index(points):
	return points.index(max(points))

def color_best(points_dict):
	for name, points in points_dict.items():
		indices = max_indices(points)
		for i in indices:
			points_dict[name][i] = Back.GREEN + Fore.BLACK + str(points[i]) + Back.RESET + Fore.RESET
	return points_dict

def max_indices(points):
	indices = [i for i, p in enumerate(points) if p == max(points)]
	if len(indices) == 3:
		indices = []
	return indices

NEGATIVE = ('không', 'R')

def negate_if_negative(q, points_dict):
	negative_exists = NEGATIVE in pos_tag(q.lower())
	has_quotes = q.count(QUOTE) >= 2
	quoted_texts = re.findall(quote_regex, q)
	negative_in_quotes = any([NEGATIVE[0] in text for text in quoted_texts])

	if negative_exists and not negative_in_quotes:
		points_dict = {name:[-n for n in points] for name, points in points_dict.items()}
	return points_dict