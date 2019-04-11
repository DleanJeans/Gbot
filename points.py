import re
from underthesea import pos_tag

from colorama import Back, Fore

EXACT = 'Exact'
SPLIT = 'Split'

best_color = Back.YELLOW

lang = None

def same_best_answer(points_dict):
	exact_max_index = max_indices(points_dict[EXACT])
	split_max_index = max_indices(points_dict[SPLIT])

	return exact_max_index == split_max_index

def color_best(points_dict):
	for name, points in points_dict.items():
		indices = max_indices(points)
		for i in indices:
			points_dict[name][i] = best_color + Fore.BLACK + str(points[i]) + Back.RESET + Fore.RESET
	return points_dict

def max_indices(points):
	indices = [i for i, p in enumerate(points) if p == max(points)]
	if len(indices) == 3:
		indices = []
	return indices

def negate_if_negative(q, points_dict):
	if lang and lang.is_negative(q):
		points_dict = {name:[-n for n in points] for name, points in points_dict.items()}
	return points_dict