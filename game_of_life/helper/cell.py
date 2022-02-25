from mesa import Agent


class Cell(Agent):
    """
    Represents a cell and its status in the simulation.
    """

    ALIVE = 1
    DEAD = 0

    def __init__(self, position, model, init_state=DEAD):
        """
        Initialize dead cell at a given position.
        """
        super().__init__(position, model)
        self.x, self.y = position
        self.state = init_state
        self._next_state = None
    
    @property
    def is_alive(self):
        """
        Check if cell state is alive.
        """
        return self.state == self.ALIVE

    @property
    def neighbors(self):
        return self.model.grid.neighbor_iter((self.x, self.y), True)
    
    def step(self):
        """
        Compute status of the cell at the next time step, based on the count of dead and alive neighbors.
        """
        live_neighbor_count = sum(neighbor.is_alive for neighbor in self.neighbors)
        
        self._next_state = self.state
        if self.is_alive:
            if live_neighbor_count < 2 or live_neighbor_count > 3:
                self._next_state = self.DEAD
        else:
            if live_neighbor_count == 3:
                self._next_state = self.ALIVE
            
    def advance(self):
        """
        Update the state to next state at each step.
        """
        self.state = self._next_state
        
