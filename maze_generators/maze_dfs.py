'''Maze Generation with Depth First Search Algorithm'''

# Import configs, classes, and libraries 
from utils.config import maze_width, n_rows, n_cols, white
from utils.cell import Cell
import pygame
import random
import time
import pickle

# DFS Maze Generation Class
class MazeDFS:
    def __init__(self):
        '''Initialize Pygame and data structures'''

        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((maze_width, maze_width))
        pygame.display.set_caption('Maze - Depth First Search')

        # Data structures setup
        self.cell_list = []
        self.wall_list = []
        self.frame_count = 0
        self.set_up()

    def set_up(self):
        '''Create full grid of Cell objects'''

        for i in range(n_rows):
            self.cell_list.append([])
            for j in range(n_cols):
                self.cell_list[i].append(
                    Cell(i, j, [True, True, True, True],
                         False, False, False, 
                         [False, False, False, False]))

    def return_cell(self, row, col):
        '''Return Cell object at (row, col) or None if out of bounds'''

        if row < 0 or col < 0 or row > n_rows - 1 or col > n_cols - 1:
            return None
        
        return self.cell_list[row][col]

    @staticmethod
    def delete_walls(current_cell, next_cell):
        '''Remove walls between two neighbouring cells'''

        x = current_cell.row - next_cell.row
        if x == 1: # Next is above 
            current_cell.lines[3] = False
            next_cell.lines[1] = False
        elif x == -1: # Next is below
            current_cell.lines[1] = False
            next_cell.lines[3] = False

        y = current_cell.col - next_cell.col
        if y == 1: # Next is left
            current_cell.lines[0] = False
            next_cell.lines[2] = False
        elif y == -1: # Next is right
            current_cell.lines[2] = False
            next_cell.lines[0] = False

    def update_canvas(self):
        '''Redraw the maze on the Pygame screen'''

        self.screen.fill(white)
        for i in range(n_rows):
            for j in range(n_cols):
                self.cell_list[i][j].draw(self.screen)
        pygame.display.update()

    def get_near_cell(self, current_cell):
        '''Return a random neighbouring cell that is not yet in the maze'''
        
        neighbours = []
        # Fetch all neighbouring cells
        top_cell = self.return_cell(current_cell.row - 1, current_cell.col)
        right_cell = self.return_cell(current_cell.row, current_cell.col + 1)
        bottom_cell = self.return_cell(current_cell.row + 1, current_cell.col)
        left_cell = self.return_cell(current_cell.row, current_cell.col - 1)

        # Append eligible neighbours
        if top_cell is not None and not top_cell.inMaze:
            neighbours.append(top_cell)
        if right_cell is not None and not right_cell.inMaze:
            neighbours.append(right_cell)
        if bottom_cell is not None and not bottom_cell.inMaze:
            neighbours.append(bottom_cell)
        if left_cell is not None and not left_cell.inMaze:
            neighbours.append(left_cell)

        # Return a random neighbour or None
        if len(neighbours) == 0:
            return None
        if len(neighbours) == 1:
            return neighbours[0]
        return random.choice(neighbours)

    def run(self):
        '''Run DFS algorithm to generate the maze'''

        current = self.cell_list[0][0]
        current.inMaze = True

        # Generate maze
        while True:
            next_cell = self.get_near_cell(current)

            # Move forward
            if next_cell is not None:
                next_cell.inMaze = True
                self.wall_list.append(current)
                self.delete_walls(current, next_cell)
                current = next_cell

            # Backtrack
            elif len(self.wall_list) > 0:
                current = self.wall_list.pop()

            # Finished
            else:
                break

            # Draw & save frame
            self.update_canvas()
            pygame.image.save(self.screen, f"./frame_{self.frame_count:05d}.png")
            self.frame_count += 1

        # Final save
        self.update_canvas()
        pygame.image.save(self.screen, "maze_dfs.png")
        with open("maze_dfs.dat", "wb") as f:
            pickle.dump(self.cell_list, f)

# Run the algorithm
if __name__ == "__main__":
    
    start = time.time()
    maze = MazeDFS()
    maze.run()
    end = time.time()
    print(f"Total Time Elapsed: {(end - start)}")
