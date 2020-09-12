from player import Player
class Team:
    def __init__(self, name, noOfPlayers):
        self.name = name
        self.noOfPlayers = noOfPlayers
        self.players = [Player(str(i+1)) for i in range(noOfPlayers)]
        self.totalRunScored = 0
        self.totalWicketDown = 0
        self.isBatting = False
        self.isBowling = False
        self.battingOrder = None
        self.strikePlayer = None
        self.nonStrikePlayer = None
        self.yetToBat = None
        self.allOut = False
        self.totalOversPlayed = None
        self.extras = 0
        self.currentBowler = None

    def isBatting(self):
        return self.isBatting
    
    def setBatting(self):
        self.isBatting = True
        self.isBowling = False

    def isBowling(self):
        return self.isBowling

    def setBowling(self):
        self.isBowling = True
        self.isBatting = False
        self.currentBowler = 0

    def wicketTaken(self):
        self.totalWicketsTaken += 1

    def setBattingOrder(self, order):
        self.battingOrder = order
        self.strikePlayer = self.battingOrder[0]-1
        self.players[self.strikePlayer].active = True
        self.nonStrikePlayer = self.battingOrder[1]-1
        self.players[self.nonStrikePlayer].active = True
        self.yetToBat = 2

    def changeStrike(self):
        self.strikePlayer, self.nonStrikePlayer = self.nonStrikePlayer, self.strikePlayer
    
    def changeBowler(self):
        self.currentBowler = (self.currentBowler+1) % self.noOfPlayers

    def recordRun(self, runs):
        self.totalRunScored += runs
        self.players[self.strikePlayer].runs += runs
        self.players[self.strikePlayer].ballsFaced += 1
        if runs == 1 or runs == 3:
            self.changeStrike()
        elif runs == 4:
            self.players[self.strikePlayer].fours += 1
        elif runs == 6:
            self.players[self.strikePlayer].sixes += 1

    def addConcededRuns(self, runs):
        if not runs:
            self.players[self.currentBowler].maidenOvers += 1
        else:
            self.players[self.currentBowler].runsConceded += runs
        self.players[self.currentBowler].totalOversBowled += 1

    def recordDotBall(self):
        if self.isBowling:
            self.players[self.currentBowler].dotBalls += 1
        else:
            self.players[self.strikePlayer].ballsFaced += 1

    def recordWicket(self):
        if self.isBowling:
            self.players[self.currentBowler].wicketsTaken += 1
        else:
            self.players[self.strikePlayer].setOut()
            self.totalWicketDown += 1
            if self.totalWicketDown == self.noOfPlayers-1:
                self.allOut = True
                return
            
            self.strikePlayer = self.battingOrder[self.yetToBat]-1
            self.players[self.strikePlayer].active = True
            self.yetToBat += 1


    def generateScorecard(self):
        print ("\nBatting Scorecard for %s:" % self.name)
        result_fields = ["Score", "4s", "6s", "Balls", "Strike Rate"]
        row_format ="{:>15}" * (len(result_fields) + 1) 
        print(row_format.format("Player Name",*result_fields))
        for player in self.players:
            strikeRate = ("%.2f" % ((player.runs/player.ballsFaced)*100) if player.ballsFaced else "0.0")
            row = [player.runs, player.fours, player.sixes, player.ballsFaced, strikeRate]
            notOutStatus = ""
            if player.active==True:
                notOutStatus = "*" 
            print(row_format.format(player.name+notOutStatus,*row))
        print("Total: %d/%d" % (self.totalRunScored, self.totalWicketDown))
        print("Extras: %s" % self.extras)

    def generateBowlingScorecard(self):
        print ("\nBowling Scorecard for %s:" % self.name)
        result_fields = ["Total Overs", "Runs Conceded", "Dot Balls", "Maiden Overs", "Wickets", "Economy"]
        row_format ="{:>15}" * (len(result_fields) + 1) 
        print(row_format.format("Player Name",*result_fields))
        for player in self.players:
            economy = ("%.2f" % (player.runsConceded/player.totalOversBowled) if player.totalOversBowled else "0.0")
            row = [player.totalOversBowled, player.runsConceded, player.dotBalls, player.maidenOvers, player.wicketsTaken, economy]
            print(row_format.format(player.name, *row))