print('Loading...')

import screenstream
import gg
import screen
import ocr
import quiz
import history

from PIL import Image

print('Done!')

TAB = '\t'
SPACE = ' '
NEWLINE = '\n'

QUOTE = '"'

print('Call confetti.init() before running')
def init():
	gg.init()

oct4 = 179
image_history = []

def run_history(folder, image):
	image = Image.open('G:/Python/Confetti/history/%s/%s.png' % (folder, image))
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

	while True:
		plain, formatted = gg.search(q)

		plain = plain.lower()
		points = count(answers, plain)

		formatted = gg.color_keywords(formatted, answers)
		print(formatted)
		print_points(answers, points)
		print(NEWLINE * 2)

		if plain == '' and q.count(QUOTE) >= 2:
			q = q.replace(QUOTE, '')
			gg.print_no_results('Removing quotes...')
			continue
		
		if points == [0, 0, 0] and not translated:
			gg.print_no_results('Translating...')
			q = gg.translate(q)
			print(q)
			translated = True
			continue

		break

def extract_answers(q):
	return q.split(NEWLINE)[1:]

def count(answers, text):
	return [text.count(a.lower()) for a in answers]

def print_points(answers, points):
	for answer, point in zip(answers, points):
		print(answer, ': ', point, sep='')