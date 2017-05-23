#connect4utils.py
#provides class to handle logic for a single connect4 game
#and a default draw function to draw the board

from enum import Enum

class Status(Enum):
    INPROGRESS = -1
    TIED = 0
    PLAYER1 = 1
    PLAYER2 = 2

class SingleGame:                
    
    def __init__(self,h=6,w=7):
        self.height = h
        self.width  = w
        
        self.__board__       = [[0 for i in range(0,self.width)] for j in range(0,self.height)]
        self.__movespercol__ = [h]*w
        self.movesleft = h*w
        self.player1 = True
        self.status = Status.INPROGRESS
        self.movehistory = []

    #the draw function should be very flexible so the developer must provide it
    #draw applies the supplied draw function on the __board__ data 
    def draw(self,drawfunc):
        drawfunc(self.__board__)
    
    def getCurrentPlayer(self):
        if self.player1:
            return 1
        else:
            return 2
    
    def make_move(self,col):
        
        #check that board is not in a terminal state
        if self.status != Status.INPROGRESS:
            raise Exception('Game Over','Trying to play a finished game')
        
        
        i,j = 0,0
        
        if self.__movespercol__[col] > 0: #check that there is some space available in selected column
            #make move for selected column
            if self.player1:#get current player
                currentplayer = 1    
            else:
                currentplayer = 2
            
            i,j = self.__movespercol__[col] - 1, col 
            self.__board__[i][j] = currentplayer
            self.movehistory.append(col)
            
            #decrement available moves for column number col
            self.__movespercol__[col] -= 1
            self.movesleft -=1
            
            #check whether player wins with this move
            self.__update_status(i,j)
            
            #swap player
            self.player1 = not self.player1
            
        #otherwise return illegal move exception
        else:
            raise Exception('Illegal Move',col)
    
    def undo_move(self):#undoes the latest move
        
        if len(self.movehistory) == 0:
            raise Exception('No moves to undo')
             
        col = self.movehistory.pop()
        
        self.player1 = not self.player1
        
        self.__movespercol__[col] += 1
        
        
        i,j = self.__movespercol__[col] -1, col
        self.__board__[i][j] = 0
        
        
        self.movesleft +=1
        
        #undoing a move always causes the game to be in progress
        self.status = Status.INPROGRESS
        
    
    def __is_winning_line(self,line,player):
        count = 0
        for i in line:
            
            if i == player:
                count += 1
            else:
                count = 0 
            
            if count == 4:
                return True
            
        return False
    
    def __update_status(self,i,j):
        #check if the current player won as a result of the current move
        
        #select current player
        if self.player1:
            currentplayer = 1
        else:
            currentplayer = 2
        
        
        top    = i - 3
        bottom = i + 3
        
        #clamp top bottom
        if top < 0:#because of the range
            top = 0
        if bottom > self.height -1:
            bottom = self.height - 1
        
        
        left  = j - 3
        right = j + 3
        
        #clamp
        if left < 0:
            left = 0
        
        if right > self.width -1:
            right = self.width - 1
        
        #----------------check column--------------------
        
        #get elements of column j
        column = (self.__board__[k][j] for k in range(top,bottom + 1))
        
        if self.__is_winning_line(column,currentplayer):
            self.status = Status(currentplayer)
            return
        
        #-----------------check row---------------------
        
        #count current player's chips
        row = (self.__board__[i][k] for k in range(left,right + 1))
        
        if self.__is_winning_line(row,currentplayer):
            self.status = Status(currentplayer)
            return
        
        #----------------check top-down diagonal-------------------
        d1 = min(abs(top - i) ,abs(left - j))
        d2 = min(abs(bottom - i) ,abs(right - j))
        
        start_i = i - d1
        end_i   = i + d2
        
        start_j = j - d1
        end_j   = j + d2
        
        diagonal1 =  (self.__board__[k][l] for k,l in zip(range(start_i,end_i + 1),range(start_j,end_j + 1)))
        
        if self.__is_winning_line(diagonal1,currentplayer):
            self.status = Status(currentplayer)
            return
        
        
        #----------------check bottom-up diagonal------------------
        d1 = min(abs(bottom - i) ,abs(left - j))
        d2 = min(abs(top - i) ,abs(right - j))
        
        start_i = i + d1
        end_i   = i - d2
        
        start_j = j - d1
        end_j   = j + d2
        
        diagonal2 =  (self.__board__[-k][l] for k,l in zip(range(-start_i,-(end_i - 1)),range(start_j,end_j + 1)))
        
        if self.__is_winning_line(diagonal2,currentplayer):
            self.status = Status(currentplayer)
            return
        
        #-----------------check whether there's a TIE---------------------------------
        if self.movesleft == 0 and self.status == Status.INPROGRESS:
            self.status = Status.TIED
            return
    
    def getavailmoves(self):
        availmoves = []
        for i in range(0,self.width):
            if self.__movespercol__[i] > 0 :
                availmoves.append(i)
        
        return availmoves


def defaultdraw(board):
    symbols = ['-','X','O']
    
    #print header
    for i in range(1,len(board[0]) + 1):
        print(i,end=' ')
    
    print('\n')
    
    #print board
    for j in board:
        for i in j:
            print(symbols[i],end=' ')
        
        print('\n')
        
        
def min_score(game,maxdepth):
    
    #check base cases
    if game.status != Status.INPROGRESS:
        return score_terminal(game),0
    
    if maxdepth == 0:
        return 0,0
    
    #-----------------find the lowest maximum------------
    lowest_max = 100
    lowest_max_move = 100
    
    for move in game.getavailmoves():
        game.make_move(move)
        #print('trying move',move)
        #game.draw(defaultdraw)
        tempmax = max_score(game,maxdepth - 1)[0]
        #print('had score of',tempmax)
        game.undo_move()
        if tempmax < lowest_max:
            lowest_max = tempmax
            lowest_max_move = move
    
    return lowest_max,lowest_max_move

def max_score(game,maxdepth):
    
    #check base cases
    if game.status != Status.INPROGRESS:
        return score_terminal(game) , 0
    
    if maxdepth == 0:
        return score_board(game),0
    
    #-----------------find the highest minimum------------
    highest_min   = -100
    highest_min_move = -1
    for move in game.getavailmoves():
        game.make_move(move)
        #print('trying move',move)
        #game.draw(defaultdraw)
        tempmin = min_score(game,maxdepth-1)[0]
        #print('had score of',tempmin)
        game.undo_move()
        if tempmin > highest_min:
            highest_min = tempmin
            highest_min_move = move
    
    return highest_min,highest_min_move

def score_terminal(game):
    
    if game.status == Status.PLAYER1:
        return -100
    if game.status == Status.PLAYER2:
        return 100
    else:
        return 0
            
def score_board(game):
    '''
    A simple heuristic to evaluate the board position
    It encourages minimax to take better position when not in terminal state
    Gives or subtracts one point for each open line of three
    '''
    score = 0
    window = []
    
    #-------evaluate row wise-----------
    
    for i in range(0,game.height):
        #init window for the row
        window = [game.__board__[i][0]**3,
                  game.__board__[i][1]**3,
                  game.__board__[i][2]**3]
        for j in range(3,game.width):
            window.append(game.__board__[i][j]**3)
            tempsum = sum(window)
            window.pop(0)
            if tempsum == 3*(2**3):
                score += 1
                continue
            if tempsum == 3:
                score -= 1
                continue
            
    #-------evaluate columnwise------------
    window = []
    for j in range(0,game.width):
        #init window for current column
        window = [game.__board__[0][j]**3,
                  game.__board__[1][j]**3,
                  game.__board__[2][j]**3]
        for i in range(3,game.height):
            window.append(game.__board__[i][j]**3)
            tempsum = sum(window)
            window.pop(0)
            if tempsum == 3*(2**3):
                score += 1
                continue
            if tempsum == 3:
                score -= 1
                continue
    
    #--------evaluate top down diagonal---------------
    window = []
    #do the diagonals that start on the left side
    for i in range(0,game.height - 4 + 1):
        #take first 3
        window = [game.__board__[i][0]**3,
                  game.__board__[i+1][1]**3,
                  game.__board__[i+2][2]**3]
        k = 3
        while i + k < game.height and i+k < game.width:
            
            window.append(game.__board__[i+k][k]**3)
            tempsum = sum(window)
            window.pop(0)
            if tempsum == 3*(2**3):
                score += 1
            if tempsum == 3:
                score -= 1
            
            k+=1
    
    #do the diagonals starting at the top
    for j in range(1,game.width - 4 + 1):
        #take first 3
        window = [game.__board__[0][j]**3,
                  game.__board__[1][j+1]**3,
                  game.__board__[2][j+2]**3]
        
        k = 3
        while j + k < game.height and j+k < game.width:
            
            window.append(game.__board__[k][j+k]**3)
            tempsum = sum(window)
            window.pop(0)
            if tempsum == 3*(2**3):
                score += 1
            if tempsum == 3:
                score -= 1
            
            k+=1
    
    #--------evaluate bottom up diagonal---------------
    window = []
    #do the diagonals that start on the right side
    for i in range(0,game.height - 4 + 1):
        #take first 3
        window = [game.__board__[i][-1]**3,
                  game.__board__[i+1][-2]**3,
                  game.__board__[i+2][-3]**3]
        k = 3
        while i + k < game.height and -1 - k > 0:
            
            window.append(game.__board__[i+k][-1 - k]**3)
            tempsum = sum(window)
            window.pop(0)
            if tempsum == 3*(2**3):
                score += 1
            if tempsum == 3:
                score -= 1
            
            k+=1
    
    #do the diagonals starting at the top
    for j in range(3,game.width - 1):
        #take first 3
        window = [game.__board__[0][j]**3,
                  game.__board__[1][j-1]**3,
                  game.__board__[2][j-2]**3]
        
        k = 3
        while j + k < game.height and j-k > 0:
            
            window.append(game.__board__[k][j-k]**3)
            tempsum = sum(window)
            window.pop(0)
            if tempsum == 3*(2**3):
                score += 1
            if tempsum == 3:
                score -= 1
            
            k+=1
    
    return score
    
        
#implement minimax 
def minimax(game):
    '''
    game is a SingleGame instance
    Selects a reasonable next move for the given game
    '''
    return max_score(game,4)[1]