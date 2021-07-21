from tkinter import Canvas


from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW
from globals import BOARD_WIDTH, BOARD_HEIGHT, BACKGROUND_COLOR, DOT_SIZE, PADDING, REGULAR_SQUARE
import random as rand



class Board(Canvas):

    def __init__(self):
        BOARD = super().__init__(width = BOARD_WIDTH, height = BOARD_HEIGHT,
                         background=BACKGROUND_COLOR, highlightthickness = 0)


        for row in range( DOT_SIZE,  BOARD_HEIGHT -  DOT_SIZE,  DOT_SIZE):
            for col in range( DOT_SIZE,  BOARD_WIDTH -  DOT_SIZE,  DOT_SIZE):
                BOARD.create_rectangle(col+PADDING, row+PADDING, col+ DOT_SIZE-PADDING,
                 row+DOT_SIZE-PADDING, fill=REGULAR_SQUARE, tag = f"{int(col/ DOT_SIZE) - 1 }-{int(row/DOT_SIZE) - 1}")

                
