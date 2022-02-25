from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from .visualize import visualize_cell
from .model import GoLGrid



canvas_element = CanvasGrid(visualize_cell, 50, 50, 250, 250)

server = ModularServer(
    GoLGrid, [canvas_element], "Game of Life", {"height": 50, "width": 50}
)