print('Loading...')

import screenstream
import screen
import ocr
import quiz

import webbrowser as wb
import os

from urllib.parse import quote
from selenium import webdriver
from bs4 import BeautifulSoup
from colorama import init as init_colorama, Fore, Back, Style
from googletrans import Translator
from PIL import Image

print('Done!')

GOOGLE = 'https://www.google.com/search?q='
NEWLINE = '\n'
TAB = '\t'
SPACE = ' '
translator = Translator()
CLASS_TITLE = 'LC20lb'
CLASS_SNIPPET = 'st'
QUOTE = '"'
SPAN = 'span'
H3 = 'h3'

print('Call confetti.init() before running')
def init():
	global driver

	init_colorama()
	print('Opening Firefox...')
	driver = webdriver.Firefox()
	print('Done!')

def decorate_em_tag(s):
	s = s.replace('<em>', Style.BRIGHT + Back.RED)
	s = s.replace('</em>', Style.NORMAL + Back.RESET)
	return s

def get_google_url(q):
	return GOOGLE + quote(q)

def google_for_results(q):
	global driver

	q = q.replace(NEWLINE, ' ')
	print('Google:', Back.GREEN, Fore.BLACK, q, Fore.RESET, Back.RESET, end=NEWLINE*2)

	url = get_google_url(q)
	driver.get(url)

	source = driver.page_source
	soup = BeautifulSoup(source, features='lxml')
	titles = soup.find_all(H3, class_=CLASS_TITLE)
	snippets = soup.find_all(SPAN, class_=CLASS_SNIPPET)

	return titles, snippets

def no_results_remove_quote(q):
	global titles
	if len(titles) == 0 and q.count(QUOTE) > 0:
		print('No results found! Removing quotes...', NEWLINE)
		q = q.replace(QUOTE, '')
		return True, q
	return False, q

def print_results():
	global titles, snippets

	for title, snip in zip(titles, snippets):
		print(Back.BLUE + title.text + Back.RESET)

		snip = str(snip).replace('<span class="st">', '').replace('<span class="f">', '').replace('</span>', '')
		snip = decorate_em_tag(snip)
		print(snip, end=NEWLINE*2)

def get_keywords():
	global keywords, answers

	keywords = list(answers)
	for i in range(len(answers) - 1):
		ans1 = answers[i]
		ans2 = answers[i + 1]

		common = list(set(ans1.split()) & set(ans2.split()))
		for c in common:
			ans1 = ans1.replace(c, '')
			ans2 = ans2.replace(c, '')
		keywords[i] = ans1.lower()
		keywords[i + 1] = ans2.lower()
	return keywords

def translate(q):
	return translator.translate(q).text

def count_in_snippets(keyword):
	return max([all_snippets.split().count(a) for a in keyword.split()])

def print_answer_counts():
	global answers, keywords, count_table, columns

	all_count = []
	for answer, keyword in zip(answers, keywords):
		count = count_in_snippets(keyword)
		all_count.append(count)
		print(answer, ': ', count, sep='')
	count_table.append(all_count)

	return sum(all_count)

def google(q):
	global answers, titles, snippets, keywords, all_snippets, count_table, columns

	count_table = []
	answers = extract_answers(q)
	enable_translate = False

	while True:
		if enable_translate:
			q = translate(q)
		
		titles, snippets = google_for_results(q)
		no_results, q = no_results_remove_quote(q)
		if no_results:
			columns = columns[1:]
			continue

		print_results()
		
		all_snippets = NEWLINE.join([s.text for s in snippets]).lower()
		keywords = get_keywords()

		no_counts = not print_answer_counts()
		
		if no_counts:
			print('')
			no_results, q = no_results_remove_quote(q)
			if no_results:
				continue
			elif not enable_translate:
				enable_translate = True
				print('No results found! Google Translating...', NEWLINE)
				continue
		
		print(NEWLINE)
		break

def extract_answers(q):
	return q.split(NEWLINE)[1:]

oct4 = 179

image_history = []

def run_history(folder, image):
	image = Image.open('G:/Python/Confetti/history/%s/%s.png' % (folder, image))
	run_on_image(image)

def run_on_image(image):
	print('OCR...')
	text = ocr.read_image(image)
	text = text.replace('”', QUOTE)
	text = quiz.process(text)
	q = NEWLINE.join(text)
	print(q, NEWLINE)
	
	google(q)

def run():
	print('Capturing...')
	ip = '192.168.1.' + str(oct4)
	image = screenstream.capture(ip)
	image = screen.preprocess(image)
	image_history.append(image)

	run_on_image(image)
	
def save_history(folder_name):
	for i, image in enumerate(image_history):
		folder = 'G:/Python/Confetti/history/%s' % folder_name
		if not os.path.exists(folder):
			os.makedirs(folder)

		path = folder + '/question%s.png' % (i + 1)
		print('Saving:', path)

		image.save(path)