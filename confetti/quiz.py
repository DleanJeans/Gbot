import re
from functools import partial
from itertools import groupby

QUOTE = '"'

def process(text):
	text = text.replace('”', QUOTE)
	text = text.replace('\n\n', '\n')
	text = text.rsplit('\n', 3)
	text[1:] = [a.strip() for a in text[1:]]
	text[1:] = map(separate_letter_digit, text[1:])
	text[1:] = map(lambda x: str.lstrip(x, '.'), text[1:])
	text[0] = text[0].replace('\n', ' ') # one-linize quiz
	return text

def separate_letter_digit(text):
	words = [''.join(w) for _, w in groupby(text, str.isdigit)]
	text = ' '.join([w.strip() for w in words])
	return text

def is_valid(text):
	return True