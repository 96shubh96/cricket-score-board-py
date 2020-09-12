BALLS_DELIVERED_IN_OVER = 6
class Over:
    def __init__(self):
        self.totalBalls = BALLS_DELIVERED_IN_OVER
        self.ballsCompleted = 0
        self.totalRuns = 0

    def isOverCompleted(self):
        return self.ballsCompleted == self.totalBalls
    
    def ballDelivered(self):
        self.ballsCompleted += 1
    
    def wideDelivery(self):
        self.totalRuns+=1
        self.ballsCompleted -= 1
    
    def noBallDelivery(self):
        self.totalRuns+=1
        self.ballsCompleted -= 1

    def addRuns(self, runs):
        self.totalRuns += runs