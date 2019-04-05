import cv2
import click
import matplotlib.pyplot as plt
import imagedisplay
from PIL import Image

"""
A script to capture a frame from the ScreenStream app
https://github.com/dkrivoruchko/ScreenStream
"""

HTTP = 'http://'
MJPEG = '/stream.mjpeg'

def capture(ip, port=8080, show=False, verbose=False):
	url = HTTP + ip + ':%s' % port + MJPEG
	if verbose:
		print('Requesting:', url)
	
	cap = cv2.VideoCapture(url)

	if verbose:
		print('Done.')

	_, frame = cap.read()
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	image = Image.fromarray(frame)

	if show:
		imagedisplay.show(image, 'ScreenStream - %s:%s' % (ip, port))

	return image


@click.command()
@click.option('-ip', default='192.168.1.100', help='Phone IP Address')
@click.option('-port', default=8080, help='The Server Port')
@click.option('--show', default=False, is_flag=True)
@click.option('--verbose/--no-verbose', default=True, is_flag=True)
def cli(ip, port=8080, show=False, verbose=True):
	capture(ip, port, show, verbose)

if __name__ == '__main__':
	cli()