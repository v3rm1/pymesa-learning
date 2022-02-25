def visualize_cell(cell):
    """
    This function is registered with the visualization server. Indicates how to draw the cell at a given time.
    
    Parameters
    ----------
    cell: 
        the cell in the simulation
    
    Returns
    -------
    dict
     Visualization portrayal dictionary.
    """
    assert cell is not None
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": cell.x,
        "y": cell.y,
        "Color": "black" if cell.is_alive else "white",
    }