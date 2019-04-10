import matplotlib.pyplot as plt

def show(image, title='Image', cmap=None):
	fig = plt.figure()
	fig.canvas.set_window_title(title)
	plt.imshow(image, cmap=cmap)
	plt.show()