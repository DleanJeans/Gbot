import confetti
import logging
import traceback

confetti.init()

while True:
	command = input('>>> ')
	try:
		eval(command)
	except Exception as e:
		logging.error(traceback.format_exc())