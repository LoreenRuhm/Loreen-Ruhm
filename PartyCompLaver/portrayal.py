def portrayPartyCompetition(agent):
    """
    This function is registered with the visualization server to be called
    each tick to indicate how to draw the cell in its current state.
    :param agent:  the agent in the simulation
    :return: the portrayal dictionary.
    """
    assert agent is not None
    if agent.agentType == "PartyLeader":
        if agent.decRule == "Sticker":
            return {
                "Shape": "circle",
                "r": 0.8,
                "Filled": "true",
                "Layer": 0,
                "x": agent.pos[0],
                "y": agent.pos[1],
                "Color": '#d70000'
                }
        elif agent.decRule == "Hunter":
            return {
                "Shape": "circle",
                "r": 0.8,
                "Filled": "true",
                "Layer": 0,
                "x": agent.pos[0],
                "y": agent.pos[1],
                "Color": "#009292"
                }
        elif agent.decRule == "Aggregator":
            return {
                "Shape": "circle",
                "r": 0.8,
                "Filled": "true",
                "Layer": 0,
                "x": agent.pos[0],
                "y": agent.pos[1],
                "Color": "#870087"
                }
        elif agent.decRule == "Predator":
            return {
                "Shape": "circle",
                "r": 0.8,
                "Filled": "true",
                "Layer": 0,
                "x": agent.pos[0],
                "y": agent.pos[1],
                "Color": '#d75f00'
                }
        elif agent.decRule == "Optimizer":
            return {
                "Shape": "circle",
                "r": 0.8,
                "Filled": "true",
                "Layer": 0,
                "x": agent.pos[0],
                "y": agent.pos[1],
                "Color": '#c20078'
                }
    else:
        if agent.voterType == "Lobbyist":
            return {
                "Shape": "circle",
                "r": 0.8,
                "Filled": "true",
                "Layer": 0,
                "x": agent.pos[0],
                "y": agent.pos[1],
                "Color": '#00005f'
                }
        elif agent.voterType == "PartyMember":
            return {
                "Shape": "circle",
                "r": .5,
                "Filled": "true",
                "Layer": 0,
                "x": agent.pos[0],
                "y": agent.pos[1],
                "Color": '#00005f'
                }
        else:
            return {
                "Shape": "circle",
                "r": .2,
                "Filled": "true",
                "Layer": 0,
                "x": agent.pos[0],
                "y": agent.pos[1],
                "Color": '#00005f'
                }
