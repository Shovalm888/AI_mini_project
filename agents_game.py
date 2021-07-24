from globals import gl
from tkinter import *
from Agent import *

class Agent_Snake(Frame):
    
    def __init__(self, root):
        """initialize Canvas board and call self.init_game()"""

        super().__init__()
                
        self.master.title('AI_mini_project')
        
        canvas = Canvas(root, width = gl.BOARD_WIDTH, height = gl.BOARD_HEIGHT,
                         background=gl.BACKGROUND_COLOR, highlightthickness = 0)
        gl.set_board(canvas)
        self.init_game()
        gl.BOARD.pack()


    def init_game(self):
        """
        * initializes game.
        * create agents.
        * call for each one set_on_board()
        """

        self.inGame = True
        self.create_agents( 1 , 2, 1, 1)
        gl.BOARD.after(gl.DELAY, self.on_timer)
    

    def create_agents(self, A = 0, E = 0,  A_len = 5, E_len = 5):
        
        if A < 0 or A > 2 or E < 0 or E > 2:
            print("** Invalid agents number")
            exit(1)
        
        self.A_Agents = []
        self.E_Agents = []

        if A == 2:
            self.A_Agents.append(A_Agent(A_len, gl.Brown))
            A -= 1

        if A == 1:
            self.A_Agents.append(A_Agent(A_len, gl.Purple))
        
        if E == 2:
            self.E_Agents.append(E_Agent(E_len, gl.Yellow))
            E -= 1

        if E == 1:
            self.E_Agents.append(E_Agent(E_len, gl.Blue))

        taken_points = []
        for agent in self.A_Agents + self.E_Agents:
            agent.set_on_board(taken_points)
            taken_points += agent.pos

    
    def on_timer(self):
        """
        #### Creates a game cycle each timer event
        ##### if inGame:
            * Updates gl.updated_agent for each agent
            * Call move() for each agent
            * Call self.draw_updated_agents() to draw them.
        ##### else:
            * End the game
        """

        self.check_collisions()

        if self.inGame:

            agents = self.A_Agents + self.E_Agents

            for agent in agents:
                gl.updated_agent[f"{agent.id}"] = False

            for agent in agents:
                agent.move(self.A_Agents, self.E_Agents)

            self.draw_updated_agents()
            
            gl.BOARD.after(gl.DELAY, self.on_timer)

        else:
            self.game_over()  


    def draw_updated_agents(self):
        """Update the agents on the board and check if there were bites"""
        agents = self.A_Agents + self.E_Agents

        for agent in agents:

            # Snake with lenght 1 stay in he same place
            if len(agent.pos) == 1 and agent.pos[0] == agent.prev_tail:
                self.inGame = False
            
            gl.BOARD.itemconfig(f"{agent.prev_tail[0]}-{agent.prev_tail[1]}", fill = gl.REGULAR_SQUARE)
            # Check if it's head is biting someone
            # if gl.BOARD.itemconfig(f"{agent.pos[0][0]}-{agent.pos[0][1]}")['fill'][4] != gl.REGULAR_SQUARE:
            #     self.inGame = False

            gl.BOARD.itemconfig(f"{agent.pos[0][0]}-{agent.pos[0][1]}", fill = agent.head)

            if len(agent.pos) > 1:
                gl.BOARD.itemconfig(f"{agent.pos[1][0]}-{agent.pos[1][1]}", fill = agent.body)

        

    def check_collisions(self):

        agents = self.A_Agents + self.E_Agents

        for agent in agents:
            if gl.BOARD.itemconfig(f"{agent.pos[0][0]}-{agent.pos[0][1]}")['fill'][4] != agent.head:
                self.inGame = False

            for point in agent.pos[1:]:
                if gl.BOARD.itemconfig(f"{point[0]}-{point[1]}")['fill'][4] != agent.body:
                    self.inGame = False
        


    def game_over(self):
        """deletes all agents and draws agents rewards message"""

        msg= f"A_agents :"
        for agent in self.A_Agents:
            msg += f"\nagent {agent.id} reward : {agent.reward}"
        
        msg += f"\nE_agents :"
        for agent in self.E_Agents:
             msg += f"\nagent : {agent.id} reward : {agent.reward}"
 
        gl.BOARD.delete(ALL)
        gl.BOARD.create_text(gl.BOARD.winfo_width() /2, gl.BOARD.winfo_height()/2,
                         text=msg)

