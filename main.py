import random as rand

SIZE = 4
global_val = 1

class Board():

    def __init__(self, SIZE):

        self.board = []
        
        for i in range(0, SIZE):
            row = []
            for j in range(0, SIZE):
                row.append(0) # Third index for value
            self.board.append(row)

    def change_dot_val(self, row, col, val):
        self.board[row][col] = val
    

class Snake():

    def __init__(self, length):
        global global_val
        # add verification on the length
        self._length = length
        self.val = global_val
        global_val = global_val + 1
        
    
    def insert_to_board(self, board):
        
        point = [rand.randint(0, SIZE-1),rand.randint(0, SIZE-1)]
        while board.board[point[0]][ point[1]] != 0:
            point[0] = rand.randint(0, SIZE-1)
            point[1] = rand.randint(0, SIZE-1)
        
        board.change_dot_val(point[0], point[1], self.val)

        # Put the snake randomly by recursive function

b = Board(SIZE)


s1 = Snake(4)
s2 = Snake(6)
s1.insert_to_board(b)
s2.insert_to_board(b)

for i in b.board:
    print(i)

