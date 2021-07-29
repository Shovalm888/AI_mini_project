from globals import gl
from tkinter import *
from agent import *
from agent_A import AgentA
from agent_E import AgentE
from board import Board

class Agent_Snake(Frame):
    
    def __init__(self, root, A_agents_num, E_agents_num,A_agent_len, E_agent_len ):
        """initializes game board"""
        super().__init__()
        self.master.title('AI_mini_project')
        Board(root)
        self.init_game(A_agents_num, E_agents_num,A_agent_len, E_agent_len )
        gl.BOARD.pack()


    def init_game(self, A_agents_num, E_agents_num,A_agent_len, E_agent_len ):
        """initializes game."""
        self.inGame = True
        self.create_agents( A_agents_num , E_agents_num, A_agent_len, E_agent_len)
        self.draw_agents()
        gl.BOARD.after(gl.DELAY, self.on_timer)
    

    def create_agents(self, A , E ,  A_len , E_len ):
        """Create agents objects and locate them on the game board"""
        if A < 0 or A > len(gl.A_agents_colors) or E < 0 or E > len(gl.E_agents_colors):
            print("** Invalid agents number")
            exit(1)
        
        self.A_Agents = []
        self.E_Agents = []
        while A > 0:
            self.A_Agents.append(AgentA(A_len, gl.A_agents_colors[A - 1]))
            A -= 1
        while E > 0:
            self.E_Agents.append(AgentE(E_len, gl.E_agents_colors[E - 1]))
            E -= 1

        self.A_Agents[0]._set_on_board_by_points([[0,0],[1,0],[2,0]])
        self.E_Agents[0]._set_on_board_by_points([[6,3],[7,3],[8,3]])
        # taken_points = []
        # for agent in self.A_Agents + self.E_Agents:
        #     agent.set_on_board_randomly( taken_points)
        #     taken_points += agent.get_pos()

    
    def on_timer(self):
        """Creates a game cycle each timer event """
        self.check_collisions()
        if self.inGame:
            agents = self.A_Agents + self.E_Agents

            for agent in agents:
                agent.change_status(False)

            for agent in agents:
                agent.automatic_movement(self.A_Agents, self.E_Agents)

            self.draw_updated_agents() 
            gl.BOARD.after(gl.DELAY, self.on_timer)
        else:
            self.game_over()  
       

    def check_collisions(self):
        """Checks for board collision based on agents colors"""
        agents = self.A_Agents + self.E_Agents
        for agent in agents:

            if (gl.BOARD.itemconfig(f"{agent.get_pos()[0][0]}-{agent.get_pos()[0][1]}")['fill'][4] 
                != agent.get_head_color()):
                self.inGame = False

            for point in agent.get_pos()[1:]:
                if gl.BOARD.itemconfig(f"{point[0]}-{point[1]}")['fill'][4] != agent.get_body_color():
                    self.inGame = False
        

    def draw_agents(self):
        """ Draw the agents on the board (for the first round)"""
        agents = self.A_Agents + self.E_Agents

        for agent in agents:
            points = agent.get_pos()
            head = points[0]
            body = points[1:]
            gl.BOARD.itemconfig(f"{head[0]}-{head[1]}", fill = agent.get_head_color())

            for point in body:
                gl.BOARD.itemconfig(f"{point[0]}-{point[1]}", fill = agent.get_body_color())


    def draw_updated_agents(self):
        """Update the agents on the board after each round"""
        agents = self.A_Agents + self.E_Agents
        for agent in agents:
            # remove tail from canvas
            gl.BOARD.itemconfig(f"{agent.get_prev_tail()[0]}-{agent.get_prev_tail()[1]}", fill = gl.REGULAR_SQUARE)
            # promotes snake's head
            gl.BOARD.itemconfig(f"{agent.get_pos()[0][0]}-{agent.get_pos()[0][1]}", fill = agent.get_head_color())
            # changes snakes prev head color to body color
            if len(agent.get_pos()) > 1:
                gl.BOARD.itemconfig(f"{agent.get_pos()[1][0]}-{agent.get_pos()[1][1]}", fill = agent.get_body_color())


    def game_over(self):
        """deletes all agents and draws agents rewards message"""
        winner_msg=""
        # update E_agent in case that he catch A_agent:
        for e_agent in self.E_Agents:
            for a_agent in self.A_Agents:
                if e_agent.get_pos()[0] in a_agent.get_pos():
                    winner_msg = f"Winner : {e_agent.get_color_name()}\nLoser :  {a_agent.get_color_name()}\n\n"

        msg= f"A_agents :"
        for agent in self.A_Agents:
            msg += f"\nagent {agent.get_color_name()} reward : {agent.get_reward():.1f}"
        
        msg += f"\nE_agents :"
        for agent in self.E_Agents:
             msg += f"\nagent : {agent.get_color_name()} reward : {agent.get_reward()}"

        msg = winner_msg + msg
        gl.BOARD.delete(ALL)
        gl.BOARD.create_text(gl.BOARD.winfo_width() /2, gl.BOARD.winfo_height()/2,
                         text=msg)

