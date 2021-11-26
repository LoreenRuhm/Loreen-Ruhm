from mesa import Model
from mesa.time import BaseScheduler
from mesa.space import MultiGrid
import numpy as np

from .partyLeaders import PartyLeaders
from .voters import Voters

class PartyComp(Model):
    """
    This class defines the model including all versions presented in the thesis.
    """
    def __init__(self, M, sizeGrid, N_Sticker, N_Hunter, N_Aggregator, N_Predator, verSion, voterThresh, N_Optimizer, M_Lobbyist, M_PartyMember):
        if verSion == '3':
            self.num_Optimizer    = N_Optimizer                                                     # Number Optimizer
        else:
            N_Optimizer = 0
            self.num_Optimizer    = N_Optimizer
        
        self.num_partyLeaders = N_Sticker + N_Hunter + N_Aggregator + N_Predator + N_Optimizer      # Number party leader
        
        if verSion == '4':
            self.num_Lobbyist     = M_Lobbyist
            self.num_PartyMember  = int(M_PartyMember*M)
            self.voterWeighting   = np.zeros(M)
            self.voterWeighting[0:M_Lobbyist]                                   = 100.0             # Weighting for version 4
            self.voterWeighting[M_Lobbyist:(M_Lobbyist + self.num_PartyMember)] = 5.0
            self.voterWeighting[(M_Lobbyist + self.num_PartyMember):M]          = 1.0
            self.voterPollweighted     = np.zeros(self.num_partyLeaders)                            # Voters' poll weighted
            self.voterPollweightedLast = np.zeros(self.num_partyLeaders)   
        else:
            self.num_Lobbyist     = 0
            self.num_PartyMember  = 0

        self.num_voters       = M                                                                   # Number voters
        self.sizeGrid         = sizeGrid                                                            # Size of the grid
        self.grid             = MultiGrid(self.sizeGrid, self.sizeGrid, True)                       # Each cell can be occupied by several agents
        self.voterType        = []                                                                  # Type of voter (version 4)
        self.decRule          = []                                                                  # Decision rules per party leader
        self.voterPoll        = np.zeros(self.num_partyLeaders)                                     # Results of the voters' poll
        self.posParty         = np.zeros((self.num_partyLeaders,2))                                 # Position party leader 
        self.posVoter         = np.zeros((M,3))                                                     # Position voter and favorite party leader
        self.cycle            = 1                                                                   # Count circles 
        self.posWinner        = []                                                                  # Position of the winner(s) 
        self.indWinner        = []                                                                  # Index of the winner(s)
        self.neighOpt         = np.zeros((self.num_Optimizer, 9, 2))                                # Neighborhood of the Optimizer
        self.neighOptpoll     = np.zeros((self.num_Optimizer, 9))                                   # Potential votes for each neighbor for Optimizer
        self.dPos             = np.zeros((self.num_partyLeaders,2))                                 # Change of party leader position in each step
        self.verSion          = verSion                                                             # Version of the model (1=original model by Laver)
        self.votUtility       = np.zeros(M)                                                         # Voters utility
        if verSion == '2':
            self.voterThresh      = voterThresh                                                     # Threshold version 2 
        else:
            self.voterThresh = 100
        self.schedule         = BaseScheduler(self)                                                 # Voters move first, afterwards the party leaders 
        
        mean_pos = sizeGrid/2                    # Mean Gaussian distribution
        std_pos  = sizeGrid/6                    # Standard deviation 
        
        # Create voters
        for j in range(self.num_voters):
            if j < self.num_Lobbyist:
                self.voterType.append('Lobbyist')
            elif j < (self.num_Lobbyist + self.num_PartyMember):
                self.voterType.append('PartyMember')
            else:
                self.voterType.append('normalVoter')
            x = int(np.random.normal(mean_pos, std_pos))
            y = int(np.random.normal(mean_pos, std_pos))
            while self.grid.out_of_bounds((x,y)):
                x = int(np.random.normal(mean_pos, std_pos))
                y = int(np.random.normal(mean_pos, std_pos))
            a = Voters(j, self)
            self.grid.place_agent(a, (x,y))
            self.posVoter[j,0] = x
            self.posVoter[j,1] = y
            self.schedule.add(a)
            
        
        # Create political leaders
        for i in range(N_Sticker):
            x = int(np.random.normal(mean_pos, std_pos))
            y = int(np.random.normal(mean_pos, std_pos))
            while self.grid.out_of_bounds((x,y)):
                x = int(np.random.normal(mean_pos, std_pos))
                y = int(np.random.normal(mean_pos, std_pos))
            self.decRule.append('Sticker')
            a = PartyLeaders(i+M, self)
            cellCont = self.grid.get_cell_list_contents((x,y))
            if cellCont:                                                # only one political leader per cell
                while (cellCont[0].agentType == "PartyLeader"):
                    x = self.random.randrange(self.grid.width)
                    y = self.random.randrange(self.grid.height)
                    cellCont = self.grid.get_cell_list_contents((x,y))
                    if not cellCont:
                        break
            self.posParty[i,0] = x
            self.posParty[i,1] = y
            self.grid.place_agent(a, (x,y))
            self.schedule.add(a)
            
        for i in range(N_Hunter):
            x = int(np.random.normal(mean_pos, std_pos))
            y = int(np.random.normal(mean_pos, std_pos))
            while self.grid.out_of_bounds((x,y)):
                x = int(np.random.normal(mean_pos, std_pos))
                y = int(np.random.normal(mean_pos, std_pos))
            self.decRule.append('Hunter')
            a = PartyLeaders(i + N_Sticker + M, self)
            cellCont = self.grid.get_cell_list_contents((x,y))
            if cellCont:
                while (cellCont[0].agentType == "PartyLeader"):
                    x = self.random.randrange(self.grid.width)
                    y = self.random.randrange(self.grid.height)
                    cellCont = self.grid.get_cell_list_contents((x,y))
                    if not cellCont:
                        break
            self.posParty[i + N_Sticker,0] = x
            self.posParty[i + N_Sticker,1] = y
            self.grid.place_agent(a, (x,y))
            self.schedule.add(a)
            
        for i in range(N_Aggregator):
            x = int(np.random.normal(mean_pos, std_pos))
            y = int(np.random.normal(mean_pos, std_pos))
            while self.grid.out_of_bounds((x,y)):
                x = int(np.random.normal(mean_pos, std_pos))
                y = int(np.random.normal(mean_pos, std_pos))
            self.decRule.append('Aggregator')
            a = PartyLeaders(i+ N_Sticker + N_Hunter + M, self)
            cellCont = self.grid.get_cell_list_contents((x,y))
            if cellCont:
                while (cellCont[0].agentType == "PartyLeader"):
                    x = self.random.randrange(self.grid.width)
                    y = self.random.randrange(self.grid.height)
                    cellCont = self.grid.get_cell_list_contents((x,y))
                    if not cellCont:
                        break
            self.posParty[i + N_Sticker + N_Hunter,0] = x
            self.posParty[i + N_Sticker + N_Hunter,1] = y
            self.grid.place_agent(a, (x,y))
            self.schedule.add(a)
            
        for i in range(N_Predator):
            x = int(np.random.normal(mean_pos, std_pos))
            y = int(np.random.normal(mean_pos, std_pos))
            while self.grid.out_of_bounds((x,y)):
                x = int(np.random.normal(mean_pos, std_pos))
                y = int(np.random.normal(mean_pos, std_pos))
            self.decRule.append('Predator')
            a = PartyLeaders(i + N_Sticker + N_Hunter + N_Aggregator + M, self)
            cellCont = self.grid.get_cell_list_contents((x,y))
            if cellCont:
                while (cellCont[0].agentType == "PartyLeader"):
                    x = self.random.randrange(self.grid.width)
                    y = self.random.randrange(self.grid.height)
                    cellCont = self.grid.get_cell_list_contents((x,y))
                    if not cellCont:
                        break
            self.posParty[i  + N_Sticker + N_Hunter + N_Aggregator,0] = x
            self.posParty[i  + N_Sticker + N_Hunter + N_Aggregator,1] = y
            self.grid.place_agent(a, (x,y))
            self.schedule.add(a)
            
        if self.verSion == '3':    
            for i in range(N_Optimizer):
                x = int(np.random.normal(mean_pos, std_pos))
                y = int(np.random.normal(mean_pos, std_pos))
                while self.grid.out_of_bounds((x,y)):
                    x = int(np.random.normal(mean_pos, std_pos))
                    y = int(np.random.normal(mean_pos, std_pos))
                self.decRule.append('Optimizer')
                a = PartyLeaders(i + N_Sticker + N_Hunter + N_Aggregator + N_Predator + M, self)
                cellCont = self.grid.get_cell_list_contents((x,y))
                if cellCont:
                    while (cellCont[0].agentType == "PartyLeader"):
                        x = self.random.randrange(self.grid.width)
                        y = self.random.randrange(self.grid.height)
                        cellCont = self.grid.get_cell_list_contents((x,y))
                        if not cellCont:
                            break
                self.posParty[i  + N_Sticker + N_Hunter + N_Aggregator + N_Predator,0] = x
                self.posParty[i  + N_Sticker + N_Hunter + N_Aggregator + N_Predator,1] = y
                self.grid.place_agent(a, (x,y))
                self.schedule.add(a)
                self.neighOpt[i, :, :] = self.grid.get_neighborhood((x,y), True, True)
            
        self.running = True

    def step(self):
        self.neighOptpoll     = np.zeros((self.num_Optimizer, 9))  
        self.schedule.step()
        self.voterPollLast    = self.voterPoll
        self.voterPoll        = np.zeros(self.num_partyLeaders)
        if self.verSion == '4':
            self.voterPollweightedLast    = self.voterPollweighted
            self.voterPollweighted        = np.zeros(self.num_partyLeaders)
        self.cycle            = self.cycle + 1
