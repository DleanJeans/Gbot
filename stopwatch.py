import time

class Stopwatch:
	then = 0
	duration = 0

	def start(self):
		self.then = time.time()

	def stop(self):
		now = time.time()
		duration = now - self.then
		self.duration = round(duration, 2)
	
	def print(self, prefix='Took:  '):
		print(prefix, self.duration, 's', sep='')
	
	def stop_n_print(self, prefix='Took:  '):
		self.stop()
		self.print(prefix)
