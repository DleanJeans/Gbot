import nltk

'''
https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk
'''
trimmable = ['DT', 'IN']
negatives = ['NOT', 'n\'t']

stemmer = nltk.PorterStemmer()

def is_negative(q):
	return sum([q.count(n) for n in negatives]) >= 1

def trim_answers(answers):
	trimmed = []
	for a in answers:
		trimmed.append(trim(a))
	return trimmed

def trim(phrase):
	tags = nltk.pos_tag(phrase.split())
	tags = [t for t in tags if t[1] not in trimmable]
	phrase = ' '.join([t[0] for t in tags])
	return phrase