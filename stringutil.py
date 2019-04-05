import base64
from html2bbcode.parser import HTML2BBCode
from unicodedata import normalize

def to_bbcode(html_text):
	parser = HTML2BBCode()
	html_text = html_text.replace('<br>', '') # remove line break
	bbcode = str(parser.feed(html_text))
	bbcode = normalize('NFKC', bbcode) # normalize '\xa0'
	return bbcode

def to_base64(object):
	return base64.b64encode(bytes(str(object), 'utf-8'))

def print_b64(object):
	print(to_base64(object))

def trim(string):
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