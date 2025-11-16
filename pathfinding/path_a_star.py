'''Pathfinding with A* Algorithm'''

# Import configs, classes, and libraries 
from utils.config import W, maze_width, n_rows, n_cols, white, red, light_blue 
from utils.cell import Cell
import networkx as nx
import pygame
import time
import pickle

# A* Pathfinder Class
class AStarPathfinder:
    def __init__(self):
        '''Initialize Pygame, load maze, and reset cell states'''

        # Setup Pygame 
        pygame.init()
        self.screen = pygame.display.set_mode((maze_width, maze_width))
        pygame.display.set_caption("A* Pathfinding")

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

    @staticmethod
    def heuristic(current, goal):
        '''Manhattan distance heuristic'''
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def run(self):
        '''Run A* pathfinding algorithm'''

        # Create graph and set start/end nodes
        G = self.maze_to_graph()
        end = (n_rows - 1, n_cols - 1)
        start = (0, 0)

        # A* structures
        g_score = {node: float("inf") for node in G.nodes}
        g_score[start] = 0
        f_score = {node: float("inf") for node in G.nodes}
        f_score[start] = self.heuristic(start, end)
        open_set = [start]
        previous = {node: None for node in G.nodes}

        last_highlighted = None

        # Find shortest path
        while open_set:
            # Sort open set by f_score and get lowest
            open_set.sort(key=lambda node: f_score[node])
            current = open_set.pop(0)

            # Visit current node
            row, col = current
            cell = self.cells[row][col]
            cell.visited = True

            # Un-highlight previous cell 
            if last_highlighted:
                lr, lc = last_highlighted
                self.cells[lr][lc].highlighted = False
                self.cells[lr][lc].visited = True

            # Highlight current node
            cell.highlighted = True
            last_highlighted = (row, col)

            # Draw frame
            self.update_canvas()
            pygame.image.save(self.screen, f"./path_astar_{self.frame_count:05d}.png")
            self.frame_count += 1

            if current == end:
                break

            # Explore neighbors of current node
            for neighbor in G.neighbors(current):
                temp_g = g_score[current] + G[current][neighbor]["weight"]

                # Update scores if better path found
                if temp_g < g_score[neighbor]:
                    g_score[neighbor] = temp_g
                    f_score[neighbor] = temp_g + self.heuristic(neighbor, end)
                    previous[neighbor] = current

                    # Add neighbor if not already present
                    if neighbor not in open_set:
                        open_set.append(neighbor)

        # Reconstruct path 
        path, node = [], end
        while node is not None:
            row, col = node
            path.append(self.cells[row][col])
            node = previous[node]
        path.reverse()

        # Mark actual path
        for cell in path:
            cell.inPath = True

        self.update_canvas()

        # Prepare line points 
        line_points = []
        for cell in path:
            x = cell.row * W + W // 2
            y = cell.col * W + W // 2
            line_points.append((x, y))

        # Draw and save red polyline for solution
        if len(line_points) > 1:
            pygame.draw.lines(self.screen, red, False, line_points, 3)
        pygame.display.update()
        pygame.image.save(self.screen, "./a_star_solution.png")

        return path

if __name__ == "__main__":
    '''Run A* Pathfinder'''
    
    start_t = time.time()
    algo = AStarPathfinder()
    algo.run()
    end_t = time.time()
    print(f"Total Time: {end_t - start_t:.4f}s")