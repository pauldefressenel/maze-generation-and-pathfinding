'''Cell class representing each cell in the maze'''

import pygame
from config import W, outline, half_outline, light_blue, red, black

class Cell:
    def __init__(self, row, col, lines=None, inPath=False,
                 inMaze=False, highlighted=False, arrows=None):
        '''Initialize a cell at (row, col) given walls and state'''

        if lines is None:
            lines = [True, True, True, True]
        if arrows is None:
            arrows = [False, False, False, False]

        self.row = row
        self.col = col
        self.lines = lines
        self.inPath = inPath
        self.inMaze = inMaze
        self.highlighted = highlighted
        self.arrows = arrows

    def draw(self, screen):
        '''Draw the cell on the Pygame screen'''

        if self.inMaze:
            pygame.draw.rect(screen, light_blue, pygame.Rect
                             (self.row * W, self.col * W, W, W))

        if self.highlighted:
            pygame.draw.rect(screen, red, pygame.Rect
                             (self.row * W, self.col * W, W, W))
        # Top wall 
        if self.lines[0]:
            pygame.draw.line(screen, black, (self.row * W, self.col * W), 
                             (self.row * W + W + half_outline, self.col * W), outline)

        # Right wall    
        if self.lines[1]:
            pygame.draw.line(screen, black, (self.row * W + W, self.col * W), 
                             (self.row * W + W, self.col * W + W + half_outline), outline)
        # Bottom wall
        if self.lines[2]:
            pygame.draw.line(screen, black, (self.row * W, self.col * W + W), 
                             (self.row * W + W + half_outline, self.col * W + W), outline)
        # Left wall
        if self.lines[3]:
            pygame.draw.line(screen, black, (self.row * W, self.col * W), 
                             (self.row * W, self.col * W + W + half_outline), outline)