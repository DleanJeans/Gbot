from threading import Lock

lock = Lock()
p = print

def print(*a, **b):
	with lock:
		p(*a, **b)