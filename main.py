import random as rand
import sys
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW
import globals


class Agent():
    
    def __init__(self, length, type):
        # add verification on the length
        self.length = length
        self.type = type  # 'A' & 'E'
        self.id = globals.serial_num
        globals.serial_num = globals.serial_num + 2  # -------- ADD 2 TO THE ID INSTEAD 1
        
class Cons:
        
    BOARD_WIDTH = 130
    BOARD_HEIGHT = 130
    DELAY = 100
    DOT_SIZE = 10
    MAX_RAND_POS = 27


class Board(Canvas):

    def __init__(self, agents):
        super().__init__(width=Cons.BOARD_WIDTH, height=Cons.BOARD_HEIGHT,
                         background="black", highlightthickness=0)

        self.agents = agents
        self.init_game()
        self.pack()

    def init_game(self):
        """initializes game"""

        self.inGame = True
        self.dots = 3
        self.score = 0
        
        # # variables used to move snake object
        self.moveX = Cons.DOT_SIZE
        self.moveY = 0
        
        self.load_images()

        self.create_objects()
        # implement here bindall to pause the program
        self.after(Cons.DELAY, self.on_timer)

    def load_images(self):
        """loads images from the disk"""
    # size = 10, 10
    # try:
    #     im = Image.open("yellow.png")
    #     im.thumbnail(size, Image.ANTIALIAS)
    #     im.save("yellow.png", "PNG")
    # except IOError: 
    #     print("err")

        # Change the color to same color for each agent where the head is the darkest color
        # For 4 Agents, head and body, two colors for each:
        self.images_names = ['red', 'purple','red', 'brown', 'orange', 'red','black', 'green', 'yellow', 'blue', 'white']
 
        self.images = []

        try:
            for name in self.images_names:
                tmp = Image.open(f"images\{name}.png")
                self.images.append(ImageTk.PhotoImage(tmp))
        except IOError as e:
            
            print(e)
            sys.exit(1)
        
    def create_objects(self):
        """creates objects on Canvas"""
    
        for agent in self.agents:
            box_point_width = int(Cons.BOARD_WIDTH / Cons.DOT_SIZE)
            box_point_height = int(Cons.BOARD_HEIGHT / Cons.DOT_SIZE)
            max_attempts = 10
            points_had_set = False
            position = []

            while (points_had_set == False and max_attempts > 0):
                if len(position) != 0:
                    position = []

                position.append([Cons.DOT_SIZE * rand.randint(0, box_point_width - 1),
                                 Cons.DOT_SIZE * rand.randint(0, box_point_height - 1)])

                while len(self.gettags(self.find_enclosed(position[0][0], position[0][1],
                                                          position[0][0] + 10, position[0][1] + 10))) != 0:
                        position[0][0] = Cons.DOT_SIZE * rand.randint(0, box_point_width - 1)
                        position[0][1] = Cons.DOT_SIZE * rand.randint(0, box_point_height - 1)

                if agent.length > 1:
                    points_had_set = self.set_the_rest(position, agent.length, 1)
                    max_attempts -= 1
                else:
                    points_had_set = True

            if max_attempts == 0:
                print (f"Snake {agent.id} has not added to the board!!!")
                return
                       
            self.create_image(position[agent.length-1][0], position[agent.length-1][1],
             image = self.images[agent.id], anchor=NW,  tag=f"{agent.id}-head")

            for point in position[:agent.length - 1]:
                self.create_image(point[0], point[1], image = self.images[agent.id + 1], anchor=NW, tag=f"{agent.id}-dot")


     
    def set_the_rest(self,pos, length,  i):

        if i == length:
            return True

        #'down' = [10, 0], 'up' = [-10, 0], 'right' = [0, 10], 'left' = [0, -10]
 
        directions = [[10, 0], [-10, 0], [0, 10], [0, -10]]

        if pos[i - 1][0] == (Cons.BOARD_WIDTH - Cons.DOT_SIZE):
            directions.remove([10, 0])

        elif pos[i - 1][0] == 0:
            directions.remove([-10, 0])

        if pos[i - 1][1] == (Cons.BOARD_HEIGHT - Cons.DOT_SIZE):
            directions.remove([0, 10])

        elif pos[i - 1][1] == 0:
            directions.remove([0, -10])

        rand.shuffle(directions)

        flag = False

        while len(directions) > 0 and flag == False:

            if len(pos) == i + 1 :
                pos.pop()
            
            goto = directions.pop()

            point = [pos[i-1][0] + goto[0], pos[i-1][1] + goto[1]]

            if point not in pos and len(self.gettags(self.find_enclosed(point[0], point[1],
                                                      point[0] + 10, point[1] + 10))) == 0:
                pos.append(point)
                flag = self.set_the_rest(pos, length, i + 1)

        return flag
            


    def move_snake(self):
        """moves the Snake object"""
        
        dots = [self.find_withtag(f"{agent.id}-dot") for agent in self.agents]
        heads = [self.find_withtag(f"{agent.id}-head") for agent in self.agents]
        items = [dot + head for dot, head in zip(dots, heads)]

        
        for item, head in zip(items, heads): 

            z = 0

            while z < len(item)-1:

                c1 = self.coords(item[z])
                c2 = self.coords(item[z+1])
                self.move(item[z], c2[0]-c1[0], c2[1]-c1[1])
                z += 1

            x1, y1, x2, y2 = self.bbox(head)
            directions = [[10, 0], [-10, 0], [0, 10], [0, -10]]
            
            if x2 == (Cons.BOARD_WIDTH):
                directions.remove([10, 0])

            elif x1 == 0:
                directions.remove([-10, 0])

            if y2 == (Cons.BOARD_HEIGHT):
                directions.remove([0, 10])

            elif y1 == 0:
                directions.remove([0, -10])

            rand.shuffle(directions)

            self.moveX = -1
            while len(directions) > 0:

                goto = directions.pop()

                point = [x1 + goto[0], y1 + goto[1]]

                if len(self.gettags(self.find_enclosed(point[0], point[1],
                                                          point[0] + 10, point[1] + 10))) == 0:
                    self.moveX, self.moveY = goto
            
            if self.moveX == -1:
                self.inGame = False
            
            else:
                self.move(head, self.moveX, self.moveY)     


    def on_timer(self):
        """creates a game cycle each timer event"""

        # self.draw_score()
        self.check_collisions()

        if self.inGame:
            self.move_snake()
            self.after(Cons.DELAY, self.on_timer)
        else:
            self.game_over()  

    def game_over(self):
           """deletes all objects and draws game over message"""

           self.delete(ALL)
           self.create_text(self.winfo_width() /2, self.winfo_height()/2,
                            text="Game Over")
    # def draw_score(self):
    #     """draws score"""
        
    #     score = self.find_withtag("score")
    #     self.itemconfigure(score, text="Score: {0}".format(self.score))

    # --- Display results ----
    # def game_over(self):
    #     """deletes all objects and draws game over message"""

    #     self.delete(ALL)
    #     self.create_text(self.winfo_width() /2, self.winfo_height()/2,
    #                      text="Game Over with score {0}".format(self.score), fill="white")

    def check_collisions(self):
        """checks for collisions"""

        dots = []
        heads = []

        for agent in self.agents:
            dots.append(self.find_withtag(f"{agent.id}-dot"))
            head = self.find_withtag(f"{agent.id}-head")
            if head not in heads:
                heads.append(head)
            else:
                self.inGame = False
                return
            
        overlaps = []
        for head in heads:
            x1, y1, x2, y2 = self.bbox(head)
            overlaps.append(self.find_overlapping(x1, y1, x2, y2))
        
        for dot in dots:
            if dot in overlaps:
                self.inGame = False
                return


            
class Snake(Frame):

    def __init__(self):
        super().__init__()

        agents = [Agent(7, 'A'), Agent(7, 'B')]    
        self.master.title('Snake')
        self.board = Board(agents)
        self.pack()


def main():

    root = Tk()
    Snake()
    root.mainloop()  


if __name__ == '__main__':
    main()
