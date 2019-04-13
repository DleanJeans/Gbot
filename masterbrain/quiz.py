QUOTE = '"'

def process(text):
	text = text.replace('\n\n', '\n')
	text = text.lstrip('0123456789. \n')
	text = text.replace('”', QUOTE)
	text = text.replace(' / ', '/')
	text = text.rsplit('\n', 3)
	text[1:] = [a.strip() for a in text[1:]]
	text[0] = text[0].replace('\n', ' ') # one-linize quiz
	return text

def is_valid(text):
	return text.count('\n') >= 3