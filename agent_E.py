from agent import Agent
import random as rand


class AgentE(Agent):

    def __init__(self, size, color):
        super().__init__(size, color)    

        

    def automatic_movement(self, A_agents, E_agents):
        """ Promotes E agent one step forward automatically """
        # collects forbidden points:
        forbidden_points = self._get_agents_points(E_agents)
        forbidden_points += self._pos[:-1]
        # composes allowed points with their rewards:
        allowed_points, rew = self._possible_moves(forbidden_points)
        allowed_points = [point + [r] for point , r in zip(allowed_points, rew)]
        # add reward base on the distance from A_agents for each allowed point
        self._heuristic_search(allowed_points, A_agents)
        rand.shuffle(allowed_points)
        allowed_points = sorted(allowed_points, key = lambda x : x[2], reverse=True)
        point = allowed_points.pop(0)
        self.move_forward(point[:2], point[2])
   
   
    def _heuristic_search(self, allowed_points,  agents):
        """returns a list of allowed points with updated rewards based on the 
        length from the objects in 'agent' variable """
        if len(agents) == 0:
            return allowed_points
        
        head = self._pos[0]
        avg_dist = []
        agents_points = []   
        for agent in agents:
            sum = 0
            for point in agent.get_round_pos():
                sum += abs(head[0] - point[0]) + abs(head[1] - point[1]) # sums the distance from self head to each agent's point
            
            avg_dist.append(sum / agent.get_size())
            agents_points += agent.get_round_pos()
        for point in agents[avg_dist.index(min(avg_dist))].get_round_pos(): 
            x_dist = head[0] - point[0]
            y_dist = head[1] - point[1]
            
            # Gives positive rewards to allowed points that gets the agent closer to his goal
            # and negative to opposite points
            if x_dist > 0: # The goal is located on the left
                self._update_rewards([head[0]-1, head[1]], [head[0] + 1, head[1]],
                 allowed_points,x_dist )
            else:          # The goal is located on the right
                self._update_rewards( [head[0] + 1, head[1]], [head[0]-1, head[1]],
                 allowed_points,x_dist )
            if y_dist > 0: # The goal is located above
                self._update_rewards([head[0], head[1] - 1], [head[0], head[1] + 1],
                 allowed_points,y_dist )
            else:          # The goal is located bellow
                self._update_rewards([head[0], head[1] + 1], [head[0], head[1] - 1],
                 allowed_points,y_dist )
        
        return allowed_points
        
        
        

 
    def _update_rewards(self, rew_point, cost_point, points, dist):
        """Gets two points, points list and distance and updates the specific points in
        the points list based on the distance"""
        indexOf = lambda part : points.index(list(filter(lambda var : var[:2] == part , points))[0]) 
        reward = lambda distance :  abs(distance)
        
        try:
            points[indexOf(rew_point)][2] += reward(dist)
        except:
            pass
        try:
            points[indexOf(cost_point)][2] -= reward(dist)
        except:
            pass

