from PIL import ImageDraw

box_outline_color = 185
top_offset = 100
skip = 400
side_offset = 40
step = 2
diff_threshold = 3

class ScreenTool:
	def process(self, image):
		center_x = image.width * 0.5
		top = None
		bottom = None

		grayscale_image = image.convert('L')

		y = 0
		while y < image.height:
			color = grayscale_image.getpixel((center_x, y))
			diff = abs(color - box_outline_color)

			if diff <= diff_threshold:
				if not top:
					top = y + top_offset
					y += skip
				elif not bottom:
					bottom = y
					break
			
			y += step

		rect = (side_offset, top, image.width - side_offset, bottom)
		image = grayscale_image.crop(rect)

		return image