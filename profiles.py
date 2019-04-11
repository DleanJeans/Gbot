import importlib

PROFILES = {
	'mb': 'masterbrain',
	'cft': 'confetti'
}

MODULES = [
	'screen',
	'quiz',
	'config',
	'lang'
]

if 'current_profile' not in globals():
	current_profile = ''

def get_name(profile):
	for short, full in PROFILES.items():
		profile = profile.replace(short, full)
	return profile

def load(profile):
	global current_profile

	gbot = importlib.import_module('gbot')

	profile = get_name(profile)
	current_profile = profile
	
	path = f'{profile}'
	module = importlib.import_module(path)

	gbot.config = module.config
	gbot.screen = module.screen
	gbot.quiz = module.quiz
	gbot.points.lang = module.lang
	gbot.count.lang = module.lang
	
	print(f'Profile \'{profile}\' loaded!')

def reload():
	global current_profile

	for module in MODULES:
		module = current_profile + '.' + module
		module = importlib.import_module(module)
		importlib.reload(module)
	load(current_profile)