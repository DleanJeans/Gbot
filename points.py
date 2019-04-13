import re
from underthesea import pos_tag

from colorama import Back, Fore

EXACT = 'Exact'
SPLIT = 'Split'

best_color = Back.YELLOW

lang = None

def same_best_answer(name_to_points):
	exact_max_index = max_indices(name_to_points[EXACT])
	split_max_index = max_indices(name_to_points[SPLIT])

	return exact_max_index == split_max_index

def color_best(name_to_points):
	for name, points in name_to_points.items():
		indices = max_indices(points)
		for i in indices:
			name_to_points[name][i] = best_color + Fore.BLACK + str(points[i]) + Back.RESET + Fore.RESET
	return name_to_points

def max_indices(points):
	indices = [i for i, p in enumerate(points) if p == max(points)]
	if len(indices) == 3:
		indices = []
	return indices

def negate_if_negative(q, name_to_points):
	if lang and lang.is_negative(q):
		name_to_points = {name:[-n for n in points] for name, points in name_to_points.items()}
	return name_to_points