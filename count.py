from itertools import tee
from lprint import print

NEWLINE = '\n'
lang = None

def exact(text, answers):
	points = [text.count(a) for a in answers]
	if sum(points) == 0:
		points = [text.lower().count(a.lower()) for a in answers]
	return points

def splitted(text, answers):
	if lang:
		answers = lang.trim_answers(answers)
	print('Trimmed:', NEWLINE, NEWLINE.join(answers), NEWLINE, sep='')

	counts = []
	splitted_text = text.split()

	for a in answers:
		count = max([splitted_text.count(word) for word in a.split()])
		counts.append(count)
	
	return counts