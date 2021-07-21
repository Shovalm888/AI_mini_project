from globals import gl
from tkinter import *
from Agent import *



def main():

    root = Tk()
    Agent_Snake(root)
    root.mainloop()  


class Agent_Snake(Frame):
    
    def __init__(self, root):
        super().__init__()
                
        self.master.title('AI')
        
        canvas = Canvas(root, width = gl.BOARD_WIDTH, height = gl.BOARD_HEIGHT,
                         background=gl.BACKGROUND_COLOR, highlightthickness = 0)
        gl.set_board(canvas)
        self.init_game()
        gl.BOARD.pack()


    def init_game(self):
        """initializes game"""

        self.inGame = True

        self.create_agents( 1 , 2, 5, 3)
        gl.BOARD.after(gl.DELAY, self.on_timer)
    

    def create_agents(self, A = 0, E = 0,  A_len = 5, E_len = 5):
        
        if A < 0 or A > 2 or E < 0 or E > 2:
            print("** Unvalid agents number")
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

        for agent in self.A_Agents + self.E_Agents:
            agent.set_on_board()

    
    def on_timer(self):
        """creates a game cycle each timer event"""

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
                   
        agents = self.A_Agents + self.E_Agents
        for agent in agents:
            
            gl.BOARD.itemconfig(f"{agent.prev_tail[0]}-{agent.prev_tail[1]}", fill = gl.REGULAR_SQUARE)
            if gl.BOARD.itemconfig(f"{agent.head_pos[0]}-{agent.head_pos[1]}")['fill'][4] != gl.REGULAR_SQUARE:
                self.inGame = False
            gl.BOARD.itemconfig(f"{agent.head_pos[0]}-{agent.head_pos[1]}", fill = agent.head)
            if len(agent.body_pos) > 0:
                gl.BOARD.itemconfig(f"{agent.body_pos[0][0]}-{agent.body_pos[0][1]}", fill = agent.body)

        

    def game_over(self):
        """deletes all agents and draws game over message"""

        msg= f"A_agents :"
        for agent in self.A_Agents:
            msg += f"\nagent {agent.id} score : {agent.score}"
        
        msg += f"\nE_agents :"
        for agent in self.E_Agents:
             msg += f"\nagent : {agent.id} score : {agent.score}"
 
        gl.BOARD.delete(ALL)
        gl.BOARD.create_text(gl.BOARD.winfo_width() /2, gl.BOARD.winfo_height()/2,
                         text=msg)




if __name__ == '__main__':
    main()

