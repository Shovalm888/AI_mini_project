from globals import gl
import random as rand


class Agent:

    def __init__(self, size, color):
        
        self._pos = []     # points of the agent's location (position), pos[0] == agent's head
        self._tails = []   # keeps the previous tails to allow position restoring
        self._rewards = [] # keeps the previous rewards to allow position restoring
        self._size = size  # agent (snake) length
        self._head_color = color['head']
        self._body_color = color['body']
        self._color_name = color['name']
        self._status = False  # indicate if the position already updated for the current round
        self._id = gl.SERIAL_NUM
        gl.SERIAL_NUM += 1

    def get_pos(self):
        return self._pos

    def get_round_pos(self):
        if self._status: # alreay updated
            return self._pos[1:] + [self._tails[-1]]
        return self._pos

    def get_prev_tail(self):
        if len(self._tails) == 0:
            return None
        return self._tails[-1]
    
    def get_status(self):
        return self._status

    def get_head_color(self):
        return self._head_color

    def get_body_color(self):
        return self._body_color

    def get_color_name(self):
        return self._color_name

    def get_id(self):
        return self._id

    def get_reward(self):
        return sum(self._rewards)

    def get_size(self):
        return self._size

    def _add_reward(self, amount):
        self._rewards.append(amount)
    
    def _sub_reward(self):
        if len(self._rewards) == 0:
            return False
        return self._rewards.pop()
    
    def change_status(self, state):
        self._status = True if state else False


    def set_on_board_randomly(self, taken_points = [], max_attempts = 20): 
        """Set agent._pos randomly""" 
        rand_head = lambda : [rand.randint(0, gl.GAME_ZONE_WIDTH - 1), rand.randint(0, gl.GAME_ZONE_HEIGHT - 1)]
        all_set = False

        while all_set == False:
            if max_attempts <= 0: # to prevent infinity loop in case that we can not find a place for agent
                return False
            point = rand_head()
            while point in taken_points:
                point = rand_head()
            self._pos = [point]
            all_set = self._set_on_board_the_rest( 1, taken_points + self._pos)
            max_attempts -= 1
                   

    def _set_on_board_the_rest(self, iter , taken_points):

        if iter == self.get_size():
            return True

        allowed_points, rew = self._possible_moves(taken_points, allowed_neg_rew= False)
        rand.shuffle(allowed_points)
        all_set = False
        while len(allowed_points) > 0 and all_set == False:
            self._pos.insert(0, allowed_points.pop())
            all_set = self._set_on_board_the_rest(iter + 1, taken_points + self._pos)

        return all_set


    def move_forward(self, new_head, reward):
        """Promotes agent head to new_head, return: (success : the replaced tail , failure : False)"""
        allowed_points, rew = self._possible_moves()
        if new_head not in allowed_points: # verify that new_head is possible for the agent
            return False

        self._tails.append(self._pos.pop()) # save the last tail
        self._pos.insert(0, new_head)
        self._add_reward(reward)
        self.change_status(True)            # indicates that the agent's location was updated
        return self._tails[-1]
    

    def move_backward(self):
        """Restore the last location of the agent"""
        if len(self._tails) == 0:
            return False

        head = self._pos.pop(0)
        self._pos.append(self._tails.pop())
        self._sub_reward()        # pop the last reward
        self.change_status(False) # restore status
        return head

        

    def _possible_moves(self, forbidden_points = [], allowed_neg_rew = True):
        """Returns the (points, rewards) to which the agent can advance, points that are in the forbidden list will get a gl.FORBIDDEN value or be deleted"""
        head = self._pos[0]
        next_possible_points = [
            [head[0] + 1 , head [1]],
            [head[0] - 1 , head [1]], 
            [head[0], head[1] + 1], 
            [head[0], head[1] - 1]
        ]

        next_possible_rewards = []
        allowed_points = []
        # Deletes the points that have crossed the board boundaries
        for new_head in next_possible_points:
            if ( new_head[0] >= 0 and new_head[0] < gl.GAME_ZONE_WIDTH and 
                new_head[1] >= 0 and new_head[1] < gl.GAME_ZONE_HEIGHT ):
                allowed_points.append(new_head)
                next_possible_rewards.append(0)
        
        i = 0
        # Handles the points that contained in the forbidden list
        while i < len(allowed_points):
            if allowed_points[i][:2] in forbidden_points:
                if allowed_neg_rew:
                    next_possible_rewards[i] += gl.FORBIDDEN
                else:
                    allowed_points.remove(allowed_points[i])
                    next_possible_rewards.remove(next_possible_rewards[i])
                    i -= 1
            i+=1
        return allowed_points, next_possible_rewards
        

    def _get_agents_points(self, agents,  ignore = None):
        """Returns the agents' points in a list, include self points (except the self tail)
        input : (agents : list of agents , ignore : an agent who might be on the list we want to ignore)"""
        points = []
        for agent in agents:
            if agent != ignore:
                points += agent.get_round_pos()[:-1]
        points += self.get_pos()[:-1]
        return points


    def _set_on_board_by_points(self, positions):
        """ ## Method for tests purposes """
        if len(positions) != self._size:
            return False

        while len(positions):
            self._pos.append(positions.pop(0)) 
        return self._pos[0]