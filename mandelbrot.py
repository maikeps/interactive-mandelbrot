import multiprocessing
import tkinter

from colour import Color
from math import sqrt, cos, atan
from PIL import Image
from PIL import ImageTk

N_MAX_ITERATIONS = 256
N_THREADS = 4
WIDTH = 128
HEIGHT = 128
SCALE_FACTOR = 1
X_CENTER = 0.3
Y_CENTER = 0.7
GRADIENT = list(Color('blue').range_to(Color('black'), N_MAX_ITERATIONS))



def mandelbrot(start_row, start_col, n_rows, n_cols, x_center=0, y_center=0, scale_factor=1.0):
	pixels_list = []
	grey_shade = 0

	for i in range(start_col, start_col+n_cols):
		for j in range(start_row, start_row+n_rows):
			x = x_center + scale_factor * float(i - WIDTH/2)/WIDTH
			y = y_center + scale_factor * float(j - HEIGHT/2)/HEIGHT

			it = 0
			a, b = (0.0, 0.0)
			r, g, b = 0, 0, 0

			# optimization
			p = sqrt((x-1/4)**2 + y**2)
			if x < p - 2*p**2 + 1/4:
				it = N_MAX_ITERATIONS
			else:
				while it < N_MAX_ITERATIONS and a**2 + b**2 < 4.0:
					a, b = a**2 - b**2 + x, 2*a*b + y
					it += 1

			r, g, b = GRADIENT[it-1].rgb

			pixels_list.append({'x': i, 'y': j, 'r': int(r*255), 'g': int(g*255), 'b': int(b*255), 'iterations': it})

	return pixels_list

def update_image():
	rows = int(HEIGHT/N_THREADS)
	pixels = []

	arg_list = []
	for i in range(N_THREADS):
		arg_list.append((rows*i, 0, rows, WIDTH, X_CENTER, Y_CENTER, SCALE_FACTOR))

	pool = multiprocessing.Pool(processes=4)
	res = pool.starmap(mandelbrot, arg_list)

	for l in res:
		pixels += l

	image = Image.new('RGB', (WIDTH, HEIGHT))

	for pixel in pixels:
		x, y = pixel['x'], pixel['y']
		r, g, b = pixel['r'], pixel['g'], pixel['b']
		image.putpixel((x, y), (r, g, b))

	return image


class Mandelbrot():
	def __init__(self):
		self.root = tkinter.Tk()
		self.root.bind('<Left>', self.left_pressed)
		self.root.bind('<Right>', self.right_pressed)
		self.root.bind('<Up>', self.up_pressed)
		self.root.bind('<Down>', self.down_pressed)
		self.root.bind('<Return>', self.zoom_in)
		self.root.bind('<BackSpace>', self.zoom_out)

		self.frame = tkinter.Frame(self.root, width=WIDTH, height=HEIGHT)
		self.frame.bind('<Button-1>', self.clicked)
		self.frame.pack()

		self.canvas = tkinter.Canvas(self.frame, width=WIDTH, height=HEIGHT)
		self.canvas.pack()

		image = update_image()
		self.tk_image = ImageTk.PhotoImage(image)
		self.mandelbrot_image = self.canvas.create_image(WIDTH/2, HEIGHT/2, image=self.tk_image)

		self.root.mainloop()

	def left_pressed(self, event):
		global X_CENTER, SCALE_FACTOR
		X_CENTER -= 0.1*SCALE_FACTOR		

		self.tk_image = ImageTk.PhotoImage(update_image())
		self.canvas.itemconfig(self.mandelbrot_image, image=self.tk_image)
		
	def right_pressed(self, event):
		global X_CENTER, SCALE_FACTOR
		X_CENTER += 0.1*SCALE_FACTOR	

		self.tk_image = ImageTk.PhotoImage(update_image())
		self.canvas.itemconfig(self.mandelbrot_image, image=self.tk_image)

	def up_pressed(self, event):
		global Y_CENTER, SCALE_FACTOR
		Y_CENTER -= 0.1*SCALE_FACTOR

		self.tk_image = ImageTk.PhotoImage(update_image())
		self.canvas.itemconfig(self.mandelbrot_image, image=self.tk_image)

	def down_pressed(self, event):
		global Y_CENTER, SCALE_FACTOR
		Y_CENTER += 0.1*SCALE_FACTOR

		self.tk_image = ImageTk.PhotoImage(update_image())
		self.canvas.itemconfig(self.mandelbrot_image, image=self.tk_image)

	def zoom_in(self, event):
		global SCALE_FACTOR
		SCALE_FACTOR /= 2

		self.tk_image = ImageTk.PhotoImage(update_image())
		self.canvas.itemconfig(self.mandelbrot_image, image=self.tk_image)

	def zoom_out(self, event):
		global SCALE_FACTOR
		SCALE_FACTOR *= 2

		self.tk_image = ImageTk.PhotoImage(update_image())
		self.canvas.itemconfig(self.mandelbrot_image, image=self.tk_image)


	def clicked(self, event):
		print(str(event.x) + ' - ' + str(event.y))


if __name__ == '__main__':
	m = Mandelbrot()