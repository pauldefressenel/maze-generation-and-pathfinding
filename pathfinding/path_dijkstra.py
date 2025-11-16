'''Pathfinding with Dijkstra Algorithm'''

# Import configs, classes, and libraries 
from utils.config import W, maze_width, n_rows, n_cols, white, red, light_blue 
from utils.cell import Cell
import networkx as nx
import pygame
import time
import pickle

# Dijkstra Pathfinder Class
class DijkstraPathfinder:
    def __init__(self):
        '''Initialize Pygame, load maze, and reset cell states'''

        # Setup Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((maze_width, maze_width))
        pygame.display.set_caption("Dijkstra Pathfinding")

        # Load the .dat maze
        with open("./maze_prims.dat", "rb") as f:
            self.cells = pickle.load(f)

        # Reset cell states
        for i in range(n_rows):
            for j in range(n_cols):
                self.cells[i][j].inMaze = False
                self.cells[i][j].inPath = False
                self.cells[i][j].highlighted = False
                self.cells[i][j].visited = False 

        self.frame_count = 0

    def return_cell(self, row, col):
        '''Return Cell object at (row, col) or None if out of bounds'''

        if row < 0 or col < 0 or row > n_rows - 1 or col > n_cols - 1:
            return None
        
        return self.cells[row][col]
   
    def update_canvas(self):
        '''Redraw the maze on the Pygame screen'''

        self.screen.fill(white)
        for i in range(n_rows):
            for j in range(n_cols):
                cell = self.cells[i][j]
                # Draw visited cells to see path exploration
                if cell.visited and not cell.inPath and not cell.highlighted:
                    pygame.draw.rect(self.screen, light_blue, pygame.Rect
                                     (cell.row * W, cell.col * W, W, W))

                # Original draw call
                cell.draw(self.screen)

        pygame.display.update()

    def maze_to_graph(self):
        '''Convert maze cells to a NetworkX graph'''

        # Nodes 
        G = nx.Graph()
        for i in range(n_rows):
            for j in range(n_cols):
                G.add_node((i, j))
        # Edges 
        for i in range(n_rows):
            for j in range(n_cols):
                cell = self.cells[i][j]
                # Top neighbor
                if cell.lines[0] is False and self.return_cell(i - 1, j):
                    G.add_edge((i, j), (i - 1, j), weight=1)
                # Right neighbor
                if cell.lines[1] is False and self.return_cell(i, j + 1):
                    G.add_edge((i, j), (i, j + 1), weight=1)
                # Bottom neighbor
                if cell.lines[2] is False and self.return_cell(i + 1, j):
                    G.add_edge((i, j), (i + 1, j), weight=1)
                # Left neighbor
                if cell.lines[3] is False and self.return_cell(i, j - 1):
                    G.add_edge((i, j), (i, j - 1), weight=1)
        return G

    def run(self):
        '''Run Dijkstra pathfinding algorithm'''

        # Create graph and set start/end nodes
        G = self.maze_to_graph()
        end = (n_rows - 1, n_cols - 1)
        start = (0, 0)

        # Dijkstra structures
        distances = {node: float("inf") for node in G.nodes}
        distances[start] = 0
        previous = {node: None for node in G.nodes}
        unvisited = set(G.nodes)

        last_highlighted = None

        # Find shortest path
        while unvisited:
            # Pick unvisited node with smallest distance
            current = min(unvisited, key=lambda node: distances[node])
            unvisited.remove(current)

            # Visit current node 
            row, col = current
            cell = self.cells[row][col]
            cell.visited = True

            # Un-highlight previous
            if last_highlighted:
                lr, lc = last_highlighted
                self.cells[lr][lc].highlighted = False
                self.cells[lr][lc].visited = True

            # Highlight current node 
            cell.highlighted = True
            last_highlighted = (row, col)

            # Draw frame 
            self.update_canvas()
            pygame.image.save(self.screen, f"./path_dijkstra_{self.frame_count:05d}.png")
            self.frame_count += 1

            if current == end:
                break

            # Relax edges
            for neighbor in G.neighbors(current):
                new_dist = distances[current] + 1
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current

if __name__ == "__main__":
    '''Run Dijkstra Pathfinder'''
    
    start_t = time.time()
    algo = DijkstraPathfinder()
    algo.run()
    end_t = time.time()
    print(f"Total Time: {end_t - start_t:.4f}s")
