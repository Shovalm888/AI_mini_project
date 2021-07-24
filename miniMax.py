from globals import gl, possible_points
import copy

class MiniMax:
    
    def activate(self, self_pos_, agents_positions, iter):
        """
        ##### Input:
        * self_pos_ : list of points that represents the agent, e.g. [ [?,?], [?,?] ]
        * agents_positions : nested list of agents positions, e.g. [ [ [?,?] ], [ [?,?],[?,?] ] ]
        * iter : current iteration
        ##### Return value: 
        potential new point to go for, e.g. [?,?] OR []
        """
        
        if iter == gl.Tree_Depth:
            return self.calculate_utilitiy(self_pos_, agents_positions)
        ###################################################################
        #  NEED TO CONSIDER TAIL CASES (ABOUT THE FORBIDDEN POINTS) AND MAKE A GLOBAL FORBIDDEN POINTS FUNCTION
        ###################################################################
        forbidden_points = []
        for pos in agents_positions:
            forbidden_points += pos[: len(pos) - 1] # without their tail
        
        forbidden_points += self_pos_
        # if len(self_pos_) == 1:
        #     forbidden_points += self_pos_
        # else:
        #     forbidden_points += self_pos_[: len(self_pos_) - 1]
        #returns the collection of the possibles next step for the agents (besides self agent)
        next_self_heads = possible_points(self_pos_[0], forbidden_points )
        # remeove -100 rewards steps:
        next_self_heads = [ point[:2] for point in next_self_heads if point[2] > gl.ForbiddenBiteReward ] 
        next_else_heads = [] # A nested list that each cell will contain possible moves for the other agents 
        self.agents_possibles_scenarios(0, agents_positions, next_else_heads)

        take_max_ = []
        for self_new_head, i in zip(next_self_heads, range(0, len(next_self_heads))):
            # update self agent position
            tail = self.update_position(self_pos_, self_new_head)

            for others_new_heads in next_else_heads:
                # update agents position
                tails = []
                for other_new_head, other_pos in zip(others_new_heads, agents_positions):
                    tails.append(self.update_position(other_pos, other_new_head))
                    
                ## Recursive CALL
                tmp_res = self.activate( self_pos_, agents_positions, iter + 1 )
                
                # restore agents position
                for other_new_head, other_pos in zip(others_new_heads, agents_positions):
                   self.restore_position(other_pos, tails.pop(0))
                
                if len(take_max_) == i:
                    take_max_.append(tmp_res)
                else:
                    take_max_[i] = min(take_max_[i], tmp_res)
            # restore self agent position
            self.restore_position(self_pos_, tail)

        if iter != 0:
            if len( take_max_) == 0:
                return gl.ForbiddenBiteReward
            return max(take_max_)
        else:
            if len( take_max_) == 0:
                return self_pos_[0] + [gl.ForbiddenBiteReward]
            return next_self_heads[take_max_.index(max(take_max_))] + [max(take_max_)]



    def agents_possibles_scenarios(self, i, agents_positions, next_else_heads, heads_scenario = []):

        if len(agents_positions) == i:
            next_else_heads.append(copy.deepcopy(heads_scenario))
            return
        # Collect the forbidden points
        forbidden_points = []
        for pos in agents_positions[0:i]: # agents that already 'updated' (need to consider their tail in forbidden)
            forbidden_points += pos
        for pos in agents_positions[i+1:]:
            forbidden_points += pos[:len(pos) - 1] # agents that have not updated yet , ignoring thier tail

        forbidden_points += agents_positions[i]

        # if len(agents_positions[i]) == 1:
            # forbidden_points += agents_positions[i] # add self agent points except the tail
        # else:
        #     forbidden_points += agents_positions[i][ : len(agents_positions[i]) - 1]

        possible_heads = possible_points(agents_positions[i][0], forbidden_points )
        # remove -100 reward new_head points
        possible_heads = [ point[:2] for point in possible_heads if point[2] > gl.ForbiddenBiteReward]

        for new_head in possible_heads:
            tail = self.update_position(agents_positions[i], new_head)
            heads_scenario.append(new_head)
            #
            self.agents_possibles_scenarios( i + 1, agents_positions, next_else_heads, heads_scenario)
            # 
            heads_scenario.pop()
            self.restore_position(agents_positions[i], tail)

            

    def update_position(self, pos, new_head):
        tail = pos.pop()
        pos.insert(0, new_head)
        return tail

    def restore_position(self, pos, tail ):
        pos.append(tail)
        head = pos.pop(0)
        return head


         


    def calculate_utilitiy(self, self_pos_, agents_points):

        sum_dist = 0 # Manhattan distance
        
        for pursuer_points in agents_points:
            for self_point in self_pos_:
                sum_dist += (abs(pursuer_points[0][0] - self_point[0]) + abs(pursuer_points[0][1] - self_point[1]))
        
        try:
            avg_dist = sum_dist / (len(self_pos_) * len(agents_points))
        except:
            print("**Error divide by 0")
            avg_dist = 0

        return avg_dist



    def allowed_only(self, next_heads, nested_agents_points):

        forbidden_points = []

        for head in next_heads:
            for agent_points in nested_agents_points:
                if head in agent_points:
                    forbidden_points.append(head)

        return [head for head in next_heads if head not in forbidden_points] 
