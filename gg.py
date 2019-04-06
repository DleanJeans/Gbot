import colorama
import re

from selenium import webdriver
from colorama import Style, Back, Fore
from urllib.parse import quote
from bs4 import BeautifulSoup
from googletrans import Translator

GOOGLE = 'https://www.google.com/search?q='

H3 = 'h3'
SPAN = 'span'

CLASS_TITLE = 'LC20lb'
CLASS_SNIPPET = 'st'

NEWLINE = '\n'

COLORAMA_TAGS = [Back.BLUE, Back.RED, Back.RESET, Style.BRIGHT, Style.NORMAL]

titles_visible = True

title_color = Back.BLUE
answer_color = Fore.BLACK + Back.YELLOW

def init():
	global driver, translator

	print('Opening Firefox...')
	driver = webdriver.Firefox()
	colorama.init()
	translator = Translator()
	print('Done!')

def is_eng(a):
	return translator.detect(a).lang == 'en'

def translate(q):
	return translator.translate(q, src='vi', dest='en').text

def search(q, answers):
	""" Returns (plain, formatted)
	"""
	global driver

	print('Google:', Back.GREEN + Fore.BLACK + q + Back.RESET + Fore.RESET + NEWLINE)
	url = get_search_url(q)
	driver.get(url)

	soup = BeautifulSoup(driver.page_source, features='lxml')

	titles = soup.find_all(H3, class_=CLASS_TITLE)
	snippets = soup.find_all(SPAN, class_=CLASS_SNIPPET)

	formatted = ''
	for title, snippet in zip(titles, snippets):
		title = title.text
		snippet = snippet.decode_contents()
		snippet = snippet.replace('<span class="f">', '').replace('</span>', '')
		snippet = snippet.replace('<wbr>', '').replace('</wbr>', '')

		if titles_visible:
			formatted += title_color + title + Back.RESET + NEWLINE 
		formatted += remove_em_tags(snippet) + NEWLINE*2
	
	plain = formatted
	for tag in COLORAMA_TAGS:
		plain = plain.replace(tag, '')
	
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
	for kw in keywords:
		case_insensitive = re.compile(r'\b%s\b' % kw, re.IGNORECASE)
		s = case_insensitive.sub(answer_color + kw + Back.RESET + Fore.RESET, s)
	return s