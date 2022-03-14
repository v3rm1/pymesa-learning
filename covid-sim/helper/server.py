import math

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import NetworkModule
from mesa.visualization.modules import TextElement
from .model import Network, num_infected
from .state import State

def network_visual(graph):

    def node_color(agent):
        return {State.SUSCEPTIBLE: "#008000", State.INFECTED: "#FF0000"}.get(agent.state, "#808080")
    def edge_color(agent_1, agent_2):
        if State.RESISTANT in (agent_1.state, agent_2.state):
            return "#000000"
        return "#e8e8e8"

    def edge_width(agent_1, agent_2):
        if State.RESISTANT in (agent_1.state, agent_2.state):
            return 3
        return 2

    def get_agents(source, target):
        return graph.nodes[source]["agent"][0], graph.nodes[target]["agent"][0]

    visual = dict()
    visual["nodes"] = [
        {
            "size": 6,
            "color": node_color(agents[0]),
            "tooltip": f"id: {agents[0].unique_id}<br>state: {agents[0].state.name}",
        }
        for (_, agents) in graph.nodes.data("agent")
    ]

    visual["edges"] = [
        {
            "source": source,
            "target": target,
            "color": edge_color(*get_agents(source, target)),
            "width": edge_width(*get_agents(source, target)),
        }
        for (source, target) in graph.edges
    ]

    return visual


network = NetworkModule(network_visual, 500, 500, library="d3")
chart = ChartModule(
    [
        {"Label": "Infected", "Color": "#FF0000"},
        {"Label": "Susceptible", "Color": "#008000"},
        {"Label": "Resistant", "Color": "#808080"},
    ]
)


class MyTextElement(TextElement):
    def render(self, model):
        ratio = model.resistant_susceptible_ratio()
        ratio_text = "&infin;" if ratio is math.inf else f"{ratio:.2f}"
        infected_text = str(num_infected(model))

        return "Resistant/Susceptible Ratio: {}<br>Infected Remaining: {}".format(
            ratio_text, infected_text
        )


model_params = {
    "num_nodes": UserSettableParameter(
        "slider",
        "Number of agents",
        10,
        10,
        100,
        1,
        description="Choose how many agents to include in the model",
    ),
    "avg_node_degree": UserSettableParameter(
        "slider", "Avg Node Degree", 3, 3, 8, 1, description="Avg Node Degree"
    ),
    "initial_outbreak_size": UserSettableParameter(
        "slider",
        "Initial Outbreak Size",
        1,
        1,
        10,
        1,
        description="Initial Outbreak Size",
    ),
    "virus_spread_prob": UserSettableParameter(
        "slider",
        "Virus Spread Chance",
        0.4,
        0.0,
        1.0,
        0.1,
        description="Probability that susceptible neighbor will be infected",
    ),
    "virus_check_fqy": UserSettableParameter(
        "slider",
        "Virus Check Frequency",
        0.4,
        0.0,
        1.0,
        0.1,
        description="Frequency the nodes check whether they are infected by " "a virus",
    ),
    "recovery_prob": UserSettableParameter(
        "slider",
        "Recovery Chance",
        0.3,
        0.0,
        1.0,
        0.1,
        description="Probability that the virus will be removed",
    ),
    "gain_resistance_prob": UserSettableParameter(
        "slider",
        "Gain Resistance Chance",
        0.5,
        0.0,
        1.0,
        0.1,
        description="Probability that a recovered agent will become "
        "resistant to this virus in the future",
    ),
}

server = ModularServer(
    Network, [network, MyTextElement(), chart], "Virus Model", model_params
)
server.port = 8521

