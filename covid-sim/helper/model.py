import math
import networkx as nwx

from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid

from .state import State
from .agent import VirusAgent



def num_state(model, state):
    return sum(1 for cell_cont in model.grid.get_all_cell_contents() if cell_cont.state is state)

def num_susceptible(model):
    return num_state(model, State.SUSCEPTIBLE)

def num_resistant(model):
    return num_state(model, State.RESISTANT)

def num_infected(model):
    return num_state(model, State.INFECTED)

class Network(Model):
    """
    Network model simulating viral vector transmission.
    """

    def __init__(
        self,
        num_nodes=10,
        avg_node_degree=4,
        initial_outbreak_size=2,
        virus_spread_prob=0.4,
        virus_check_fqy=0.5,
        recovery_prob=0.3,
        gain_resistance_prob=0.3
    ) -> None:
        self.num_nodes = num_nodes
        node_conn_prob = avg_node_degree/self.num_nodes
        self.G = nwx.erdos_renyi_graph(n=self.num_nodes, p=node_conn_prob)
        self.grid = NetworkGrid(self.G)
        self.schedule = RandomActivation(self)
        self.init_outbreak_size = (initial_outbreak_size if initial_outbreak_size <= num_nodes else num_nodes)
        self.virus_spread_prob = virus_spread_prob
        self.virus_check_fqy = virus_check_fqy
        self.recovery_prob = recovery_prob
        self.gain_resistance_prob = gain_resistance_prob

        self.datacollector = DataCollector(
            {
                "Susceptible": num_susceptible,
                "Infected": num_infected,
                "Resistant": num_resistant,
            }
        )
        for i, node in enumerate(self.G.nodes()):
            agent = VirusAgent(
                i,
                self,
                State.SUSCEPTIBLE,
                self.virus_spread_prob,
                self.virus_check_fqy,
                self.recovery_prob,
                self.gain_resistance_prob,
            )
            # Add agent to scheduler
            self.schedule.add(agent)
            # Add agent to graph
            self.grid.place_agent(agent, node)

        # Infect some nodes (random sampling)
        infected_nodes = self.random.sample(self.G.nodes(), self.init_outbreak_size)
        for agent in self.grid.get_cell_list_contents(infected_nodes):
            agent.state = State.INFECTED
        
        # Set run and collect data
        self.running = True
        self.datacollector.collect(self)
    
    def resistant_susceptible_ratio(self) -> float:
        try:
            return num_state(self, State.RESISTANT) / num_state(self, State.SUSCEPTIBLE)
        except ZeroDivisionError:
            return math.inf

    def step(self) -> None:
        # Set run and collect data
        self.schedule.step()
        self.datacollector.collect(self)

    def run_model(self, n_steps) -> None:
        for i in range(n_steps):
            self.step()
