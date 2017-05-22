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