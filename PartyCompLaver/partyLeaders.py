from mesa import Agent
import numpy as np

class PartyLeaders(Agent):
    """
    This class defines the agent type politcal leader. 
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.agentType = "PartyLeader"
        self.decRule   = self.model.decRule[self.unique_id - self.model.num_voters]
        
    def move(self):
        '''
        Defines the behavior of each party leader.
        '''
        if self.unique_id == self.model.num_voters:
            self.model.posWinner = []
            self.model.indWinner = [i for i, x in enumerate(self.model.voterPoll) if x == np.max(self.model.voterPoll)]
            for i in self.model.indWinner:
                self.model.posWinner.append(self.model.posParty[i,:])                               # Position of the winner in each circle
               
        if self.model.decRule[self.unique_id - self.model.num_voters] == 'Sticker':
            return
        
        elif self.model.decRule[self.unique_id - self.model.num_voters] == 'Hunter':
            if self.model.cycle == 1:                                                               # First cicle: Hunter moves to a random cell
                neighbors   = self.model.grid.get_neighborhood(self.pos, True)
                neighbors   = [x for x in neighbors if np.sum(np.abs(np.array(x) - np.array(self.pos))) < 3] 
                self.newPos = neighbors[np.random.randint(0,len(neighbors))]
                self.model.dPos[self.unique_id - self.model.num_voters,:] = np.array(self.newPos) - np.array(self.pos)         # Save Hunters' step
                self.model.grid.move_agent(self, self.newPos)
                
            else:
                if self.model.verSion == '4':
                    dPolls = self.model.voterPollweighted[self.unique_id - self.model.num_voters] - self.model.voterPollweightedLast[self.unique_id  - self.model.num_voters] 
                else:
                    dPolls = self.model.voterPoll[self.unique_id - self.model.num_voters] - self.model.voterPollLast[self.unique_id  - self.model.num_voters]
                if dPolls > 0:      
                    self.newPos = np.array(self.pos) + self.model.dPos[self.unique_id - self.model.num_voters,:]
                    if not self.model.grid.out_of_bounds(self.newPos):
                        self.model.grid.move_agent(self, (int(self.newPos[0]), int(self.newPos[1])))                            
                else:
                    neighbors   = self.model.grid.get_neighborhood(self.pos, True)
                    self.oldDir = np.array(self.pos) + self.model.dPos[self.unique_id - self.model.num_voters,:]
                    dNeighbors  = self.model.grid.get_neighborhood((int(self.oldDir[0]),int(self.oldDir[1])), True, True)
                    neighbors   = [x for x in neighbors if x in neighbors and x not in dNeighbors]
                    neighbors   = [x for x in neighbors if np.sum(np.abs(np.array(x) - np.array(self.pos))) < 3] 
                    self.newPos = neighbors[np.random.randint(0,len(neighbors))]
                    self.model.dPos[self.unique_id - self.model.num_voters,:] = np.array(self.newPos) - np.array(self.pos)
                    self.model.grid.move_agent(self, self.newPos)
                    
        elif self.model.decRule[self.unique_id - self.model.num_voters] == 'Aggregator':
            if self.model.verSion == '4':
                posVoter         = np.ones([self.model.num_voters,3])       
                posVoter[:,0:2]  = self.model.posVoter[:,0:2]
                posVoter[self.model.posVoter[:,2] != (self.unique_id - self.model.num_voters)] = 0
                newPos    = np.zeros(2)
                newPos[0] = np.sum((self.model.voterWeighting * posVoter[:,0])/np.sum(self.model.voterWeighting*posVoter[:,2]))
                newPos[1] = np.sum((self.model.voterWeighting * posVoter[:,1])/np.sum(self.model.voterWeighting*posVoter[:,2]))
            else:
                newPos = np.mean(self.model.posVoter[self.model.posVoter[:,2] == (self.unique_id - self.model.num_voters)][:,0:2],0)
            if not np.isnan(newPos[0]):
                self.model.grid.move_agent(self, (int(newPos[0]), int(newPos[1])))
                    
        elif self.model.decRule[self.unique_id - self.model.num_voters] == 'Predator':
            if (self.unique_id - self.model.num_voters) not in self.model.indWinner:
                self.dPos = np.array(self.model.posWinner) - np.array(self.pos)
                self.dPos = self.dPos[np.argmin(np.linalg.norm(self.dPos, 2, 1)),:]
                self.dPos = np.rint(self.dPos/np.linalg.norm(self.dPos)).astype(int)
                self.newPos = np.array(self.pos) + self.dPos
                self.model.grid.move_agent(self, (self.newPos[0], self.newPos[1])) 
                
        elif self.model.decRule[self.unique_id - self.model.num_voters] == 'Optimizer':
            poll = self.model.neighOptpoll[self.unique_id - self.model.num_voters - self.model.num_partyLeaders + self.model.num_Optimizer,:]
            ind  = np.random.choice([i for i, x in enumerate(poll) if x == np.max(poll)]) 
            pos  = self.model.neighOpt[self.unique_id - self.model.num_voters - self.model.num_partyLeaders + self.model.num_Optimizer, ind, :]
            self.model.grid.move_agent(self, (int(pos[0]), int(pos[1])))
            self.model.neighOpt[self.unique_id - self.model.num_voters - self.model.num_partyLeaders + self.model.num_Optimizer, :, :] = self.model.grid.get_neighborhood(self.pos, True, True)
            
        self.model.posParty[self.unique_id - self.model.num_voters,0] = self.pos[0]
        self.model.posParty[self.unique_id - self.model.num_voters,1] = self.pos[1]
            
        
    def step(self):
        self.move()