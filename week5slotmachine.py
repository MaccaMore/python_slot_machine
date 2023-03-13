

#TODO/ bugs:
    #Sanitize user inputs
    #Allow changing bet amount and lines after first pull
    #Make it so user cannot bet under 0 credits
    #Program in diagonals for addtional lines
    #Make chance for X variable accessible

#Random for randomizing symbols, time for slowing down feature function
import random
import time

#This class is so that values can easily be changed
#!symbolChart and symbolMulti MUST HAVE THE SAME AMOUNT OF VALUES
class slotLine():
    symbolChart = ["X","J", "K", "Q", "1"]
    symbolMulti = [8, 3, 2, 2, 1]
    threeOfAKind = 3
    betList = [1, 2, 10, 50, 200]
    
#This class stores the game variables
class playerData():
    credit = 100
    betAmount = 0
    lines = 0
    previousWin = 0
    previousWinData = []
    freeGames = 0

#We put this as global so that both levelPull and featureFunc can call
lines = []

#This is the function that checks player input
def playerInputFunc():
    playerInput = input()
    if playerInput == "help":
        print("Commands: return/ enter, line [1-3], bet [1, 2, 10, 50], data")
    if playerInput == "":
        #I am using previousWin and total win to keep track of the winnings, so we reset for new run here
        playerData.previousWin = 0
        leverPull()
        #Split the text and reference the second word, then convert to int
    if playerInput == "line [1-3]":
        playerData.lines = int(playerInput.split()[1])
    if playerInput == "bet [.50, 2, 10, 50]":
        playerData.betAmount = int(playerInput.split()[1])
    if playerInput == "data":
        print(playerData.previousWinData)

def featureFunc():
    featureCounter = 6
    lines = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    print("FEATURE!")
    while featureCounter > 0:
        xPositions = []
        for a in range(len(lines)):
            for b in range(len(lines[a])):
                if random.random() < 0.2 and lines[a][b] != "X":
                    lines[a][b] = "X"
                    time.sleep(0.3)
                    xPositions.append([a, b])
        if len(lines) == 3:
            print(f" {lines[0]}\n {lines[1]}\n {lines[2]} \n")
        else:
            print(lines)
        featureCounter -= 1
        print(f"Feature Counter: {featureCounter}")
        
        if all(line == ["X", "X", "X"] for line in lines):
            playerData.previousWin = playerData.previousWin + 1000 * playerData.betAmount
            print("\
                   ____   __    ___  _  _  ____  _____  ____ \n\
                  (_  _) /__\  / __)( )/ )(  _ \(  _  )(_  _)\n\
                  .-_)(  /(__)\( (__  )  (  )___/ )(_)(   )(  \n\
                  \____)(__)(__)\___)(_)\_)(__)  (_____) (__) \n\
            | 1000x return and 5 free games! |")
            playerData.freeGames = 6
            break
        else:
            playerData.freeGames = sum(line.count("X") for line in lines)
            playerData.previousWin = sum(line.count("X") for line in lines) * 20 * playerData.betAmount + playerData.previousWin
            print(f"You win: {playerData.previousWin} Free Games: {playerData.freeGames}")

#This is the math behind slot
def leverPull():
    #Randomly chooses 3 from symbolChart and prints
    for a in range(playerData.lines):
        line = []
        for b in range(3):
            line.append(random.choice(slotLine.symbolChart))
        print(line)
        lines.append(line)
        #Checks if 3 of a kind
        if line[0] == line[1] == line[2]:
            playerData.previousWin = slotLine.symbolMulti[slotLine.symbolChart.index(line[0])] * playerData.betAmount * slotLine.threeOfAKind + playerData.previousWin
        #If not 3 of a kind, 2 of a kind
        if line[0] == line[1]:
            playerData.previousWin = slotLine.symbolMulti[slotLine.symbolChart.index(line[0])] * playerData.betAmount + playerData.previousWin
        #Check if they are all X if so they hit a feature
        if line[0] == line[1] == line[2] == "X":
            featureFunc()
    #If player doesnt spin 3 line and has no free games, take away credits
    if playerData.freeGames < 1:
     playerData.credit -= playerData.betAmount * playerData.lines
    else:
        playerData.freeGames = playerData.freeGames - 1
    #Check if 3 from lines are the same
   
        
  
    #Add previousWin to credit
    playerData.credit = playerData.credit + playerData.previousWin
    #Displays current status
    print(f"| Credits: {playerData.credit:.1f} | Previous Win: {playerData.previousWin * playerData.betAmount} | Bet Amount: {playerData.betAmount} | Lines: {playerData.lines} | Free Games: {playerData.freeGames} |")

    

    #Add previousWin to previousWinData list for win tracking
    playerData.previousWinData.append(playerData.previousWin)

    


print("This is a slot machine game. Type 'help' for a list of commands.")
print("You start with 100 credits. Good luck!")
#ask player how many lines they want to play
playerData.lines = int(input("How many lines would you like to play? (1-3): "))
#ask player how much they want to bet, reference list from slotLine
playerData.betAmount = int(input("How much would you like to bet?: " + str(slotLine.betList) + ": "))
#Check there are enough credits to play
if playerData.betAmount > playerData.credit:
    print("You don't have enough credits to play this high yet.")
    playerData.betAmount = int(input("How much would you like to bet?" + str(slotLine.betList) + ": "))
print("Type 'help' for commands")



#Loop for game, player inputs can be "help", "return", "line [1-3]", "bet [$.50, $2, $10, $50]"
while playerData.credit > 0:
    playerInputFunc()
else:
    print("You have no more credits. Game over.")



