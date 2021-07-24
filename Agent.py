from globals import gl, possible_points
import random as rand
from tkinter import Tk, Frame, Canvas, ALL, NW
import copy
from miniMax import MiniMax

class Agent:

    def __init__(self, size, colors):
        """
        Initialize agent variables.
        ##### Input:
        * size : snake length
        * color : dict of two colors
        """
        self.head = colors['head']
        self.body = colors['body']
        self.size = size
        self.reward = 0
        self.pos = []
        self.prev_tail = [0,0]
        self.id = gl.SERIAL_NUM
        gl.SERIAL_NUM += 1
        gl.updated_agent[f"{self.id}"] = False


    def set_on_board(self, taken_points):

        """
        Choose randomly the point on Canvas the agent will start from.
        ##### Input: 
        * taken_points : the points that already was taken by the other agents
        """

        box_point_width = int(gl.BOARD_WIDTH / gl.DOT_SIZE) - gl.BOARD_PADDING - 1   # minus board padding + minus 1 because it represents index
        box_point_height = int(gl.BOARD_HEIGHT / gl.DOT_SIZE) - gl.BOARD_PADDING - 1 # minus board padding
        max_attempts = 10  # max attempts to determine agent position
        points_had_set = False
        rand_head = lambda : [[rand.randint(0, box_point_width  ), rand.randint(0, box_point_height  )]]

        while (points_had_set == False ):      
            # set the head
            self.pos = rand_head()
            while self.pos[0] in taken_points:
                    self.pos = rand_head()
                    max_attempts -= 1
                    if max_attempts <= 0:
                        print(f"**Failure, Can not set agent N.o. {self.id}")
                        exit(1)

            if self.size > 1:
                points_had_set = self.__set_the_rest__(1, taken_points)      
                max_attempts -= 1
            else:
                points_had_set = True
               
        gl.BOARD.itemconfig(f"{self.pos[0][0]}-{self.pos[0][1]}", fill = self.head)                 
        for point in self.pos[1: ]:
            gl.BOARD.itemconfig(f"{point[0]}-{point[1]}",fill = self.body)


     
    def __set_the_rest__(self,  i, taken_points):
        
        if i == self.size:
            return True

        points = possible_points(self.pos[i-1], self.pos[ : i-1] + taken_points)
        points = [ point[:2] for point in points if point[2] > gl.ForbiddenBiteReward]
        flag = False

        while len(points) > 0 and flag == False:
            if len(self.pos) == i + 1 :
                self.pos.pop()
            
            point = points.pop(0)
            self.pos.append(point)
            flag = self.__set_the_rest__(i + 1, taken_points)

        return flag

    def positions_updating(self, new_point):
        self.pos.insert(0, new_point[:2])
        self.prev_tail = self.pos.pop()
        self.reward += new_point[2]
        gl.updated_agent[f"{self.id}"] = True
    
    # def remove_forbidden_points(self, Agents, points):
        
    #     coords = []

    #     for agent in Agents:

    #         for point in agent.body_pos[:len(agent.body_pos) - 1]: #except the tail
    #             coords.append(point)
    #         if gl.updated_agent[f"{agent.id}"]:
    #             coords.append(agent.body_pos[len(agent.body_pos) - 1: len(agent.body_pos)])
    #         else:
    #             coords.append(agent.head_pos)
        
    #     tmp_points = []

    #     for point in points:
    #         if point not in coords:
    #             tmp_points.append(point)
        
    #     return tmp_points





            



class A_Agent(Agent):

    def __init__(self, size, colors):
        super().__init__(size, colors)

        self.mini_max =  MiniMax()




    def move(self, A_Agents, E_Agents):

        agents = A_Agents + E_Agents
        agents.remove(self)
        # Collect "Enemies" points (include A_Agents points except self points)
        agents_points = [ copy.deepcopy(agent.pos) for agent in agents ]
        self_pos_ = copy.deepcopy(self.pos)

        final_head = self.mini_max.activate(self_pos_,agents_points, 0 )

        self.positions_updating(final_head)
        # points = possible_points(self.head_pos, self.body_pos)
        # allowed_points = self.remove_forbidden_points(A_Agents + E_Agents, points)

        # if len(allowed_points) > 0:

        #     self.take_max_val_ = []
        #     self.take_head_ = []
        #     self.take_min_val_ = []
        #     heads = []
        #     bodies = []
        #     agents = A_Agents + E_Agents
        #     agents.remove(self)

        #     # Collect "Enemies" points (include A_Agents points except self points)
        #     for agent in agents:
                
        #         body_len = len(agent.body_pos)

        #         if gl.updated_agent[f"{agent.id}"]:
        #             if body_len == 0:
        #                 heads.append(copy.deepcopy(agent.prev_tail))
        #                 bodies.append([])
        #             else:
        #                 heads.append(copy.deepcopy(agent.body_pos[0]))
        #                 bodies.append(copy.deepcopy(agent.body_pos[1:]))
        #         else:
        #             heads.append(copy.deepcopy(agent.head_pos))
        #             bodies.append(copy.deepcopy(agent.body_pos))
                
        #     self_head_pos = copy.deepcopy(self.head_pos)
        #     self_body_pos = copy.deepcopy(self.body_pos)

        #     self.self_heads_iterator(allowed_points, self_head_pos, self_body_pos, heads, bodies)

        # else:
        #     print(f"Agent {self.id} got stuck")

        # for _ in self.take_min_val_:
        #     self.take_max_val_.append(min(_))

        # final_head = self.take_head_[self.take_max_val_.index(max(self.take_max_val_))]

        # self.positions_updating(final_head)
        

    def self_heads_iterator(self, allowed_points, self_head_pos, self_body_pos, heads, bodies):

        for new_head in allowed_points:
            self.take_head_.append(new_head)
            self.tmp_avg_ = []
            self.self_possible_movment(new_head, self_head_pos, self_body_pos, heads, bodies)
            self.take_min_val_.append(copy.deepcopy(self.tmp_avg_))



    def self_possible_movment(self, new_head, self_head_pos, self_body_pos, heads, bodies):
        # Simulate a new position after progress to "new head"
        self_body_pos.insert(0, new_head)
        prev_tail = self_body_pos.pop()
        self_head_pos = new_head
        new_heads = []

        for head, body in zip(heads, bodies):
                    new_heads.append(possible_points(head, body))       
        
        self.others_possible_movement(self_head_pos, self_body_pos, heads, bodies, new_heads, 0)
        # body & head restoration:
        self_body_pos.append(prev_tail)
        self_head_pos = self_body_pos.pop(0)        
        pass
    

    def others_possible_movement(self, self_head_pos,self_body_pos,  heads, bodies, new_heads,i ):
        # Simulate all the possibilities of agents progress:
        if i == len(new_heads):
            
            # Calculate and save utility
            self.calculate_utility(self_head_pos,self_body_pos, heads, bodies)
            return 

        for j in range(0, len(new_heads[i])):
            
            bodies[i].insert(0, heads[i])
            prev_tail = bodies[i].pop()
            heads[i] = new_heads[i][j]
            self.others_possible_movement(self_head_pos, self_body_pos, heads, bodies, new_heads,i + 1)
            # body[i] and head[i] restoration:
            bodies[i].append(prev_tail)
            heads[i] = bodies[i].pop(0)


    def calculate_utility(self, self_head_pos,self_body_pos, heads, bodies): # bodies transfared to improve the calculation's accuracy in the future

        sum_dist = 0 # Manhattan distance
        self_points = self_body_pos
        self_points.append(self_head_pos)
        
        for head in heads:
            for self_point in self_points:
                sum_dist += (abs(head[0] - self_point[0]) + abs(head[1] - self_point[1]))
        
        try:
            avg_dist = sum_dist / (len(heads) * len(self_points))
        except:
            print("**Error divide by 0")
            avg_dist = 0

        self.tmp_avg_.append(avg_dist)
        


class E_Agent(Agent):

    def __init__(self, size, colors):
        super().__init__(size, colors)

    
    def move(self, A_Agents, E_Agents):
        """
        #### move E agent
        ##### input:
        * A_Agents : list of the agents we want to catch
        * E_Agent : list of the agents we want avoid from biting them
        """
        
        forbidden_points = []
        for agent in E_Agents:
            if gl.updated_agent[f"{agent.id}"]:
                forbidden_points += agent.pos[1:] + [agent.prev_tail]
            else:
                forbidden_points += agent.pos

        points = possible_points(self.pos[0], self.pos[1: len(self.pos) - 1] + forbidden_points)
        self.heuristic_search(A_Agents, points)
        rand.shuffle(points)
        points = sorted(points, key = lambda x : x[2], reverse= True)
        self.positions_updating(points.pop(0))




    def heuristic_search(self, A_Agents, points):
        """
        Gives reward to the points that will get the agent closer to its target
        Algorithm based heuristic search
        ##### input:
        * A_Agent : The agents we need to catch (target), A_Agent Object
        * points  : nested list of points and the their temporary rewards
        """
        if len(A_Agents) == 0:
            return []
        
        points_to_chase = []
        for agent in A_Agents:
            if gl.updated_agent[f"{agent.id}"]:
                points_to_chase += agent.pos[1:] + [agent.prev_tail]
            else:
                points_to_chase += agent.pos

        nearest_point = points_to_chase[0]
        min_dist = gl.BOARD_HEIGHT + gl.BOARD_WIDTH

        for point, index in zip(points_to_chase, range(0, len(points_to_chase))):
            dist = (abs(self.pos[0][0] - point[0]) + abs(self.pos[0][1] - point[1]))
            if dist < min_dist:
                min_dist = dist
                nearest_point = index
        
        wanted_point = points_to_chase[nearest_point]

        X_dist = self.pos[0][0] - wanted_point[0]
        Y_dist = self.pos[0][1] - wanted_point[1]
        
        if X_dist > 0:
            self.update_rewards([self.pos[0][0] - 1, self.pos[0][1]], [self.pos[0][0] + 1, self.pos[0][1]], points, X_dist)
        else :
            self.update_rewards([self.pos[0][0] + 1, self.pos[0][1]], [self.pos[0][0] - 1, self.pos[0][1]], points, X_dist)
        if Y_dist > 0:
            self.update_rewards([self.pos[0][0],self.pos[0][1] - 1], [self.pos[0][0],self.pos[0][1] + 1], points, Y_dist)
        else :
            self.update_rewards([self.pos[0][0],self.pos[0][1] + 1], [self.pos[0][0],self.pos[0][1] - 1], points, Y_dist)



    def update_rewards(self, rew_point, cost_point, points, dist):

        indexOf = lambda part : points.index(list(filter(lambda var : var[:2] == part , points))[0]) 
        reward = lambda distance : abs(distance)
        
        try:
            points[indexOf(rew_point)][2] += reward(dist)
        except:
            pass
        try:
            points[indexOf(cost_point)][2] -= reward(dist)
        except:
            pass


        

    


