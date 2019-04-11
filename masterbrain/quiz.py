QUOTE = '"'

class QuizTool:
	def process(self, text):
		text = text.replace('\n\n', '\n')
		text = text.lstrip('0123456789. ')
		text = text.replace('”', QUOTE)
		text = text.replace(' / ', '/')
		text = text.rsplit('\n', 3)
		text[1:] = [a.strip() for a in text[1:]]
		text[0] = text[0].replace('\n', ' ') # one-linize quiz
		return text