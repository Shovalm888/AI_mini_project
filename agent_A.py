from agent import Agent
from globals import gl
from math import sqrt

class AgentA(Agent):
    
    def __init__(self, size, color):
        super().__init__(size, color)


    def automatic_movement(self, A_agents, E_agents):    
        forbidden_points = self._get_agents_points(E_agents + A_agents, self)
        allowed_points, rew = self._possible_moves(forbidden_points)
        allowed_points = [point + [r] for point , r in zip(allowed_points, rew)]
        a_agents_without_self = [ agent for agent in A_agents if agent != self]
        recomended = self.minimax(a_agents_without_self, E_agents)
        # return the index in allowed point of the point that the first two vars equals to 'part'
        indexOf = lambda part : allowed_points.index(list(filter(lambda var : var[:2] == part , allowed_points))[0])
        for point in recomended:  
            allowed_points[indexOf(point[:2])][2] += point[2]

        allowed_points = sorted(allowed_points, key = lambda x : x[2] , reverse= True)
        point = allowed_points.pop(0)
        self.move_forward(point[:2], point[2])


    



    def create_scenarios(self, scenarios , agents_allowed_points, one_scenario = [], iter = 0):
        """Gets nested list that each cell contain a list of the possible heads for some agent.\n
        Returns in scenarios a list that each cell contains a possible scenario
        of the progress of all the agents without collisions"""
        # agents_allowed_points length represents the number of agent and iter used for indexing
        if iter == len(agents_allowed_points):
            scenarios.append(one_scenario.copy())
            return

        for point in agents_allowed_points[iter]:
            if point not in one_scenario:
                one_scenario.append(point)
                self.create_scenarios(scenarios, agents_allowed_points, one_scenario, iter + 1)
                one_scenario.pop()


    def minimax(self, A_agents, E_agents, iter = 0):
        """ Return list of allowed head and rewards based on mini_max algorithm """
        # Calculate possible heads
        agents = A_agents + E_agents
        forbidden = self._get_agents_points( agents )
        self_heads, rew = self._possible_moves(forbidden, allowed_neg_rew= False)
        self_heads = [point + [r] for point , r in zip(self_heads, rew)]  # bound each point to its reward
        
        if iter == gl.Tree_Depth:
                self._calculate_avg_heads_dis(self_heads, E_agents ) # Updates self_heads rewards
                return self_heads

    
        # Calculate possible scenarios
        agents_allowed_points = []
        for agent in agents:
            forbidden = agent._get_agents_points( agents )
            agent_heads, rew = agent._possible_moves(forbidden, allowed_neg_rew= False)
            agents_allowed_points.append([point + [r] for point , r in zip(agent_heads, rew)])
        scenarios = []
        self.create_scenarios(scenarios, agents_allowed_points)
        # Main loop: illustrate the future possible moves on the board
        take_min = gl.BIG_DIS
        for self_head in self_heads:
            # Move forward self agent
            self.move_forward(self_head[:2], self_head[2])
            take_min = gl.BIG_DIS
            for scenario in scenarios:
                skip = False
                # Check if in this scenario self agent will be bitten
                for point in self.get_pos():
                    if point in scenario:
                        take_min = gl.FORBIDDEN
                        skip = True
                        break

                if skip == False: 
                    # Move forward the rest agents
                    for new_head, agent in zip(scenario, agents):
                        agent.move_forward(new_head[:2], new_head[2])
                    # Recursive call
                    heads_ = self.minimax(A_agents, E_agents, iter + 1)
                    val = self.extract_max(heads_)
                    # Restore agents positions
                    for  agent in  agents:
                        agent.move_backward()

                    if val < take_min:
                        take_min = val

            # Restore self agent
            self.move_backward()
            self_heads[self_heads.index(self_head)][2] = take_min
        return self_heads
        

    def extract_max(self, heads):
        """Gets nested list [[point, reward],...] and return the max reward in the list"""
        max_rew = gl.FORBIDDEN
        for head in heads:
            if head[2] > max_rew:
                max_rew = head[2]
        return max_rew

    
    def _calculate_avg_heads_dis(self, self_heads, E_agents):
        """Gets self possible heads and calculate for each one illustrate agent
        movement and call to _calculate_avg_dis"""
        for head in self_heads :  # for each self possible head
            self.move_forward(head[:2], head[2])
            if len(E_agents) > 0:
                self_heads[self_heads.index(head)][2] += self._calculate_avg_dis(E_agents)
            self.move_backward()
        return self_heads


    def _calculate_avg_dis(self, E_agents):
        """Gets list of agents from type E and calculate the
        average distance between their heads to each point of self agent"""
        sum_dis = 0
        for agent in E_agents:
            agent_head = agent.get_pos()[0]
            for point in self.get_pos():
                sum_dis += abs(agent_head[0] - point[0]) + abs(agent_head[1] - point[1])
        
        if len(E_agents) == 0:
            return gl.BIG_DIS
        return sum_dis / (len(E_agents) * self.get_size())
        