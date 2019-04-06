print('Loading...')

import screenstream
import gg
import screen
import ocr
import quiz
import history
import count
import points
import os

from tabulate import tabulate
from colorama import Back, Fore

from PIL import Image

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

print('Call confetti.init() before running')
def init():
	gg.init()

def clear():
	history.clear()
	_ = os.system('cls')

def run_history(folder, image):
	try:
		image = Image.open('G:/Python/Confetti/history/%s/%s.png' % (folder, image))
	except FileNotFoundError as e:
		print(e)
		return
	run_image(image)

def run_image(image):
	print('OCR...')
	text = ocr.read_image(image)
	text = quiz.process(text)
	q = NEWLINE.join(text)
	print(q, NEWLINE)
	
	answer(q)

def run():
	print('Capturing...')
	ip = '192.168.1.' + str(oct4)
	image = screenstream.capture(ip)
	image = screen.preprocess(image)
	history.add(image)

	run_image(image)

def save_history(name):
	history.save(name)

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
	
	if not points.same_best_answer(points_dict):
		no_ans_q = q.split('?')[0]
		plain, formatted = gg.search(no_ans_q, answers)
		to_be_printed.append(formatted)
		points_dict[NO_ANS+EXACT] = count.exact(plain, answers)
		points_dict[NO_ANS+SPLIT] = count.splitted(plain, answers)

	no_answers = sum(points_dict[EXACT]) == 0 and sum(points_dict[SPLIT]) == 0

	if no_answers:
		print('Translating...')
		eng_q = gg.translate(q)
		translated_answers = [gg.translate(a) for a in answers]
		print(eng_q)
		print(NEWLINE.join(translated_answers))
		print(NEWLINE)

		plain, formatted = gg.search(eng_q, answers)
		to_be_printed.append(formatted)
		points_dict[ENG] = count.splitted(plain, answers)

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
	for r in combined_results:
		print(r[0], NEWLINE)
