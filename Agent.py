from globals import gl, possible_points
import random as rand
from tkinter import Tk, Frame, Canvas, ALL, NW

class Agent:

    def __init__(self, size, colors):

        self.head = colors['head']
        self.body = colors['body']
        self.size = size
        self.score = 0
        self.body_pos = []
        self.head_pos = []
        self.prev_tail = []
        self.id = gl.SERIAL_NUM
        gl.SERIAL_NUM += 1
        gl.updated_agent[f"{self.id}"] = False


    def set_on_board(self):

        """creates objects on Canvas"""

        box_point_width = int(gl.BOARD_WIDTH / gl.DOT_SIZE) - 2 - 1   # minus board padding + minus 1 because it represents index
        box_point_height = int(gl.BOARD_HEIGHT / gl.DOT_SIZE) - 2 - 1 # minus board padding
        max_attempts = 10
        points_had_set = False
        position = []

        while (points_had_set == False and max_attempts > 0):

            if len(self.head_pos) != 0:
                self.head_pos = []

            self.head_pos = [rand.randint(0, box_point_width  ), rand.randint(0, box_point_height  )]
            
            while gl.BOARD.itemconfig(f"{self.head_pos[0]}-{self.head_pos[1]}")['fill'][4] != gl.REGULAR_SQUARE:
                    max_attempts -= 1
                    if max_attempts <= 0:
                        print(f"**Failure, Can not set agent N.O. {self.id}")
                        exit(1)
                    self.head_pos[0] = rand.randint(0, box_point_width )
                    self.head_pos[1] = rand.randint(0, box_point_height )

            if self.size > 1:
                points_had_set = self.__set_the_rest__( 1)      
                max_attempts -= 1
            else:
                points_had_set = True

        if max_attempts <= 0:
            print (f"Agent: {self.id} has not added to the board!!!")
            return
                   
        gl.BOARD.itemconfig(f"{self.head_pos[0]}-{self.head_pos[1]}",
         fill = self.head)
                 
        for point in self.body_pos:
            gl.BOARD.itemconfig(f"{point[0]}-{point[1]}",fill = self.body)


     
    def __set_the_rest__(self,  i):
        
        if i == self.size:
            # self.prev_tail = self.body_pos[0]
            return True

        if i == 1:
            points = possible_points(self.head_pos, self.body_pos)
        else:
            points = possible_points(self.body_pos[i - 2], self.body_pos)

        rand.shuffle(points)

        flag = False

        while len(points) > 0 and flag == False:

            if len(self.body_pos) == i :
                self.body_pos.pop()
            
            point = points.pop()

            if point not in (self.body_pos + [self.head_pos]) and gl.BOARD.itemconfig(f"{point[0]}-{point[1]}")['fill'][4] == gl.REGULAR_SQUARE:
                self.body_pos.append(point)
                flag = self.__set_the_rest__(i + 1)

        return flag

    
    def remove_forbidden_points(self, Agents, points):
        
        coords = []

        for agent in Agents:

            for point in agent.body_pos:
                coords.append(point)
            if gl.updated_agent[f"{agent.id}"]:
                coords.append(agent.prev_tail)
            else:
                coords.append(agent.head_pos)
        
        tmp_points = []

        for point in points:
            if point not in coords:
                tmp_points.append(point)
        
        return tmp_points


    def positions_updating(self, new_point):
        self.body_pos.insert(0, self.head_pos)
        self.prev_tail = self.body_pos.pop()
        self.head_pos = new_point
        gl.updated_agent[f"{self.id}"] = True



            



class A_Agent(Agent):

    def __init__(self, size, colors):
        super().__init__(size, colors)

    def move(self, a, b):
        self.prev_tail=[0,0]
        points = possible_points(self.head_pos, self.body_pos)
        points = self.remove_forbidden_points(a+b, points)
        if len(points) > 0:
            self.positions_updating(points.pop())
        

    


class E_Agent(Agent):

    def __init__(self, size, colors):
        super().__init__(size, colors)

    
    def move(self, A_Agents, E_Agents):
        """moves E agent"""
        

        points = possible_points(self.head_pos, self.body_pos)

        preffered_directions = self.heuristic_search(A_Agents)

        allowed_points = self.remove_forbidden_points(E_Agents, points)
        
        reward = None      
        pref = None

        while len(preffered_directions) > 0:
            pref, reward = preffered_directions.pop()

            if pref in allowed_points:
                break
        
        
        if pref != None:
            self.positions_updating(pref)
            self.score += reward
        
        elif len(allowed_points) > 0 :
            rand.shuffle(allowed_points)
            self.positions_updating(allowed_points.pop())
        
        elif len(points) > 0 :
            self.positions_updating(points.pop())

        else :
            print("line 141")
            exit(1)
        

    def heuristic_search(self, A_Agents):

        if len(A_Agents) == 0:
            return []
        
        coords = [] 
        for agent in A_Agents:

            for point in agent.body_pos:
                coords.append(point)
            if gl.updated_agent[f"{agent.id}"]:
                coords.append(agent.prev_tail)
            else:
                coords.append(agent.head_pos)

        nearest_point = coords[0]
        min_dist = gl.BOARD_HEIGHT + gl.BOARD_WIDTH
        for point, index in zip(coords, range(0, len(coords))):

            dist = (abs(self.head_pos[0] - point[0]) + abs(self.head_pos[1] - point[1]))

            if dist < min_dist:
                min_dist = dist
                nearest_point = index
        
        X_dist = self.head_pos[0] - coords[nearest_point][0]
        Y_dist = self.head_pos[1] - coords[nearest_point][1]
        X_direction = -1
        Y_direction = -1
        to_ret = []

        if X_dist > 0:                
            X_direction = [self.head_pos[0] - 1, self.head_pos[1]]
        elif X_dist < 0:
            X_direction = [self.head_pos[0] + 1, self.head_pos[1]]
        if Y_dist > 0:
            Y_direction = [self.head_pos[0],self.head_pos[1] - 1]
        elif Y_dist < 0:
            Y_direction = [self.head_pos[0], self.head_pos[1] + 1]

        if X_dist == 0:
            to_ret.append([Y_direction, 2])
        elif Y_dist == 0:
            to_ret.append([X_direction, 2])

        else:
            if abs(Y_dist) > abs(X_dist):
                to_ret.append([X_direction, 1])
                to_ret.append([Y_direction, 2])

            else:
                to_ret.append([Y_direction, 1])
                to_ret.append([X_direction, 2])

        return to_ret




        

    


