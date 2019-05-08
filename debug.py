import gbot
import logging
import traceback

while True:
	command = input('>>> ')
	try:
		eval(command)
	except Exception as e:
		logging.error(traceback.format_exc())