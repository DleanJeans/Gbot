import re
from functools import partial

QUOTE = '"'

letter_digit_sep = r'([0-9]+(\.[0-9]+)?)'
sep_letter_digit = partial(re.sub, letter_digit_sep, r' \1 ')

def process(text):
	text = text.replace('”', QUOTE)
	text = text.replace('\n\n', '\n')
	text = sep_letter_digit(text)
	text = text.replace(' / ', '/')
	text = text.rsplit('\n', 3)
	text[1:] = [a.strip() for a in text[1:]]
	text[0] = text[0].replace('\n', ' ') # one-linize quiz
	return text