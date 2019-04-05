import colorama

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

def init():
	global driver, translator

	print('Opening Firefox...')
	driver = webdriver.Firefox()
	colorama.init()
	translator = Translator()
	print('Done!')

def translate(q):
	return translator.translate(q).text

def search(q):
	""" Returns (plain_text, formatted_text)
	"""
	global driver

	print('Google:', Back.GREEN + Fore.BLACK + q + Style.RESET_ALL + NEWLINE)
	url = get_search_url(q)
	driver.get(url)

	soup = BeautifulSoup(driver.page_source, features='lxml')

	titles = soup.find_all(H3, class_=CLASS_TITLE)
	snippets = soup.find_all(SPAN, class_=CLASS_SNIPPET)

	formatted_text = ''
	for title, snippet in zip(titles, snippets):
		title = title.text
		snippet = snippet.decode_contents().replace('<span class="f">', '').replace('</span>', '')
		
		formatted_text += Back.BLUE + title + Back.RESET + NEWLINE + colorama_em_tags(snippet) + NEWLINE*2
	
	plain_text = formatted_text
	for tag in COLORAMA_TAGS:
		plain_text = plain_text.replace(tag, '')
	
	return plain_text, formatted_text

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
		s = s.replace(kw, Style.RESET_ALL + Back.GREEN + Fore.BLACK + kw + Style.RESET_ALL)
	return s