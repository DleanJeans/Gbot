import os

DIRECTORY = os.path.dirname(__file__).replace('\\', '/') + '/%s/history'

def add(image):
	global images
	if images == None:
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