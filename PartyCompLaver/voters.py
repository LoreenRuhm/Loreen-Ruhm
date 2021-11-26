from mesa import Agent
import numpy as np

class Voters(Agent):
    """
    This class defines the agent type voter. 
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.agentType = "Voter"
        self.voterType = self.model.voterType[self.unique_id]
        
    def move(self):
        utilityVoter = np.sqrt(np.sum(np.array(([self.pos[0], self.pos[1]]) - self.model.posParty)**2,1))       # Proximity is calculated using the Euclidean norm.
        ind = np.random.choice([i for i, x in enumerate(utilityVoter) if x == np.min(utilityVoter)])
        self.model.votUtility[self.unique_id] = - utilityVoter[ind]**2
        if self.model.verSion == '2':       # Threshold for not voting
            if utilityVoter[ind] > self.model.voterThresh:
                self.model.posVoter[self.unique_id, 2] = 99                                                     # 99 means the voters does not chose one of the parties
            else:
                self.model.voterPoll[ind] = self.model.voterPoll[ind] + 1
                self.model.posVoter[self.unique_id, 2] = ind 
        else:
            self.model.voterPoll[ind] = self.model.voterPoll[ind] + 1                                           # Results of the voters poll is saved in voterPoll.
            self.model.posVoter[self.unique_id, 2] = ind                                                        # Voters' positions in posVoter.
            if self.model.verSion == '3':     # Optimzer
                for ii in range(self.model.num_Optimizer):
                    posInclOpt   = list(np.delete(self.model.posParty, ii + self.model.num_Optimizer - self.model.num_partyLeaders, axis=0)) + list(self.model.neighOpt[ii,:,:])
                    utilityVoter = np.sqrt(np.sum(np.array(([self.pos[0], self.pos[1]]) - np.array(posInclOpt))**2,1))
                    ind = np.random.choice([i for i, x in enumerate(utilityVoter) if x == np.min(utilityVoter)]) - self.model.num_partyLeaders + 1
                    if ind > -1:
                        self.model.neighOptpoll[ii, ind] = self.model.neighOptpoll[ii, ind] + 1
            if self.model.verSion == '4':
                self.model.voterPollweighted[ind] = self.model.voterPollweighted[ind] + self.model.voterWeighting[self.unique_id]
            
    def step(self):
        self.move()