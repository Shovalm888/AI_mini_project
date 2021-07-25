class Globals:
    def __init__(self):
        self.Tree_Depth = 2
        self.SERIAL_NUM = 0
        self.BOARD_WIDTH = 450
        self.BOARD_HEIGHT = 450
        self.BOARD_PADDING = 2 # in squers units
        self.DELAY = 1000
        self.DOT_SIZE = 30
        self.PADDING = 3
        self.BACKGROUND_COLOR = "#4C1618"
        self.REGULAR_SQUARE = "#D8D8DC"
        self.BOARD = None
        self.updated_agent={}
        self.ForbiddenBiteReward = -100
        self.ForbiddenDirectionReward = -200
        self.FORBBIDEN = -100
    
        self.Purple = {'head' : "#D22EC2",
                  'body' : "#801B77"}
        self.Yellow = {'head' : "#FEFD49",
                  'body' : "#9B982C"}
        self.Blue = {'head' : "#5007C5",
                'body' : "#340177"}
        self.Brown = {'head' : "#FB8F78",
                 'body' : "#985545"}


    def set_board(self, var):
        """ 
        devide the board to squars, leave 1 square padding in each side and save\n
        each square under specific tag, e.g. : 3-2 , when 3 represents the column\n
        and 2 the row (like [x, y])
         """
        self.BOARD = var

        for row in range( self.DOT_SIZE,  self.BOARD_HEIGHT -  self.DOT_SIZE,  self.DOT_SIZE):
            for col in range( self.DOT_SIZE,  self.BOARD_WIDTH -  self.DOT_SIZE,  self.DOT_SIZE):
                self.BOARD.create_rectangle(col+self.PADDING, row+self.PADDING, col+ self.DOT_SIZE-self.PADDING,
                    row+self.DOT_SIZE-self.PADDING, fill=self.REGULAR_SQUARE, tag = f"{int(col/ self.DOT_SIZE) - 1 }-{int(row/self.DOT_SIZE) - 1}")

    def get_board(self):
        return self.BOARD

gl = Globals()


def possible_points(head_pos, forbidden_pos = []): # expect to get nested arrays for several agents
    """
    ##### input :
    * head_pos -> head point, e.g. [?,?]
    * forbidden_pos -> list of forbidden points.

    e.g.  [ [?,?]  , [?,?] , [?,?] ]   =||= EMPTY
    
    ##### output : 
    * list of points with reward in each one, e.g.  [ [?,?,reward] , [?,?,reward] ]
    * reward == -100 in case that the point was in forbbiden points
    * reward == -200 in case of suicide (go into the wall)
    """

    width = int(gl.BOARD_WIDTH / gl.DOT_SIZE) - 2
    height = int(gl.BOARD_HEIGHT / gl.DOT_SIZE) - 2

    points_with_rew = [
        [head_pos[0] - 1, head_pos[1], 0],
        [head_pos[0] + 1, head_pos[1], 0],
        [head_pos[0], head_pos[1] - 1, 0],
        [head_pos[0], head_pos[1] + 1, 0]
    ]

    for point in points_with_rew:
        if point[0] < 0 or point[0] >= width or point[1] < 0 or point[1] >= height:
            point[2] += gl.ForbiddenDirectionReward
        elif point in forbidden_pos:
            point[2] += gl.ForbiddenBiteReward

    return points_with_rew    
   