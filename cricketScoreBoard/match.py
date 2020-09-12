from team import Team
from over import Over
class Match:
    def __init__(self, noOfPlayers, noOfOvers):
        self.team1 = Team("Team 1", noOfPlayers)
        self.team2 = Team("Team 2", noOfPlayers)
        self.totalOvers = noOfOvers
        self.currentOver = 0
        self.Overs = None
        self.battingTeam = None
        self.bowlingTeam = None
        self.events = {
                '1': self.takeSingle, '2': self.takeDouble, '3': self.takeTriple, 
                '4': self.takeFour, '6': self.takeSix, 'Wd': self.wideBall, 
                'Nb': self.noBall, 'W': self.takeWicket, '0': self.dotBall
        }
        self.firstBatting = None
        self.currentInning = 0
        self.inningsEnded = None
    
    def declareResult(self):
        print ("\nResult")
        
        if self.team1.totalRunScored > self.team2.totalRunScored:
            if self.firstBatting == self.team1:
                diff = self.team1.totalRunScored - self.team2.totalRunScored
                print ("%s won the match by %d runs" % (self.team1.name, diff))
            else:
                wickets = self.team1.noOfPlayers - self.team1.totalWicketDown - 1
                print ("%s won the match by %d runs" % (self.team1.name, wickets))

        elif self.team1.totalRunScored < self.team2.totalRunScored:
            if self.firstBatting == self.team2:
                diff = self.team2.totalRunScored - self.team1.totalRunScored
                print ("%s won the match by %d runs" % (self.team2.name, diff))
            else:
                wickets = self.team2.noOfPlayers - self.team2.totalWicketDown - 1
                print ("%s won the match by %d wickets" % (self.team2.name, wickets))
        else:
            print ("Match Drawn")
        print()
            
    def setFirstBatting(self, team):
        if team == 1:
            self.firstBatting = self.team1
        else:
            self.firstBatting = self.team2
    
    def setBattingOrder(self, order):
        self.battingTeam.setBattingOrder(order)

    def setBattingTeam(self, team):
        team.setBatting()
        self.battingTeam = team

    def setBowlingTeam(self, team):
        team.setBowling()
        self.bowlingTeam = team

    def startFirstInning(self):
        self.currentInning = 1
        if self.firstBatting == self.team1:
            self.resetInning(self.team1, self.team2)
        else:
            self.resetInning(self.team2, self.team1)
    
    def startSecondInning(self):
        self.currentInning = 2
        self.battingTeam, self.bowlingTeam = self.bowlingTeam, self.battingTeam
        self.resetInning(self.battingTeam, self.bowlingTeam)
        return self.declareResult()

    def resetInning(self, battingTeam, bowlingTeam):
        self.Overs = [Over() for _ in range(self.totalOvers)]
        self.currentOver = 0
        self.setBattingTeam(battingTeam)
        self.setBowlingTeam(bowlingTeam)
        print ("Batting order for %s:" % self.battingTeam.name)
        
        while True:
            try:
                order = list(map(int, input().split()))
                assert len(order)==self.battingTeam.noOfPlayers
                self.setBattingOrder(order)
            except Exception as f:
                print ("Please enter valid input")
                continue
            else:
                break

        self.inningsEnded=False
        self.startInning()
    
    def startInning(self):
        for over in range(self.totalOvers):
            print ("Starting Over %s:" % (over+1))
            currentOver = self.Overs[self.currentOver]
            while not currentOver.isOverCompleted():
                if self.inningsEnded:
                    return
                activity = input()
                while activity not in self.events.keys() and activity[-2:]!=',W':
                    print ("Please ented valid input!!")
                    activity = input()
                self.recordCurrentBall(activity)
            
    def endInnings(self):
        self.inningsEnded = True
        if self.currentOver != self.totalOvers:
            self.battingTeam.generateScorecard()
            print ("Overs %s\n" % self.battingTeam.totalOversPlayed)
            self.bowlingTeam.generateBowlingScorecard()
    
    def changeOver(self):
        self.currentOver += 1
        if self.currentOver == self.totalOvers:
            self.battingTeam.totalOversPlayed = str(self.currentOver)
            return self.endInnings()
        self.battingTeam.changeStrike()
        self.bowlingTeam.changeBowler()

    def printScoreCard(self):
        self.battingTeam.generateScorecard()
        print("Overs: %d\n" % (self.currentOver+1))
        self.bowlingTeam.generateBowlingScorecard()
        print()
        
    def recordCurrentBall(self, ball):
        self.Overs[self.currentOver].ballDelivered()
        if (ball[-2:] == ',W'):
            self.runAndOut(ball)
        else:
            self.events[ball]()
        
        #If current team has already scored more run, declare win 
        if self.currentInning == 2:
            if self.battingTeam.totalRunScored > self.bowlingTeam.totalRunScored:
                self.bowlingTeam.addConcededRuns(self.Overs[self.currentOver].totalRuns)
                ballsPlayed = self.Overs[self.currentOver].ballsCompleted
                self.battingTeam.totalOversPlayed = str(self.currentOver) + (("." + str(ballsPlayed)) if ballsPlayed<6 else "")
                return self.endInnings()
            
        if self.Overs[self.currentOver].isOverCompleted():
            self.bowlingTeam.addConcededRuns(self.Overs[self.currentOver].totalRuns)
            self.printScoreCard()
            self.changeOver()

    def takeSingle(self):
        self.battingTeam.recordRun(1)
        self.Overs[self.currentOver].addRuns(1)

    def takeDouble(self):
        self.battingTeam.recordRun(2)
        self.Overs[self.currentOver].addRuns(2)

    def takeTriple(self):
        self.battingTeam.recordRun(3)
        self.Overs[self.currentOver].addRuns(3)

    def takeFour(self):
        self.battingTeam.recordRun(4)
        self.Overs[self.currentOver].addRuns(4)

    def takeSix(self):
        self.battingTeam.recordRun(6)
        self.Overs[self.currentOver].addRuns(6)

    def dotBall(self):
        self.battingTeam.recordDotBall()
        self.bowlingTeam.recordDotBall()

    def ifOllOut(self):
        if self.battingTeam.allOut:
            print ("%s All out" % self.battingTeam.name)
            ballsPlayed = self.Overs[self.currentOver].ballsCompleted
            self.battingTeam.totalOversPlayed = str(self.currentOver) + (("." + str(ballsPlayed)) if ballsPlayed<6 else "")
            return self.endInnings()

    def takeWicket(self):
        self.battingTeam.recordWicket()
        self.bowlingTeam.recordWicket()
        return self.ifOllOut()

    def runAndOut(self, ball):
        run = int(ball[:1])
        #print(run)
        self.battingTeam.recordRun(run)
        self.takeWicket()

    def wideBall(self):
        self.battingTeam.totalRunScored += 1
        self.battingTeam.extras += 1
        self.Overs[self.currentOver].wideDelivery()

    def noBall(self):
        self.battingTeam.totalRunScored += 1
        self.battingTeam.extras += 1
        self.Overs[self.currentOver].noBallDelivery()