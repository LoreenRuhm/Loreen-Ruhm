from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .portrayal import portrayPartyCompetition
from .Model import PartyComp

sizeGrid  = 100

# Visualization of the 2D political space on a grid
canvas_element = CanvasGrid(portrayPartyCompetition, sizeGrid, sizeGrid, 1000, 1000)

# The parameters of the model
model_params = {
    "M": UserSettableParameter("slider", "Number of Voters", 200, 1, 1000, 1),
	"sizeGrid": sizeGrid,
    "N_Sticker": UserSettableParameter("slider", "Number of Sticker", 2, 0, 20, 1),
    "N_Hunter": UserSettableParameter("slider", "Number of Hunter", 0, 0, 20, 1),
    "N_Aggregator": UserSettableParameter("slider", "Number of Aggregator", 0, 0, 20, 1),
    "N_Predator": UserSettableParameter("slider", "Number of Predator", 0, 0, 20, 1),
    "verSion":  UserSettableParameter("choice", "Version", value='1', choices=["1","2","3","4"]),
    "voterThresh": UserSettableParameter("slider", "Threshold Voters (works only in version 2!)", 10, 1, 50, 1),
    "N_Optimizer": UserSettableParameter("slider", "Number of Optimizer (works only in version 3!)", 0, 0, 20, 1),
    "M_Lobbyist": UserSettableParameter("slider", "Number of Lobbyists (works only in version 4!)", 0, 0, 20, 1),
    "M_PartyMember": UserSettableParameter("slider", "Percentage of party members (works only in version 4!)", 0.0, 0, 1, 0.01)
    
}

server = ModularServer(
    PartyComp, [canvas_element], "PartyCompLaver", model_params)
