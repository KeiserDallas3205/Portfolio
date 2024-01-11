####################
#Name: Keiser Dallas
#Date: 10/27/2023
#Class: CSC 475-001
#Assignment3: Othello
#Desc: This program is an implementation of the game 'Othello'. The game is mean't to be command-line friendly.
#           Player moves are read from the command -line, and the board is printed using ASCII art.
#           There are 2 game modes:
#
#               Single Player
#               Multiplayer
#
#           The single player game mode allows the player to choose their disc color,
#           and test their skills agains an AI opponent. The AI opponent lists it's
#           best moves, then uses the minimax search algorithm to select the best move.
#           Afterwards, the AI opponent tells the human player how many moves it considered.
#           The human player is given the option to skip if they have no avaialable moves to make.
#           Similarly, the AI opponent will skip its move if it has none to make.
#
#           The multiplayer game mode allows 2 players to play each other back in forth.
#           Players are allowed to skip if there are no available moves for them to make
#
#           Rules:
#
#           The rules are consistent with classic Othello rules. Human players are given the option to
#           skip their turn if they have no available moves. Players can flip opponent disks in all directions
#           (vertically, horizontally, and diagonally)
#
#           Move input shoould be as follows:
#                   6,4  ; where 6 is the row and 4 is the column (the comma separator is required).
#
#
#           Finally, their are 2 DEBUG modes:
#
#               Showing simulations
#               Turning alpha-beta pruning on/off
#
#           Before the AI chooses its best move, it will prompt the player to see its decision path. This
#           mode is turned off by default, but if the player chooses to they can see.
#
#           Also, the player is prompted on whether they would like to turn alpha-beta pruning off. Aplha-beta
#           pruning is turned on by defaut, but if the player chooses to they can turn it off. 
####################
import sys

#*************** GLOBAL VARIABLES *****************#

# Dimensions of board game (8x8)
boardSize = 8

player1 = 'X'

player2 = 'O'

playerOneCount = 0  # X's

playerTwoCount = 0  # O's

playThru = 0 # Number of game states considered by minimax


directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)] # Directions to check for moves
maxDepth = 3


#*************** GAME SETUP ************************#

# Initialized the board
gameBoard = [[" " for squares in range(boardSize)] for row in range(boardSize)]

# Initial game state
gameBoard[3][3] = 'X'
gameBoard[3][4] = 'O'
gameBoard[4][3] = 'O'
gameBoard[4][4] = 'X'





#************** GAME FUNCTIONS ********************#

# Function takes in a move (row,col) and the player
# Determines whether that move is valid
# Returns a boolean for the validity of the move, and a direction to move in
# ex. 1,0,False
def isValid(row,col, player):

    # Correct the board offset
    row -= 1
    col -= 1
    
    # Indicates whether the move is valid or not
    valid = False
    
    # Check for OUT OF BOUNDS ERRORS
    if((boardSize <= row < 0) or (boardSize <= row < 0)):
        return False

    # Check if spot is already taken
    if(gameBoard[row][col] != " "):
        return False
    
    # Check for valid moves in ALL directions(vertical, horizontal, and diagonal)
    for dr, dc in directions:
        
        # Starting from the desired positon, search in that direction 
        r,c = row + dr, col + dc
        
        # Checks if an opponent disc was on the searchable path
        passedOponentDisc = False
        
        # While staying in bounds of game board
        while((0 <= r < boardSize) and (0 <= c < boardSize)):
            
            # The next available spot is empty
            if(gameBoard[r][c] == " "):
                
                # You've ran out of searchable places 
                break 
            
            # The next availabe spot is a similar disc
            if(gameBoard[r][c] == player):
                
                # Check and see if you can passed AT LEAST ONE opponent disc on the way
                if(passedOponentDisc):
                    
                    # If so, That's a valid move
                    return True
                
                else:
                    
                    # If not, That's not a valid move
                    break
            
            # The next available spot is an opponent disc
            else: 
                passedOponentDisc = True
            
            # Keep searching the path, until a condition is met
            r += dr
            c += dc
            
    # If you've made it this far, then no playable move was found in ANY direction
    return False
        

# Function process player's move (row,col)
#   Adds the player disc to the specified spot
#   Then fiips any necessary opponent disc(s)
def makeMove(row,col,player):

    # Correct the board offset
    row -= 1
    col -= 1

    # Place player disc in that position
    gameBoard[row][col] = player

    # Check in all directions for opponent disc(s)
    for dr,dc in directions:

        # Starting at the next space in that direction
        r = row + dr
        c = col + dc

        # List holds the opponent disc(s) that need to be flipped
        flipList = []

        # While IN BOUNDS of the game board
        while((0 <= r < boardSize) and (0 <= c < boardSize)):

            # If the space is empty
            if(gameBoard[r][c] == " "):

                # Not a playable move
                break

            # If you reach a friendly disc
            if(gameBoard[r][c] == player):

               # And you passed opponent disc(s) on the way
               if(len(flipList) > 0):
                   

                   # Flip those opponent disc(s)
                   for fr,fc in flipList:
                       gameBoard[fr][fc] = player

                   # Stop looking in that direction 
                   break

            # If you reach an opponent disc
            else:

                # Add that coordinate to be flipped
                flipList.append((r,c))

            # Move in that direction
            r += dr
            c += dc



# Function determines whether the game is over
# Returns a boolean
def isGameOver():

    # If both players have no valid moves left
    if(((len(getValidMoves(player1)) == 0 and len(getValidMoves(player2)) == 0) or ((playerOneCount + playerTwoCount) == 64))):

        # Then the game is over
        return True
    else:

        # Game continues
        return False
    

# Function takes in a player
# Returns a list of all valid moves for that player
def getValidMoves(player):

    # Holds all possible moves for a player
    validMoves = []

    # Check each square on the board
    for row in range(1,9):
        for col in range(1,9):

            # If that position is a valid move for the player
            if(isValid(row,col,player) == True):

                # Add it to the list
                validMoves.append((row,col))
    
    # Return the list
    return validMoves


#*************** AI IMPLEMENTATION *****************#

# Function takes in a player (A.I.) and a depth to search
# Searches through the game tree til the specified depth 
# Make the best move found 
def makeBestMove(player,depth,maximizingPlayer):

    print("AI choosing its move...")

    # Access game board
    global gameBoard

    # Access play through counter & reset 
    global playThru
    playThru = 0

    # Determines if skip the whole play through
    dontShow = False

    #********* DEBUG MODE ***************#

    # Controls DEBUG mode
    DEBUG = False
    
    shouldDebug = input("Do you want to see my moves? [Y/y] or [N/n]")

    # Check for case sensitivity
    if(shouldDebug == 'y'): shouldDebug = 'Y'
    if(shouldDebug == 'n'): shouldDebug = 'N'
    
    # If they want to see
    if(shouldDebug == 'Y'):
        DEBUG = True
  
    #********** A/B PRUNING MODE ****************#

    # Controls alpha-beta pruning
    isPruning = True
    # ALPHA-BETA pruning controls
    shouldPrune = input("Pruning on [Y/y] or off [N/n]")

    # Check for case sensitivity
    if(shouldPrune == 'y'): shouldPrune = 'Y'
    if(shouldPrune == 'n'): shouldPrune = 'N'

    if(shouldPrune == 'N'):
        isPruning = False

    #********************************************#


    # Get all possible moves
    legalMoves = getValidMoves(player)

    print(f"Debug Valid Moves: {legalMoves}")
    
    # Holds the best possible move
    bestMove = None 
    
    # Maximizing player (X/BLACK)
    #if(player == 'X'):
    if(maximizingPlayer):
        
        # Set best eval
        bestEval = -sys.maxsize
        
        # Evaluate each move
        for row,col  in legalMoves:

            # DEBUG mode
            if(DEBUG):
                print(f"Simulating move: ({row},{col}) ")
            
            # Save the current game state 
            board_Copy = [row[:] for row in gameBoard]
            
            # Simulate the move
            makeMove(row,col,player)

            # Count the simulated move
            playThru += 1
            
            
            # DEBUG mode
            if(DEBUG):
                print(f"Simulated Move #{playThru}")
                printBoard()
            
                
            # Evaluate the simulated move
            evalve = minimax(gameBoard,depth,player,sys.maxsize,-sys.maxsize,maximizingPlayer,DEBUG,isPruning) 
            
            # Check to see if we found a better eval
            if(evalve > bestEval):
                
                # This is now the best move
                bestEval = evalve
                bestMove = (row,col)
            
            # Reset the game board
            gameBoard = [row[:] for row in board_Copy]
            
    # Minimizing player (O/WHITE)
    else:
    
        # Set best eval
        bestEval = sys.maxsize
        
        # Evaluate each move
        for row,col in legalMoves:

             # DEBUG mode
            if(DEBUG):
                print(f"Simulating move: ({row},{col}) ")
            
            # Save the board state
            board_Copy = [row[:] for row in gameBoard]
            
            # Simulate the move
            makeMove(row,col,player)

            # Count the simulated move
            playThru +=1


            if(DEBUG):
                print(f"Simulated Move #{playThru}")
                printBoard()
                
            
            # Evaluate the move
            evalve = minimax(gameBoard,depth,player,sys.maxsize,-sys.maxsize,maximizingPlayer,DEBUG,isPruning) 
            
            # Check to see if we found a better eval
            if(evalve < bestEval):
                
                # This is now the best move
                bestEval = evalve
                bestMove = (row,col)
            
            # Reset the game board
            gameBoard = [row[:] for row in board_Copy]
    
    # After searching all possible moves, make the best move
    if(bestMove is not None):
        
        print(f"Debug: Best Move: {bestMove}")
        makeMove(bestMove[0],bestMove[1],player)
        
        # Display the number of simulated game states 
        print(f"We considered {playThru} moves")
        print()





# Function takes in game state(array), depth, player, 
#   alpha(int), beta(int), and maxmimizing player(boolean)
# Searches from that game state until a specified depth
# Returns the evaluation of the final move (int)
def minimax(board, depth, player, alpha, beta, maximizingPlayer,DEBUG,isPruning):

    # Access game board
    global gameBoard

    # Access the play through counter & reset
    global playThru
    
    # If done searching (reached max depth)
    if(depth == 0):
        
        # return the score of that move
        return evaluateBoard(player)
    
    # Get the simulated game state
    gameBoard = [row[:] for row in board]
        
    # Grab all possible moves for player
    legalMoves = getValidMoves(player)
    
    
    # Maximizing player
    if(maximizingPlayer):
        
        # Search for the highest score
        maxEval = -sys.maxsize
        
        # Evaluate each move
        for row,col in legalMoves:
            
            # Copy the board
            board_Copy = [row[:] for row in gameBoard]
            
            # Simulate the move
            makeMove(row,col,player)

            # Count the simulated move
            playThru += 1

            
            #****** DEBUG MODE ********#
            if(DEBUG):
                print(f"Simulated Move #{playThru}")
                printBoard()
            #*************************#
            
            
            # Evaluate the simulated move
            evalve = minimax(gameBoard, depth-1,player, alpha, beta, not maximizingPlayer,DEBUG,isPruning)  # False
            
            # Check if we found a better evaluation
            maxEval = max(evalve,maxEval)
            
            # Check alpha
            alpha  = max(alpha,evalve)
            
            # Restore the game board
            gameBoard = [row[:] for row in board_Copy]
            
            # If alpha-beta pruning turned on
            if(isPruning):
                # Aplha-beta pruning 
                if(beta <= alpha):
                    break
        
        # Return the best evaluation
        return maxEval
    
    # Minimizing player
    else:
        
        # Search for the lowest score
        minEval = sys.maxsize
        
        # Evaluate each move
        for row,col in legalMoves:
            
            # Copy the board
            board_Copy = [row[:] for row in gameBoard]
            
            # Simulate the move
            makeMove(row,col,player)

            # Count the simulated move
            playThru += 1

            #****** DEBUG MODE ********#
            if(DEBUG):
                print(f"Simulated Move #{playThru}")
                printBoard()
            #*************************#

            # Evaluate the simulated move
            evalve = minimax(gameBoard, depth-1,player, alpha, beta, not maximizingPlayer,DEBUG,isPruning) # True
            
            # Check if we found a better evaluation
            minEval = min(evalve,minEval)
            
            # Check beta
            beta = min(beta,evalve)
            
            # Restore the game board
            gameBoard = [row[:] for row in board_Copy]
            
            # If alpha-beta pruning turned on
            if(isPruning):
                # Aplha-beta pruning 
                if(beta <= alpha):
                    break
        
        # Return the best evaluation
        return minEval


# Function takes in a player
# Computes a heuristic for the game state
# Returns that value(int)
def evaluateBoard(player):
    
    # Count the player discs
    playerCount = sum(row.count(player) for row in gameBoard)
    
    # Count the opponent discs
    opponentCount = sum(row.count('X' if player == 'O' else 'O') for row in gameBoard)
    
    return playerCount - opponentCount
    


#*************** OUTPUT GENERATION *****************#


# Function that prints out game board
def printBoard():
    print("", end=" ")
    
    # Print the horizontal board positions
    for i in range(1,boardSize+1):
        print(i, end= " ")
    print()
        
    # Print the board
    for row, number in zip(range(boardSize), range(1,boardSize+1)):
        # Prints the vertical board positions 
        print(number, end="")

        # Prints whats in that space on game board
        for square in range(boardSize):
            print(gameBoard[row][square], end=" ")
        print()

    print()

# Function that keeps score
def updateScore():
    # Access the player scores
    global playerOneCount
    global playerTwoCount

    # Reset the score
    playerOneCount = 0
    playerTwoCount = 0

    # Tally up the points 
    for row in gameBoard:
        for square in row:
            if(square == 'X'):
                playerOneCount += 1
            elif(square == 'O'):
                playerTwoCount += 1
    


# Function displays the score
def showScore():
    print()
    print(f"Player 1: {playerOneCount}  Player 2: {playerTwoCount}")


# Function displays game over message
def gameOver():

    # Player 1 Winner
    if(playerOneCount > playerTwoCount):
        print(f"PLAYER 1 WINS {playerOneCount} to {playerTwoCount}")
    # Player 2 Winner
    elif(playerTwoCount > playerOneCount):
        print(f"PLAYER 2 WINS {playerTwoCount} to {playerOneCount}")
    # Draw
    else:
        print(f"DRAW ! {playerOneCount} to {playerTwoCount} ")


#************** MAIN ******************#

# START GAME

# Prompt user for game mode
mode = int(input("Do you want to play single player [1], multiplayer [2]"))

# Execute the selected game mode
match mode:
    
    # Single Player Mode
    case 1: 
        
        # Prompt player to choose a disc color (BLACK or WHITE)
        choice = input("Do you want BLACK ['X' or 'x'] or WHITE ['O' or 'o'] ?")

        # Handles case sensitivity
        if(choice == 'o'): choice = 'O'
        if(choice == 'x'): choice = 'X'

        # Assign players
        match choice:

            # HUMAN -> BLACK   |    AI -> WHITE
            case 'X':
                
                # Display game board
                showScore()
                printBoard()

                while(not isGameOver()):

                    # Player 1 goes first (X / BLACK)
                    while(True):

                        # Give the player an option to skip if no playable moves
                        print("Enter (-99,-99) to skip, if no playable moves")

                        
                        row,col = map(int,input("Player 1 (X), Enter your move (row,col)").split(","))

               

                        # Checks if opponent wants to skip and if allowed 
                        if((row and col) == -99):

                            if(len(getValidMoves(player1)) == 0):
                                print("Player 1 skipped their turn")
                                break
                            
                            else:
                                print("You cannot skip, you still have a move!")
                                print(getValidMoves(player1))
                        else:

                            # Processes their move
                            if(isValid(row,col,player1) == True):

                                makeMove(row,col,player1)
                                updateScore()
                                break

                            else:
                                print("Not valid move, try again or skip!")

                    # Display board after each move
                    showScore()
                    printBoard()

                    # Player 2 goes second (O / WHITE)
                    while(True):
                            
                        # AI makes his move
                        makeBestMove(player2,maxDepth,True) 
                        updateScore()
                        break

                    # Display the board after each move
                    showScore()
                    printBoard()

                # Game over
                gameOver()
                

            case 'O':

                # Display game board
                showScore()
                printBoard()

                while(not isGameOver()):
                    # Player 1 goes first (X / BLACK) -> AI
                    while(True):
                            
                        # AI makes his move
                        makeBestMove(player1,maxDepth,False) 
                        updateScore()
                        break

                    # Display the board after each move
                    showScore()
                    printBoard()

                    # Player 2 goes second (O / WHITE)
                    while(True):

                        # Give the player an option to skip if no playable moves
                        print("Enter (-99,-99) to skip, if no playable moves")

                        
                        row,col = map(int,input("Player 2 (O), Enter your move (row,col)").split(","))

               

                        # Checks if opponent wants to skip and if allowed 
                        if((row and col) == -99):

                            if(len(getValidMoves(player2)) == 0):
                                print("Player 2 skipped their turn")
                                break
                            
                            else:
                                print("You cannot skip, you still have a move!")
                                print(getValidMoves(player2))
                        else:

                            # Processes their move
                            if(isValid(row,col,player2) == True):

                                makeMove(row,col,player2)
                                updateScore()
                                break

                            else:
                                print("Not valid move, try again or skip!")

                    # Display board after each move
                    showScore()
                    printBoard()

                # Game over
                gameOver()

    # Multiplayer Mode
    case 2:
        # Display game board
        showScore()
        printBoard()

        while(not isGameOver()):

            # Player 1 goes first (X / BLACK)
            while(True):

                # Give the player an option to skip if no playable moves
                print("Enter (-99,-99) to skip, if no playable moves")

                
                row,col = map(int,input("Player 1 (X), Enter your move (row,col)").split(","))


                # Checks if opponent wants to skip and if allowed 
                if((row and col) == -99):

                    if(len(getValidMoves(player1)) == 0):
                        print("Player 1 skipped their turn")
                        break
                    
                    else: print("You cannot skip, you still have a move!")

                else:

                    # Processes their move
                    if(isValid(row,col,player1) == True):

                        makeMove(row,col,player1)
                        updateScore()
                        break

                    else:
                        print("Not valid move, try again or skip!")

            # Display board after each move
            showScore()
            printBoard()

            # Player 2 goes second (O / WHITE)
            while(True):
                
                # Give the player an option to skip if no playable moves
                print("Enter (-99,-99) to skip, if no playable moves")

                
                row,col = map(int,input("Player 2 (O), Enter your move (row,col)").split(","))

                # Checks if opponent wants to skip and if allowed 
                if((row and col) == -99):

                    if(len(getValidMoves(player2)) == 0):
                        print("Player 2 skipped their turn")
                        break
                    
                    else: print("You cannot skip, you still have a move!")

                else:
                    
                    # Processes their move
                    if(isValid(row,col,player2) == True):

                        makeMove(row,col,player2)
                        updateScore()
                        break

                    else:
                        print("Not valid move, try again or skip!")
            

            # Display the board after each move
            showScore()
            printBoard()

        # Game over
        gameOver()


