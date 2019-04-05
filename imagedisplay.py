import matplotlib.pyplot as plt

def show(image, title='Image'):
	fig = plt.figure()
	fig.canvas.set_window_title(title)
	plt.imshow(image)
	plt.show()