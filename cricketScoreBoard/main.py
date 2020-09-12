from match import Match

if __name__ == '__main__':
    print ("No of Players for each team: ")
    noOfPlayers = int(input())
    while noOfPlayers <=1:
        print ("Enter valid input for No of Players, players must be more than 1")
        noOfPlayers = int(input())
    
    print ("No of Overs: ")
    overs = int(input())
    while overs <=0:
        print ("Enter valid input for No of Overs, it must be atleast 1")
        overs = int(input())

    match = Match(noOfPlayers, overs)
    
    print ("Which team will bat first ? Please choose either 1 or 2")
    ans = int(input())
    match.setFirstBatting(ans)
    match.startFirstInning()
    
    print ("1st Inning ended")
    print ("Starting 2nd Inning...")
    match.startSecondInning()



