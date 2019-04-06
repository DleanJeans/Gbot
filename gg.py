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

def init():
	global driver, translator

	print('Opening Firefox...')
	driver = webdriver.Firefox()
	colorama.init()
	translator = Translator()
	print('Done!')

def translate(q):
	return translator.translate(q).text

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
		snippet = snippet.decode_contents().replace('<span class="f">', '').replace('</span>', '')
		
		if titles_visible:
			formatted += Back.BLUE + title + Back.RESET + NEWLINE 
		formatted += colorama_em_tags(snippet) + NEWLINE*2
	
	plain = formatted
	for tag in COLORAMA_TAGS:
		plain = plain.replace(tag, '')
	
	formatted = color_keywords(formatted, answers)

	return plain, formatted

def get_search_url(q):
	return GOOGLE + quote(q)

def colorama_em_tags(s):
	s = s.replace('<em>', Style.BRIGHT + Back.RED)
	s = s.replace('</em>', Style.NORMAL + Back.RESET)
	return s

def print_no_results(s):
	print(Back.RED, 'No results found! ', s, Back.RESET, sep='')

def color_keywords(s, keywords):
	for kw in keywords:
		# case_insensitive = re.compile(re.escape(kw), re.IGNORECASE)
		case_insensitive = re.compile(r'\b%s\b' % kw, re.IGNORECASE)
		s = case_insensitive.sub(Style.RESET_ALL + Back.YELLOW + Fore.BLACK + kw + Style.RESET_ALL, s)
	return s