import os

DIRECTORY = os.path.dirname(__file__).replace('\\', '/') + '/%s/history/'

def add(image):
	global images
	if not 'images' in globals():
		images = []
	images.append(image)

def clear():
	global images
	images = []

def save(profile, folder_name):
	global images
	if images == [] or images == None:
		print('No images in history!')

	for i, image in enumerate(images):
		folder = DIRECTORY % profile + folder_name
		if not os.path.exists(folder):
			os.makedirs(folder)

		path = folder + '/%s.png' % (i + 1)
		print('Saving:', path)

		image.save(path)
	print('')

def get_days(profile):
	folder = DIRECTORY % profile
	walker = os.walk(folder)
	next(walker) # skip first one

	for dir in walker:
		print(os.path.basename(dir[0]))
	print('')