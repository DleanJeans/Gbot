import os

images = []
directory = 'G:/Python/Confetti/history/'

def add(image):
	global images
	images.append(image)

def save(name):
	global images
	for i, image in enumerate(images):
		folder = directory + '%s' % name
		if not os.path.exists(folder):
			os.makedirs(folder)

		path = folder + '/%s.png' % (i + 1)
		print('Saving:', path)

		image.save(path)