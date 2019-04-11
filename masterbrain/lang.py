import nltk

'''
https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk
'''
trimmable = ['DT', 'IN']

class LangTool:
	def __init__(self):
		self.stemmer = nltk.PorterStemmer()

	def is_negative(self, q):
		return q.count('NOT') >= 1
	
	def trim_answers(self, answers):
		trimmed = []
		for a in answers:
			trimmed.append(self.trim(a))
		return trimmed

	def trim(self, phrase):
		tags = nltk.pos_tag(phrase.split())
		tags = [t for t in tags if t[1] not in trimmable]
		phrase = ' '.join([t[0] for t in tags])
		return phrase