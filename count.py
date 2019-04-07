from itertools import tee

NEWLINE = '\n'

def exact(text, answers):
	points = [text.count(a) for a in answers]
	if sum(points) == 0:
		points = [text.lower().count(a.lower()) for a in answers]
	return points

def splitted(text, answers):
	answers = trim_common_words(answers)
	print('Trimmed:', NEWLINE, NEWLINE.join(answers), NEWLINE, sep='')

	counts = []
	splitted_text = text.split()

	for a in answers:
		count = max([splitted_text.count(word) for word in a.split()])
		counts.append(count)
	
	return counts

def trim_common_words(answers):
	trimmed = answers[:]
	for i in range(len(answers) - 1):
		a = answers[i]
		b = answers[i+1]

		common = list(set(a.split()) & set(b.split()))
		for c in common:
			a = a.replace(c, '')
			b = b.replace(c, '')
		
		trimmed[i] = a.strip()
		trimmed[i + 1] = b.strip()
	return trimmed