from PIL import ImageDraw

image_scale = 0.5

BOX_HEIGHT = 760
FRIENDS_WIDTH = 400
FRIENDS_Y = 300

def process(image):
	box_height = BOX_HEIGHT * image_scale
	friends_width = FRIENDS_WIDTH * image_scale
	friends_y = FRIENDS_Y * image_scale

	rect = (0, image.height - box_height, image.width, image.height)
	image = image.crop(rect)

	friends_pos = (image.width - friends_width, friends_y)
	draw = ImageDraw.Draw(image)
	draw.rectangle((friends_pos, image.size), 'white')

	return image.convert('L')

def post_process(image):
	return image

def cut_image(image):
	x = 10
	y = image.height * 0.175
	bx = image.width - 10
	by = image.height * 0.5

	image = image.crop((x, y, bx, by))

	return image