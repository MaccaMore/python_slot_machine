#TODO
    # Program in diagonals for additional lines
        # When user puts only 1 or 2 lines, all 3 lists should be diplayed still
        # up to 5 lines possible
    # I am happy with the version of the build. No major bugs. Do not think I am learning much more from this project.
        # Maybe in future I will come back to this and add the extra lines. I need to working on another project.
    # The only thing I can work on now is ensuring the odds are fair. I will write data to file and analyse it

    #Work out better odds for game, I want the player to eventually lose

    # Allow specify chance of a particular symbol #A: Done
        #For example X should have lower chance to show
    # Make player bar scale #A: DONE
        # Read how many total characters for 'credit' 'betAmount' 'previous win' and print more '__'
    # Add more ASCII art

    # A : Can we modularise counting previous win totals and credit won into their own seperate functions
        # This would allow for easier debugging and readability
#BUG
    # I found a bug, could still bet under 0 credits. This occurrred because although it was checking enough credits, it was not checking for the * lines

import random
import time



# This class is so that values can easily be changed
# !symbolChart and symbolMulti and symbolChance MUST HAVE THE SAME AMOUNT OF VALUES
# !symbolChance does not have to equal 100, takes the sum and select a random number between them
class slotLine:
    symbolChart = ["🏧", "❎", "💟", "🈸"]
    symbolMulti = [5, 4, 3, 1]
    symbolChance = [20, 15, 25, 40]
    threeOfAKind = 2
    betList = [1, 2, 10, 50, 200]


# This class stores the game variables
class playerData:
    credit = 0
    betAmount = 0
    lines = 0
    previousWin = 0
    previousWinData = []
    freeGames = 0
    hasFeature = False # fixes bug when getting feature # A : NICE, boolean flags are a good way to control stuff

# This is the function that checks player input
def playerInputFunc():
    while True:
        playerInput = None # A: Reset playerInput to None to stop it from being used from previous loop
        try:
            if playerData.credit <= 0:
                print("You have no credits left. Game over.")
                break
            playerInput = input(" Return to pull lever, or type 'help': ")
            if playerInput == "help":
                print("Commands: return/ enter, change lines, change bet, data")
                continue
            if playerInput == "" and playerData.betAmount * playerData.lines <= playerData.credit:
                playerData.previousWin = 0
                leverPull()
                continue
            if playerInput == "" and playerData.betAmount * playerData.lines >= playerData.credit:
                print("You don't have enough credits, change your bet amount.")
                continue
            if playerInput == "change lines":
                # A: split here is unnecessary, we can just call the chooseLines function
                playerData.lines = chooseLines()
                continue
            if playerInput == "change bet":
                # A: split here is unnecessary, we can just call the makeBet function
                playerData.betAmount = makeBet()
                continue
            if playerInput == "data":
                print(playerData.previousWinData)
                continue
            else:
                #throw an exception
                raise ValueError
        except ValueError:
            print("Please enter a valid command. Type 'help' for a list of commands.")
            continue
    

# A : User input for lines function
def chooseLines():
    # ask player how many lines they want to play
    try:
        lines = int(input("How many lines would you like to play? (1-3): "))
        if lines < 1 or lines > 3:
            raise ValueError # A: prevents the user from entering a number outside of the range
    except ValueError:
        print("Please enter a valid number.")
        return chooseLines()
    if playerData.lines > 3:
        print("You can only play up to 3 lines.")
        return chooseLines() # recursively calls chooseLines until a valid input is passed
    return lines


# A : User input for bet function
def makeBet():
    # ask player how much they want to bet, reference list from slotLine
    if (playerData.freeGames > 0): # A: This should fix being able to change bet amount when you have free games
        print("You have free games remaining. You must play them before changing your bet.") #Oh no this broke the game, it makes it so they can have a bet amount of null lmao
        return playerData.betAmount
    try:
        betAmount = int(input("How much would you like to bet?: " + str(slotLine.betList) + ": "))
        if betAmount not in slotLine.betList:
            raise ValueError
    except ValueError:
        print("Please enter a valid number.")
        return makeBet()
    if betAmount * playerData.lines >= playerData.credit:
        print("You don't have enough credits to play this high.")
        return makeBet() # recursively calls makeBet until a valid input is passed
    return betAmount


def startGame():
    print("This is a slot machine game. Type 'help' for a list of commands.")
    print("You start with 100 credits. Get 3 🏧 in a row for feature. Good luck!")
    playerData.credit = 100 # A: here to allow for modulation of code

    playerData.betAmount = makeBet() # A: this is a good way to handle user input

    playerData.lines = chooseLines()

    playerInputFunc() # A: Call for user input controlling game


# A: I think in order to handle this it needs to be split in to 3 lists, not a list of lists.
# A: Means a rewrite of entire featureFunc I think. Can use code from leverPull
def featureFunc(lines):
    featureCounter = 5
    print(" " * 19 +"FEATURE!")
    time.sleep(1)
    print("\n" * 6)
    lines = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    while featureCounter > 0:
        xPositions = []
        for a in range(len(lines)): # This line generates an int from 0-9 (length of lines) stored in 'a', it also loops for the length of this int
            if random.random() < 0.5 and lines[a] != "$": #If number in the 'a' list are not $
                for b in range(len(lines[a])): # This line generates an int from 0-'a' stored in 'b'. Iterates over the characters in the 'a' list
                    if random.random() <.5 and lines[a][b] != "$": 
                        lines[a][b] = "$"
                        xPositions.append((a, b)) # I should think of a as rows, b as columns

        row_check = 0
        for row in lines:
            print(" " * 17 + "___________")
            print(" " * 16 + f"[ {' | '.join(row)} ]")
            if row_check < 2:
                print(" " * 17 + "‾‾‾‾‾‾‾‾‾‾‾")
        row_check += 1
        print(" " * 13 + f"~Feature Counter: {featureCounter}~")
        time.sleep(.7)
        print("\n" * 7)
        featureCounter -= 1

        if all(line == ["$", "$", "$"] for line in lines):
            playerData.previousWin = playerData.previousWin + 150 * playerData.betAmount
            print("\n" * 6)
            print(f"\
   ____   __    ___  _  _  ____  _____  ____ \n\
  (_  _) /__\  / __)( )/ )(  _ \(  _  )(_  _)\n\
 .-_)(  /(__)\( (__  )  (  )___/ )(_)(   )(  \n\
 \____)(__)(__)\___)(_)\_)(__)  (_____) (__) \n\
  ~~~~ 150x return  and   5 free games! ~~~~")
            time.sleep(2)
            playerData.freeGames = 5
            break
    playerData.previousWin += sum(line.count("$") for line in lines) * 4 * playerData.betAmount


# This is the math behind slot
def leverPull():
    playerData.hasFeature = False
    lines = []
    print(" \n \n")
    print(" " * 16 +"______________")
    # Randomly chooses 3 from symbolChart and prints
    for a in range(playerData.lines):
        line = []
        for b in range(3):
        #ma
            line.append(random.choices(slotLine.symbolChart, weights=slotLine.symbolChance)[0])
        print('               [ ' + ' | ' .join(line) + ' ]')
        time.sleep(0.2)
        lines.append(line)
        # Checks if 3 of a kind
        if line[0] == line[1] == line[2]:
            playerData.previousWin = slotLine.symbolMulti[slotLine.symbolChart.index(
                line[0])] * playerData.betAmount * slotLine.threeOfAKind + playerData.previousWin
        # If not 3 of a kind, 2 of a kind
        elif line[0] == line[1]:
            playerData.previousWin = slotLine.symbolMulti[slotLine.symbolChart.index(
                line[0])] * playerData.betAmount + playerData.previousWin
        # Check if they are all X if so they hit a feature
        if line[0] == line[1] == line[2] == "🏧":
             playerData.hasFeature = True

    print(" " * 16 + "‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
    if playerData.hasFeature == True:
        featureFunc(lines)

    if playerData.freeGames < 1:
        playerData.credit -= playerData.betAmount * playerData.lines
    else:
        playerData.freeGames = playerData.freeGames - 1
    
    # Add previousWin to credit
    playerData.credit = playerData.credit + playerData.previousWin
    # Displays current status
    print(" " + ("_" * 44))
    print(f"| Credits: {playerData.credit:.1f} | Previous Win: {playerData.previousWin}".ljust(45) + "|")
    print(f"| Bet Amount: {playerData.betAmount} | Lines: {playerData.lines} | Free Games: {playerData.freeGames}" .ljust(45) + "|")
    print(" " + "‾" * 44)

    # Add previousWin to previousWinData list for win tracking
    # Instead of storing previous win here, I store what the multiplier would have been. IE previouswin = 180/ 10 / 3 = 6 per 1 credit bet 
    playerData.previousWinData.append(round(playerData.previousWin/(playerData.betAmount/playerData.lines), 2))
    lines = []

startGame()