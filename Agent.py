from agent_A import AgentA
from agent_E import AgentE
from globals import gl, possible_points
import random as rand
from miniMax import MiniMax


class Agent:

    def __init__(self, size, color):
        
        self._pos = []
        self._tails = []
        self._rewards = []
        self._size = size
        self._head_color = color['head']
        self._body_color = color['body']
        self._board_height = int(gl.BOARD_HEIGHT / gl.DOT_SIZE) - gl.BOARD_PADDING
        self._board_width = int(gl.BOARD_WIDTH / gl.DOT_SIZE) - gl.BOARD_PADDING
        self._status = False  # indicate if the position already updated for the current round
        self._id = gl.SERIAL_NUM
        gl.SERIAL_NUM += 1

    def get_pos(self):
        return self._pos

    def get_round_pos(self):

        if self._status: # alreay updated
            return self._pos[1:] + [self._tails[-1]]

        return self._pos

    
    def get_status(self):
        return self._status

    def get_head_color(self):
        return self._head_color

    def get_body_color(self):
        return self._body_color

    def get_id(self):
        return self._id

    def get_reward(self):
        return sum(self._rewards)

    def get_size(self):
        return self._size

    def _add_reward(self, amount):
        self._rewards.append(amount)
    
    def _sub_reward(self, amount):
        if len(self._rewards) == 0:
            return False
        return self._rewards.pop()
    
    def change_status(self, state):
        self._status = True if state else False

    def set_on_board_randomly(self, forbidden_points = [], max_attempts = 20):

        rand_head = lambda : [rand.randint(0, self._board_width - 1), rand.randint(0, self._board_height - 1)]
        all_set = False

        while all_set == False:
            if max_attempts <= 0:
                return False
            point = rand_head()
            while point in forbidden_points:
                point = rand_head
            self._pos = [point]
            all_set = self._set_on_board_the_rest( 1, forbidden_points + self._pos)
            max_attempts -= 1
                   

    def _set_on_board_the_rest(self, iter , forbidden_points):

        new_points, rewards = self._possible_moves(forbidden_points)
        allowed_points = [point+[rew] for point, rew in zip(new_points, rewards) if rew > gl.FORBBIDEN]

        if len(allowed_points) == 0:
            return False

        rand.shuffle(allowed_points)
        all_set = False

        while len(allowed_points) > 0 and all_set == False:
            self._pos.insert(0, allowed_points.pop())
            all_set = self.set_on_board_randomly(iter + 1, forbidden_points + self._pos)

        return all_set


    def _set_on_board_by_points(self, positions):
        """ ## Method for tests purposes """

        if len(positions) != self._size:
            return False

        while len(positions):
            self._pos.append(positions.pop(0))
        
        return self._pos[0]


    
    def move_forward(self, new_head, reward):

        allowed_points, rew = self._possible_moves()
        if new_head not in allowed_points:
            return False

        self._tails.append(self._pos.pop()) # save the last tail
        self._pos.insert(0, new_head)
        self._add_reward(reward)
        self.change_status(True)
        return self._tails[-1]
    

    def move_backward(self):

        if len(self._tails) == 0:
            return False

        head = self._pos.pop(0)
        self._pos.append(self._tails.pop())
        self._sub_reward()
        self.change_status(False)
        return head

        

    def _possible_moves(self, forbidden_points = []):

        head = self._pos[0]
        next_possible_points = [
            [head[0] + 1 , head [1]],
            [head[0] - 1 , head [1]], 
            [head[0], head[1] + 1], 
            [head[0], head[1] - 1]
        ]

        next_possible_rewards = []

        allowed_points = []
        for new_head in next_possible_points:
            if ( new_head[0] >= 0 or new_head[0] < self._board_width or 
            new_head[1] >= 0 or new_head[1] < self._board_height ):
                allowed_points.append(new_head)
                next_possible_rewards.append(0)
        
        for point in forbidden_points:
            if point in allowed_points:
                next_possible_rewards[allowed_points.index(point)] += gl.FORBBIDEN
        
        return allowed_points, next_possible_rewards
        


    def _heuristic_search(self, allowed_points,  agents):
        """return list of allowed points with updated rewards based lenght"""
        if len(agents) == 0:
            return allowed_points
        
        agents_points = []   
        head = self._pos[0]

        for agent in agents:
            agents_points += agent.get_round_pos()

        for point in agents_points:
            x_dist = head[0] - point[0]
            y_dist = head[1] - point[1]
            if x_dist > 0:
                self._update_rewards([head[0]-1, head[1]], [head[0] + 1, head[1]],
                 allowed_points,x_dist, self._board_width )
            else:
                self._update_rewards( [head[0] + 1, head[1]], [head[0]-1, head[1]],
                 allowed_points,x_dist, self._board_width )
            
            if y_dist > 0:
                self._update_rewards([head[0], head[1] - 1], [head[0], head[1] + 1],
                 allowed_points,y_dist, self._board_height )
            else:
                self._update_rewards([head[0], head[1] + 1], [head[0], head[1] - 1],
                 allowed_points,y_dist, self._board_height )
        
        return allowed_points
        
        


        










# class Agent:

#     def __init__(self, size, colors):
#         """
#         Initialize agent variables.
#         ##### Input:
#         * size : snake length
#         * color : dict of two colors
#         """
#         self.head = colors['head']
#         self.body = colors['body']
#         self.size = size
#         self.reward = 0
#         self.pos = []
#         self.prev_tail = [0,0]
#         self.id = gl.SERIAL_NUM
#         gl.SERIAL_NUM += 1
#         gl.updated_agent[f"{self.id}"] = False


#     def set_on_board(self, taken_points):

#         """
#         Choose randomly the point on Canvas the agent will start from.
#         ##### Input: 
#         * taken_points : the points that already was taken by the other agents
#         """

#         box_point_width = int(gl.BOARD_WIDTH / gl.DOT_SIZE) - gl.BOARD_PADDING - 1   # minus board padding + minus 1 because it represents index
#         box_point_height = int(gl.BOARD_HEIGHT / gl.DOT_SIZE) - gl.BOARD_PADDING - 1 # minus board padding
#         max_attempts = 10  # max attempts to determine agent position
#         points_had_set = False
#         rand_head = lambda : [[rand.randint(0, box_point_width  ), rand.randint(0, box_point_height  )]]

#         while (points_had_set == False ):      
#             # set the head
#             self.pos = rand_head()
#             while self.pos[0] in taken_points:
#                     self.pos = rand_head()
#                     max_attempts -= 1
#                     if max_attempts <= 0:
#                         print(f"**Failure, Can not set agent N.o. {self.id}")
#                         exit(1)

#             if self.size > 1:
#                 points_had_set = self.__set_the_rest__(1, taken_points)      
#                 max_attempts -= 1
#             else:
#                 points_had_set = True
               
#         gl.BOARD.itemconfig(f"{self.pos[0][0]}-{self.pos[0][1]}", fill = self.head)                 
#         for point in self.pos[1: ]:
#             gl.BOARD.itemconfig(f"{point[0]}-{point[1]}",fill = self.body)


     
#     def __set_the_rest__(self,  i, taken_points):
        
#         if i == self.size:
#             return True

#         points = possible_points(self.pos[i-1], self.pos[ : i-1] + taken_points)
#         points = [ point[:2] for point in points if point[2] > gl.ForbiddenBiteReward]
#         flag = False

#         while len(points) > 0 and flag == False:
#             if len(self.pos) == i + 1 :
#                 self.pos.pop()
            
#             point = points.pop(0)
#             self.pos.append(point)
#             flag = self.__set_the_rest__(i + 1, taken_points)

#         return flag

#     def positions_updating(self, new_point):
#         self.pos.insert(0, new_point[:2])
#         self.prev_tail = self.pos.pop()
#         self.reward += new_point[2]
#         gl.updated_agent[f"{self.id}"] = True           



# class A_Agent(Agent):

#     def __init__(self, size, colors):
#         super().__init__(size, colors)

#         self.mini_max =  MiniMax()


#     def move(self, A_Agents, E_Agents):

#         e_agents = E_Agents
#         ind = A_Agents.index(self)
#         a_agents = A_Agents[:ind] + A_Agents[ind+1 :]
#         # Collect "Enemies" points (include A_Agents points except self points)
#         e_agents_points = [ agent.pos.copy() for agent in e_agents ]
#         a_agents_points = [ agent.pos.copy() for agent in a_agents ]
#         self_pos_ = self.pos.copy()

#         final_head = self.mini_max.activate(self_pos_,e_agents_points,a_agents_points , 0 )

#         self.positions_updating(final_head)



# class E_Agent(Agent):

#     def __init__(self, size, colors):
#         super().__init__(size, colors)

    
#     def move(self, A_Agents, E_Agents):
#         """
#         #### move E agent
#         ##### input:
#         * A_Agents : list of the agents we want to catch
#         * E_Agent : list of the agents we want avoid from biting them
#         """
        
#         forbidden_points = []
#         for agent in E_Agents:
#             if gl.updated_agent[f"{agent.id}"]:
#                 forbidden_points += agent.pos[:len(agent.pos)-1]
#             else:
#                 forbidden_points += agent.pos
        
#         forbidden_points += self.pos[ : len(self.pos) - 1]

#         points = possible_points(self.pos[0], forbidden_points)
#         self.heuristic_search(A_Agents, points)
#         rand.shuffle(points)
#         points = sorted(points, key = lambda x : x[2], reverse= True)
#         self.positions_updating(points.pop(0))




#     def heuristic_search(self, A_Agents, points):
#         """
#         Gives reward to the points that will get the agent closer to its target
#         Algorithm based heuristic search
#         ##### input:
#         * A_Agent : The agents we need to catch (target), A_Agent Object
#         * points  : nested list of points and the their temporary rewards
#         """
#         if len(A_Agents) == 0:
#             return []
        
#         
#         for agent in A_Agents:
#             if gl.updated_agent[f"{agent.id}"]:
#                 points_to_chase += agent.pos[1:] + [agent.prev_tail]
#             else:
#                 points_to_chase += agent.pos

#         nearest_point = points_to_chase[0]
#         min_dist = gl.BOARD_HEIGHT + gl.BOARD_WIDTH

#         for point, index in zip(points_to_chase, range(0, len(points_to_chase))):
#             dist = (abs(self.pos[0][0] - point[0]) + abs(self.pos[0][1] - point[1]))
#             if dist < min_dist:
#                 min_dist = dist
#                 nearest_point = index
        
#         wanted_point = points_to_chase[nearest_point]

#         X_dist = self.pos[0][0] - wanted_point[0]
#         Y_dist = self.pos[0][1] - wanted_point[1]
        
#         if X_dist > 0:
#             self.update_rewards([self.pos[0][0] - 1, self.pos[0][1]], [self.pos[0][0] + 1, self.pos[0][1]], points, X_dist)
#         else :
#             self.update_rewards([self.pos[0][0] + 1, self.pos[0][1]], [self.pos[0][0] - 1, self.pos[0][1]], points, X_dist)
#         if Y_dist > 0:
#             self.update_rewards([self.pos[0][0],self.pos[0][1] - 1], [self.pos[0][0],self.pos[0][1] + 1], points, Y_dist)
#         else :
#             self.update_rewards([self.pos[0][0],self.pos[0][1] + 1], [self.pos[0][0],self.pos[0][1] - 1], points, Y_dist)



#     def update_rewards(self, rew_point, cost_point, points, dist):

#         indexOf = lambda part : points.index(list(filter(lambda var : var[:2] == part , points))[0]) 
#         reward = lambda distance : abs(distance)
        
#         try:
#             points[indexOf(rew_point)][2] += reward(dist)
#         except:
#             pass
#         try:
#             points[indexOf(cost_point)][2] -= reward(dist)
#         except:
#             pass


        

    


