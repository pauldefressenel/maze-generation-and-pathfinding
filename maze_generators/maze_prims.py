'''Maze Generation with Prim's Algorithm'''

# Import configs, classes, and libraries 
from utils.config import maze_width, n_rows, n_cols, white
from utils.cell import Cell
import pygame
import random
import time
import pickle

# Prim's Maze Generation Class
class MazePrims:
    def __init__(self):
        '''Initialize Pygame and data structures'''

        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((maze_width, maze_width))
        pygame.display.set_caption("Maze - Prim's Algorithm")

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

    def run(self):
        '''Run Prim's algorithm to generate the maze'''

        first_cell = self.cell_list[0][0]
        first_cell.inMaze = True

        # Add the four walls of starting cell
        self.wall_list.append([first_cell, 0])
        self.wall_list.append([first_cell, 1])
        self.wall_list.append([first_cell, 2])
        self.wall_list.append([first_cell, 3])

        # Generate maze
        running = True
        while running:
            while len(self.wall_list) > 0:
                random_wall = random.choice(self.wall_list)
                cell, direction = random_wall

                # Top wall
                if direction == 0:
                    dividing_cell = self.return_cell(cell.row - 1, cell.col)
                    if dividing_cell is not None:
                        if cell.inMaze ^ dividing_cell.inMaze:
                            self.delete_walls(cell, dividing_cell)
                            if not cell.inMaze:
                                cell.inMaze = True
                            if not dividing_cell.inMaze:
                                dividing_cell.inMaze = True
                                self.wall_list.append([dividing_cell, 0])
                                self.wall_list.append([dividing_cell, 1])
                                self.wall_list.append([dividing_cell, 3])

                # Right wall
                if direction == 1:
                    dividing_cell = self.return_cell(cell.row, cell.col + 1)
                    if dividing_cell is not None:
                        if cell.inMaze ^ dividing_cell.inMaze:
                            self.delete_walls(cell, dividing_cell)
                            if not cell.inMaze:
                                cell.inMaze = True
                            if not dividing_cell.inMaze:
                                dividing_cell.inMaze = True
                                self.wall_list.append([dividing_cell, 0])
                                self.wall_list.append([dividing_cell, 1])
                                self.wall_list.append([dividing_cell, 2])

                # Bottom wall
                if direction == 2:
                    dividing_cell = self.return_cell(cell.row + 1, cell.col)
                    if dividing_cell is not None:
                        if cell.inMaze ^ dividing_cell.inMaze:
                            self.delete_walls(cell, dividing_cell)
                            if not cell.inMaze:
                                cell.inMaze = True
                            if not dividing_cell.inMaze:
                                dividing_cell.inMaze = True
                                self.wall_list.append([dividing_cell, 1])
                                self.wall_list.append([dividing_cell, 2])
                                self.wall_list.append([dividing_cell, 3])

                # Left wall
                if direction == 3:
                    dividing_cell = self.return_cell(cell.row, cell.col - 1)
                    if dividing_cell is not None:
                        if cell.inMaze ^ dividing_cell.inMaze:
                            self.delete_walls(cell, dividing_cell)
                            if not cell.inMaze:
                                cell.inMaze = True
                            if not dividing_cell.inMaze:
                                dividing_cell.inMaze = True
                                self.wall_list.append([dividing_cell, 0])
                                self.wall_list.append([dividing_cell, 2])
                                self.wall_list.append([dividing_cell, 3])

                # Remove processed wall
                self.wall_list.remove(random_wall)

                # Draw & save frame
                self.update_canvas()
                pygame.image.save(self.screen, f"./frame_{self.frame_count:05d}.png")
                self.frame_count += 1

            # Final save
            self.update_canvas()
            pygame.image.save(self.screen, "maze_prims.png")
            with open("maze_prims.dat", "wb") as f:
                pickle.dump(self.cell_list, f)
            break

# Run the algorithm
if __name__ == "__main__":

    start = time.time()
    maze = MazePrims()
    maze.run()
    end = time.time()
    print(f"Total Time Elapsed: {(end - start)}")
