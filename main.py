from globals import gl
from tkinter import *
from Agent import *
from agents_game import Agent_Snake


# _name => private (method and variable both)
# __name => replaces with _classname__name to avoid names overlapping


def main():

    root = Tk()
    Agent_Snake(root)
    root.mainloop()  




if __name__ == '__main__':
    main()

