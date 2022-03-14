from enum import Enum

class State(Enum):
    # Based on the SIR model of disease propagation
    SUSCEPTIBLE = 0
    INFECTED = 1
    RESISTANT = 2