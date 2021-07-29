class Globals:
    def __init__(self):
        self.Tree_Depth = 0       # Determines how many steps ahead A_agents will calculate
        self.SERIAL_NUM = 0       # Serial number for each agent, each agent increase this number value in its creation
        self.BOARD_WIDTH = 450
        self.BOARD_HEIGHT = 450
        self.BOARD_PADDING = 1    # Determine the padding for each size (in DOT_SIZE units) 
        self.DELAY = 500          # Delay between the game rounds
        self.DOT_SIZE = 30
        self.PADDING = 3          # Padding for each DOT
        self.BACKGROUND_COLOR = "#4C1618"
        self.REGULAR_SQUARE = "#D8D8DC"
        self.BOARD = None         # Board global 'pointer'
        self.FORBIDDEN = -100     # The minimum reward the agent can get on forbidden action
        self.REWARDED = abs(self.FORBIDDEN) # The maximum reward the agent can get if he accomplished his goal
        self.GAME_ZONE_HEIGHT = int(self.BOARD_HEIGHT / self.DOT_SIZE) - (2 * self.BOARD_PADDING) # maintains the board's playing zone height 
        self.GAME_ZONE_WIDTH = int(self.BOARD_WIDTH / self.DOT_SIZE) - (2 * self.BOARD_PADDING) # maintains the board's playing zone width 
        self.BIG_DIS = self.GAME_ZONE_WIDTH + self.GAME_ZONE_HEIGHT # Maximum distance between agents (Manhattan distance)

    
        self.Purple = {'head' : "#D22EC2",
                  'body' : "#801B77",
                  'name' : 'Purple'}
        self.Brown = {'head' : "#FB8F78",
                 'body' : "#985545",
                 'name' : 'Brown'}
        self.Yellow = {'head' : "#FEFD49",
                  'body' : "#9B982C",
                  'name' : 'Yellow'}
        self.Blue = {'head' : "#5007C5",
                'body' : "#340177",
                'name' : 'Blue'}

        self.A_agents_colors = [self.Purple, self.Brown]
        self.E_agents_colors = [self.Yellow, self.Blue]

gl = Globals()

