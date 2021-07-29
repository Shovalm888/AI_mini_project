from tkinter import Canvas
from globals import gl


class Board:

    def __init__(self, root):
        canvas = Canvas(root, width = gl.BOARD_WIDTH, height = gl.BOARD_HEIGHT,
                         background=gl.BACKGROUND_COLOR, highlightthickness = 0)
        
        self.set_board(canvas)


    def set_board(self, canvas):
        """ 
        devide the board to squars, leave 1 square padding in each side and save\n
        each square under specific tag, e.g. : 3-2 , when 3 represents the column\n
        and 2 the row (like [x, y])
         """
        gl.BOARD = canvas

        for row in range( gl.DOT_SIZE,  gl.BOARD_HEIGHT -  gl.DOT_SIZE,  gl.DOT_SIZE):
            for col in range( gl.DOT_SIZE,  gl.BOARD_WIDTH -  gl.DOT_SIZE,  gl.DOT_SIZE):
                gl.BOARD.create_rectangle(col+gl.PADDING, row+gl.PADDING, col+ gl.DOT_SIZE-gl.PADDING,
                    row+gl.DOT_SIZE-gl.PADDING, fill=gl.REGULAR_SQUARE, tag = f"{int(col/ gl.DOT_SIZE) - 1 }-{int(row/gl.DOT_SIZE) - 1}")
