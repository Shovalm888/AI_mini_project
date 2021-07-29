from tkinter import *
from agents_game import Agent_Snake


def main():

    root = Tk()
    Agent_Snake(root, 1, 1, 3, 3)
    root.mainloop()  




if __name__ == '__main__':
    main()

