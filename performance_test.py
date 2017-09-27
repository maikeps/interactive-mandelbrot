import mandelbrot
from time import time

if __name__ == '__main__':
	test_count = 50
	results = []
	avg = 0

	for i in range(4):
		for j in range(int(test_count/4)):
			before = time()
			mandelbrot.update_image()
			after = time()

			elapsed = after-before
			avg += elapsed
			
			print(elapsed)
	
	avg /= test_count

	print('\nAvg: ' + str(avg))