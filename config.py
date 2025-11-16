'''Configuration file'''

# Maze geometry (deal with square maze for simplicty)
maze_width = maze_length = 100 # in pixels
W = 5  # cell width
n_rows = maze_width // W
n_cols = maze_length // W
outline = W // 5 # wall thickness
half_outline = outline // 2

# Colors 
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
light_blue = (173, 216, 230)
