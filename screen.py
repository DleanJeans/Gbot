from PIL import ImageDraw

BOX_HEIGHT = 380
FRIENDS_WIDTH = 200
FRIENDS_Y = 150

def preprocess(image):
	rect = (0, image.height - BOX_HEIGHT, image.width, image.height)
	image = image.crop(rect)

	friends_pos = (image.width - FRIENDS_WIDTH, FRIENDS_Y)
	draw = ImageDraw.Draw(image)
	draw.rectangle((friends_pos, image.size), 'white')

	return image