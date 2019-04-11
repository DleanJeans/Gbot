import re
from underthesea import pos_tag

QUOTE_REGEX = r'"([^"]*)"'
NEGATIVE = ('không', 'R')
QUOTE = '"'

class LangTool:
	def is_negative(self, q):
		negative_word_exists = NEGATIVE in pos_tag(q.lower())
		quoted_texts =re.findall(QUOTE_REGEX, q)
		negative_in_quotes = any([NEGATIVE[0] in text for text in quoted_texts])

		return negative_word_exists and not negative_in_quotes
	
	def trim_answers(self, answers):
		trimmed = answers[:]
		for i in range(len(answers) - 1):
			a = answers[i]
			b = answers[i+1]

			common = list(set(a.split()) & set(b.split()))
			for c in common[::-1]:
				test_a = a.replace(c, '').strip()
				test_b = b.replace(c, '').strip()
				if test_a != '':
					a = test_a
				if test_b != '':
					b = test_b
			
			trimmed[i] = a
			trimmed[i + 1] = b
		return trimmed