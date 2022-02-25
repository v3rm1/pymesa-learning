from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import Grid
from .cell import Cell

class GoLGrid(Model):
    """
    Create the 2D grid of cells as defined in Conway's Game of Life.  
    """

    def __init__(self, height=50, width=50):
        """
        Initialize a Grid of dimensions height * width.
        Initialize scheduler for updating grid and agent state.
        """

        self.schedule = SimultaneousActivation(self)

        self.grid = Grid(height, width, torus=True)

        for (contents, x, y) in self.grid.coord_iter():
            cell = Cell((x, y), self)
            if self.random.random() < 0.1:
                cell.state = cell.ALIVE
            self.grid.place_agent(cell, (x, y))
            self.schedule.add(cell)
        
        self.running = True

    def step(self):
        """
        Advance each cell by one step using scheduler.
        """
        self.schedule.step()
    