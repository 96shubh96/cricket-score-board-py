class Player:
    def __init__(self, name):
        self.name = name
        self.runs = 0
        self.fours = 0
        self.sixes = 0
        self.ballsFaced = 0
        self.out = False
        self.active = None
        self.totalOversBowled = 0
        self.runsConceded = 0
        self.wicketsTaken = 0
        self.dotBalls = 0
        self.maidenOvers = 0

    def setOut(self):
        self.out = True
        self.active = False

    def isOut(self):
        return self.out