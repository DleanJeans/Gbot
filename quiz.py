import json
import re
from functools import partial

letter_digit_sep = r'([0-9]+(\.[0-9]+)?)'
sep_letter_digit = partial(re.sub, letter_digit_sep, r' \1 ')

def process(text):
	text = text.replace('\n\n', '\n')
	text = text.rsplit('\n', 3)
	# text[1:] = map(trim_non_alnum, text[1:])
	text[1:] = map(sep_letter_digit, text[1:])
	text[1:] = [a.strip() for a in text[1:]]
	text[0] = text[0].replace('\n', ' ') # one-linize quiz
	return text

def trim_non_alnum(string):
	for char in string:
		if char.isalnum():
			break
		else:
			string = string[1:]
	
	for char in reversed(string):
		if char.isalnum():
			break
		else:
			string = string[:-1]

	return string