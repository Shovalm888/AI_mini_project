from agent import Agent

class AgentA(Agent):
    
    def __init__(self, size, color):
        super().__init__(size, color)


    def _mini_max(self, iter, A_agents, E_agents):
        pass


    def _update_rewards(self, cost_point, rew_point, points, dist, axis_len):
    
        indexOf = lambda part : points.index(list(filter(lambda var : var[:2] == part , points))[0]) 
        reward = lambda distance :  axis_len - abs(distance)
        
        try:
            points[indexOf(rew_point)][2] += reward(dist)
        except:
            pass
        try:
            points[indexOf(cost_point)][2] -= reward(dist)
        except:
            pass


    def automatic_movement(self, E_agents, A_agents):
        
        forbidden_points = []
        for agent in E_agents:
            forbidden_points += agent.get_pos()
        forbidden_points += self._pos[:-2] + self._pos[:1]

        allowed_points = self._possible_moves(forbidden_points)
        
        pass