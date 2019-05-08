import colorama
import re
import browser
import requests
import os

from colorama import Style, Back, Fore
from urllib.parse import quote
from bs4 import BeautifulSoup
from googletrans import Translator
from underthesea import ner
from lprint import print

GOOGLE = 'https://www.google.com/search?q='
GOOGLE_IMAGE = 'https://www.google.com/search?tbm=isch&q='
GOOGLE_REVERSE_IMAGE = 'http://www.google.com/searchbyimage/upload'
TEMP_PATH = os.path.dirname(__file__).replace('\\', '/') + '/gg-temp.png'

H3 = 'h3'
SPAN = 'span'

CLASS_TITLE = 'LC20lb'
CLASS_SNIPPET = 'st'

NEWLINE = '\n'
QUOTE = '"'

COLORAMA_TAGS = [Back.BLUE, Back.RED, Back.RESET, Style.BRIGHT, Style.NORMAL]

titles_visible = True

title_color = Back.BLUE
answer_color = Fore.BLACK + Back.YELLOW

def start(num_browsers):
	global browser, translator

	print('Opening Firefox...')
	browser.start(num_browsers)
	colorama.init()
	translator = Translator()
	print('Done!')

def is_eng(a):
	return translator.detect(a).lang != 'vi'

def translate(q):
	return translator.translate(q, src='vi', dest='en').text

saved_plain = ''
saved_formatted = ''

def reverse_search_image(image):
	global saved_plain, saved_formatted

	image.save(TEMP_PATH)
	multipart = {'encoded_image': (TEMP_PATH, open(TEMP_PATH, 'rb')), 'image_content': ''}
	
	response = requests.post(GOOGLE_REVERSE_IMAGE, files=multipart, allow_redirects=False)
	url = response.headers['Location']

	browser.open_url(url)

	saved_plain, saved_formatted = extract_results(None)

def get_saved():
	return saved_plain, saved_formatted

def search_image(q, driver=-1):
	url = GOOGLE_IMAGE + quote(q)
	browser.open_url(url, driver)

def search(get_q, answers, driver=-1):
	q = get_q()
	q = q.replace(QUOTE, ' ')
	print('Google:', Back.GREEN + Fore.BLACK + q + Back.RESET + Fore.RESET + NEWLINE)

	url = get_search_url(q)
	browser.open_url(url, driver)

	return extract_results(answers, driver)

def extract_results(answers, driver=-1):
	soup = BeautifulSoup(browser.get_source(driver), features='lxml')

	titles = soup.find_all(H3, class_=CLASS_TITLE)
	snippets = soup.find_all(SPAN, class_=CLASS_SNIPPET)

	formatted = ''
	for title, snippet in zip(titles, snippets):
		title = title.text
		snippet = snippet.text

		if titles_visible:
			formatted += title_color + title + Back.RESET + NEWLINE 
		formatted += remove_em_tags(snippet) + NEWLINE*2
	
	plain = formatted
	for tag in COLORAMA_TAGS:
		plain = plain.replace(tag, '')
	
	if answers:
		formatted = color_keywords(formatted, answers)

	return plain, formatted

def get_search_url(q):
	return GOOGLE + quote(q)

def remove_em_tags(s):
	s = s.replace('<em>', '')
	s = s.replace('</em>', '')
	return s

def print_no_results(s):
	print(Back.RED, 'No results found! ', s, Back.RESET, sep='')

def color_keywords(s, keywords):
	def color(kw):
		nonlocal s
		case_insensitive = re.compile(r'\b%s\b' % kw, re.IGNORECASE)
		s = case_insensitive.sub(answer_color + kw + Back.RESET + Fore.RESET, s)

	for kw in keywords:
		color(kw)
		for word in ner(kw):
			if word[1] == 'Np':
				color(word[0])
	return s