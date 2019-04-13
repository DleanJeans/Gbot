from stopwatch import Stopwatch

sw = Stopwatch()
sw.start()
print('Loading...')

import screenstream
import gg
import ocr
import history
import count
import points
import os
import profiles
import importlib

from tabulate import tabulate
from colorama import Back, Fore
from PIL import Image
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool
from lprint import print

print('Done!', end=' ')
sw.stop_and_print()

TAB = '\t'
SPACE = ' '
NEWLINE = '\n'
QUOTE = '"'

ANSWERS = 'Answers'
EXACT = 'Exact'
SPLIT = 'Split'
NO_ANS = 'NoAns'
ENG = 'Eng'

oct4 = 179

print('Call gbot.start(profile, octet4) before running')
def start(profile='', octet4=None):
	sw.start()

	global oct4
	if octet4:
		oct4 = octet4
	if profile != '':
		load_profile(profile)
	gg.start()
	
	sw.stop_and_print()

def reload_everything():
	import pkgutil

	files = [name for _, name, _ in pkgutil.iter_modules([''])]
	print(files)
	for file in files:
		reload(file)

def reload(module_name='gbot'):
	module_name = profiles.get_name(module_name)
	module = importlib.import_module(module_name)
	importlib.reload(module)

	if module_name in profiles.PROFILES.values():
		profiles.reload()
	
	print(f'Module \'{module_name}\' reloaded!')

def load_profile(name):
	profiles.load(name)

def clear():
	history.clear()
	os.system('cls')

def run_history(folder, image):
	sw.start()

	profile = profiles.current_profile
	dirname = os.path.dirname(__file__).replace('\\', '/')
	
	try:
		image = Image.open(f'{dirname}/{profile}/history/{folder}/{image}.png')
	except FileNotFoundError as e:
		print(e, NEWLINE)
		return
	
	image = screen.post_process(image)
	run_image(image)

	sw.stop_and_print('run_history() took: ')

def run_image(image):
	print('OCR...')
	text = ocr.read_image(image, *config.ocr)

	while True:
		print(text, NEWLINE)
		text = quiz.process(text)
		q = NEWLINE.join(text)
		if quiz.is_valid(q):
			break
		else:
			text = ocr.read_image(image, *config.ocr2)
	print(q, NEWLINE)
	
	answer(q)

def run():
	sw.start()

	print('Capturing...')
	ip = '192.168.1.' + str(oct4)
	image = screenstream.capture(ip)
	image = screen.process(image)
	history.add(image)

	run_image(image)

	sw.stop_and_print('run() took: ')

def save_history(name):
	profile = profiles.current_profile
	history.save(profile, name)

def do_search(search):
	name = search[0]
	search = search[1:]
	plain, formatted = gg.search(*search)

	answers = search[1]
	exact_count = count.exact(plain, answers)
	split_count = count.splitted(plain, answers)

	return name, formatted, exact_count, split_count

def answer(q):
	def get_q(q):
		return q

	def get_no_ans_q(q, answers):
		q = q.replace(' '.join(answers), '')
		print('Removed Answers:', NEWLINE, q)
		return q

	def get_eng_q(q):
		print('Translating...', end='\r')
		q = gg.translate(q)
		print('Translated:', NEWLINE, q)
		return q

	sw.start()

	translated = False
	
	print('')
	answers = extract_answers(q)
	
	q = q.replace(NEWLINE, ' ')

	searches = []

	get_q = partial(get_q, q)
	get_no_ans_q = partial(get_no_ans_q, q, answers)

	searches.append(('', get_q, answers, 0))
	searches.append((NO_ANS, get_no_ans_q, answers, 1))

	answers_in_eng = any([gg.is_eng(a) for a in answers])

	if config.enable_translate and (config.force_translate or answers_in_eng):
		if not answers_in_eng:
			answers = [gg.translate(a) for a in answers]
		get_eng_q = partial(get_eng_q, q)
		
		searches.append((ENG, get_eng_q, answers, 2))

	to_be_printed = []
	name_to_points = {}
	
	with ThreadPool(3) as pool:
		results = pool.map(do_search, searches)
	
	for search_res in results:
		name, formatted, exact_count, split_count = search_res

		to_be_printed.append(formatted)
		name_to_points[name + EXACT] = exact_count
		name_to_points[name + SPLIT] = split_count
	
	print_roundrobin_reversed(to_be_printed)

	name_to_points = points.negate_if_negative(q, name_to_points)
	points.add_total(name_to_points)
	name_to_points = points.color_best(name_to_points)

	# add answers as headers
	table = {ANSWERS:answers}
	table.update(name_to_points)

	print(tabulate(table, headers='keys'))
	print(NEWLINE)

def extract_answers(q):
	return q.split(NEWLINE)[1:]

def print_roundrobin_reversed(to_be_printed):
	to_be_printed = [text.split(NEWLINE*2)[::-1] for text in to_be_printed]
	combined_results = zip(*to_be_printed)
	for result in combined_results:
		for text in result:
			print(text, NEWLINE)
