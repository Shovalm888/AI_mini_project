class Globals:
    def __init__(self):
        self.SERIAL_NUM = 0
        self.BOARD_WIDTH = 450
        self.BOARD_HEIGHT = 450
        self.DELAY = 500
        self.DOT_SIZE = 30
        self.PADDING = 3
        self.BACKGROUND_COLOR = "#4C1618"
        self.REGULAR_SQUARE = "#D8D8DC"
        self.BOARD = None
        self.updated_agent={}
    
        self.Purple = {'head' : "#D22EC2",
                  'body' : "#801B77"}
        self.Yellow = {'head' : "#FEFD49",
                  'body' : "#9B982C"}
        self.Blue = {'head' : "#5007C5",
                'body' : "#340177"}
        self.Brown = {'head' : "#FB8F78",
                 'body' : "#985545"}
    def set_board(self, var):

        self.BOARD = var

        for row in range( self.DOT_SIZE,  self.BOARD_HEIGHT -  self.DOT_SIZE,  self.DOT_SIZE):
            for col in range( self.DOT_SIZE,  self.BOARD_WIDTH -  self.DOT_SIZE,  self.DOT_SIZE):
                self.BOARD.create_rectangle(col+self.PADDING, row+self.PADDING, col+ self.DOT_SIZE-self.PADDING,
                    row+self.DOT_SIZE-self.PADDING, fill=self.REGULAR_SQUARE, tag = f"{int(col/ self.DOT_SIZE) - 1 }-{int(row/self.DOT_SIZE) - 1}")

    def get_board(self):
        return self.BOARD

gl = Globals()

def possible_points(head_pos, self_body_pos):
    
    width = int(gl.BOARD_WIDTH / gl.DOT_SIZE) - 2
    height = int(gl.BOARD_HEIGHT / gl.DOT_SIZE) - 2

    directions = []

    if head_pos[0] > 0:
        directions.append([-1, 0])
    if head_pos[0] < width - 1:
        directions.append([1, 0])
    if head_pos[1] > 0:
        directions.append([0, -1])
    if head_pos[1] < height - 1:
        directions.append([0, 1])

    # Agent can not bite himself
    to_ret = []
    
    for tmp in directions:
        if [tmp[0]+head_pos[0], tmp[1]+head_pos[1]] not in self_body_pos:
            to_ret.append([tmp[0]+head_pos[0], tmp[1]+head_pos[1]])

    return to_ret