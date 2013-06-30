"""2D drawing examples."""
import sys
from random import randint

# Try to import SDL2. The import might fail, if the SDL2 DLL could not be
# loaded. In that case, just print the error and exit with a proper
# error code.
try:
	from sdl2 import (SDL_QUIT, SDL_MOUSEBUTTONDOWN, SDL_Color, 
				SDL_BlitSurface, SDL_GetPerformanceFrequency, SDL_GetError,
				SDL_GetPerformanceCounter)
	from sdl2.sdlttf import (TTF_Init, TTF_Quit, TTF_OpenFont, 
				TTF_RenderText_Solid, TTF_RenderText_Shaded, TTF_GetError)
	import sdl2.ext as sdl2ext
	from sdl2.ext.ebs import World, Entity, System
except ImportError:
	import traceback
	traceback.print_exc()
	sys.exit(1)

RESOURCES = sdl2ext.Resources(__file__, "resources")

# Draws random lines on the passed surface
def draw_lines(surface, width, height):
	# Fill the whole surface with a black color.
	sdl2ext.fill(surface, 0)
	for x in range(15):
		# Create a set of four random points for drawing the line.
		x1, x2 = randint(0, width), randint(0, width)
		y1, y2 = randint(0, height), randint(0, height)
		# Create a random color.
		color = sdl2ext.Color(randint(0, 255),
							  randint(0, 255),
							  randint(0, 255))
		# Draw the line with the specified color on the surface.
		# We also could create a set of points to be passed to the function
		# in the form
		#
		# line(surface, color, (x1, y1, x2, y2, x3, y3, x4, y4, ...))
		#                       ^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^
		#                         first line     second line
		sdl2ext.line(surface, color, (x1, y1, x2, y2))


# Draws random, filled rectangles on the passed surface
def draw_rects(surface, width, height):
	# Fill the whole surface with a black color.
	sdl2ext.fill(surface, 0)
	for k in range(15):
		# Create a set of four random points for the edges of the rectangle.
		x, y = randint(0, width), randint(0, height)
		w, h = randint(1, width // 2), randint(1, height // 2)
		# Create a random color.
		color = sdl2ext.Color(randint(0, 255),
							  randint(0, 255),
							  randint(0, 255))
		# Draw the filled rect with the specified color on the surface.
		# We also could create a set of points to be passed to the function
		# in the form
		#
		# fill(surface, color, ((x1, y1, x2, y2), (x3, y3, x4, y4), ...))
		#                        ^^^^^^^^^^^^^^    ^^^^^^^^^^^^^^
		#                          first rect        second rect
		sdl2ext.fill(surface, color, (x, y, w, h))

class FPS(object):
	def __init__(self, renderer):
		super(FPS, self).__init__()
		self.renderer = renderer
		self.font = TTF_OpenFont(RESOURCES.get_path("tuffy.ttf"), 16)
	def process(self):
		freq = SDL_GetPerformanceFrequency()
		text = "FPS: " + str(freq)
		textSurface = TTF_RenderText_Shaded(self.font,text, SDL_Color(255, 255, 255), SDL_Color(40, 90, 120))
		SDL_BlitSurface(textSurface, None, self.renderer, None)
		
		
		

def run():
	# You know those from the helloworld.py example.
	# Initialize the video subsystem, create a window and make it visible.
	sdl2ext.init()
	TTF_Init()
	window = sdl2ext.Window("2D drawing primitives", size=(800, 600))
	window.show()
	

	# As in colorpalettes.py, explicitly acquire the window's surface to
	# draw on.
	windowsurface = window.get_surface()
	
	fps = FPS(windowsurface)

	# We implement the functionality as it was done in colorpalettes.py and
	# utilise a mapping table to look up the function to be executed, together
	# with the arguments they should receive
	functions = ((draw_lines, (windowsurface, 800, 600)),
				 (draw_rects, (windowsurface, 800, 600))
				 )

	# A storage variable for the function we are currently on, so that we know
	# which function to execute next.
	curindex = 0
	draw_lines(windowsurface, 800, 600)
	

	textSurface = TTF_RenderText_Shaded(font, repr(SDL_GetPerformanceFrequency()), SDL_Color(255, 255, 255), SDL_Color(40, 90, 120))
			
	# The event loop is nearly the same as we used in colorpalettes.py. If you
	# do not know, what happens here, take a look at colorpalettes.py for a
	# detailled description.
	running = True
	while running:
		events = sdl2ext.get_events()
		for event in events:
			if event.type == SDL_QUIT:
				running = False
				break
			if event.type == SDL_MOUSEBUTTONDOWN:
				curindex += 1
				if curindex >= len(functions):
					curindex = 0
				# In contrast to colorpalettes.py, our mapping table consists
				# of functions and their arguments. Thus, we get the currently
				# requested function and argument tuple and execute the
				# function with the arguments.
				func, args = functions[curindex]
				func(*args)
				break
		textSurface = TTF_RenderText_Shaded(font,"FPS: " + str(SDL_GetPerformanceFrequency()), SDL_Color(255, 255, 255), SDL_Color(40, 90, 120))
		SDL_BlitSurface(textSurface, None, windowsurface, None)
		window.refresh()
	TTF_Quit()
	sdl2ext.quit()
	return 0


if __name__ == "__main__":
	sys.exit(run())
