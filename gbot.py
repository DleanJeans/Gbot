print('Loading...')

import screenstream
import gg
import ocr
import history
import count
import points
import os

from tabulate import tabulate
from colorama import Back, Fore
from PIL import Image
import importlib

print('Done!')

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

force_no_answer_search = True
force_translate = False

CUSTOM_MODULES = [
	'screen',
	'quiz',
	'config'
]

print('Call gbot.init(profile, octet4) before running', NEWLINE)
def init(profile, octet4):
	global oct4
	oct4 = octet4
	load_profile(profile)
	gg.init()

def get_profile(profile):
	profile = {
		'mb': 'masterbrain',
		'cft': 'confetti'
	}.get(profile, profile)
	return profile

def load_profile(profile):
	global config, screen, quiz
	profile = get_profile(profile)
	
	path = f'{profile}.config'
	config = importlib.import_module(path)

	screen = config.ScreenTool()
	quiz = config.QuizTool()
	points.lang = config.LangTool()
	count.lang = config.LangTool()
	
	print(f'Profile \'{profile}\' loaded!', NEWLINE)

def reload(module_name='gbot', profile=''):
	module_name = module_name.replace('cft', 'confetti').replace('mb', 'masterbrain')
	module = importlib.import_module(module_name, profile)
	importlib.reload(module)
	print(f'Module \'{module_name}\' reloaded!', NEWLINE)

def clear():
	history.clear()
	os.system('cls')

def run_history(profile, folder, image):
	profile = get_profile(profile)
	dirname = os.path.dirname(__file__).replace('\\', '/')

	try:
		image = Image.open(f'{dirname}/{profile}/history/{folder}/{image}.png')
	except FileNotFoundError as e:
		print(e, NEWLINE)
		return
	
	image = screen.post_process(image)

	run_image(image)

def run_image(image):
	print('OCR...')
	text = ocr.read_image(image, *config.ocr)
	print(text)
	text = quiz.process(text)
	q = NEWLINE.join(text)
	print(q, NEWLINE)
	
	answer(q)

def run():
	print('Capturing...')
	ip = '192.168.1.' + str(oct4)
	image = screenstream.capture(ip)
	image = screen.process(image)
	history.add(image)

	run_image(image)

def save_history(profile, name):
	profile = get_profile(profile)
	history.save(profile, name)

def answer(q):
	translated = False
	
	print('')
	answers = extract_answers(q)
	
	q = q.replace(NEWLINE, ' ')

	points_dict = {}
	plain, formatted = gg.search(q, answers)

	if plain == '' and q.count(QUOTE) >= 2:
		q = q.replace(QUOTE, '')
		gg.print_no_results('Removing quotes...')
		plain, formatted = gg.search(q, answers)
	
	to_be_printed = [formatted]

	points_dict[EXACT] = count.exact(plain, answers)
	points_dict[SPLIT] = count.splitted(plain, answers)
	
	if config.force_no_answer_search or not points.same_best_answer(points_dict):
		no_ans_q = q.replace(' '.join(answers), '')
		plain, formatted = gg.search(no_ans_q, answers)
		to_be_printed.append(formatted)
		points_dict[NO_ANS+EXACT] = count.exact(plain, answers)
		points_dict[NO_ANS+SPLIT] = count.splitted(plain, answers)

	if config.enable_translate:
		if not config.force_translate:
			no_matches = sum(points_dict[EXACT]) == 0 and sum(points_dict[SPLIT]) == 0
			answers_in_eng = any([gg.is_eng(a) for a in answers])

		if config.force_translate or answers_in_eng or no_matches:
			print('Translating...')
			eng_q = gg.translate(q)
			translated_answers = [gg.translate(a) for a in answers]
			print(eng_q)
			print(NEWLINE.join(translated_answers))
			print(NEWLINE)

			plain, formatted = gg.search(eng_q, answers)
			to_be_printed.append(formatted)
			points_dict[ENG] = count.splitted(plain, translated_answers)

	print_roundrobin_reversed(to_be_printed)

	points_dict = points.negate_if_negative(q, points_dict)
	points_dict = points.color_best(points_dict)
	table = {ANSWERS:answers}
	table.update(points_dict)

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
