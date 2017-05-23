#connect4.py
#cli connect 4 game

from connect4utils import *
from enum import Enum

#--------define game commands ------------
class Command(Enum):
    NEWGAME = 1
    QUIT = 2
    PLAYERMODE = 3
    BOARDSIZE = 4
    RESUME = 5
    PLAY = 6

    
#--------define status flags --------------
GAME_IN_PROGRESS = False
MAIN_MENU = True
SINGLE_PLAYER = True

#--------initialize game state variables --------------
current_game = None
MIN_DIM = 6
BOARD_HEIGHT = 6
BOARD_WIDTH  = 7

print('######### CONNECT-4 V2.0 ##############')

def read_mainmenu_commands():
    global GAME_IN_PROGRESS
    
    print('######### MAIN MENU ##############')
    print('1 New Game')
    print('2 Quit')
    print('3 Player Mode')
    print('4 Board Size')
    optionlist = [1,2,3,4]
    
    if GAME_IN_PROGRESS:
        print('5 RESUME')
        optionlist.append(5)
    
    command = 0
    while True:
        try:
            command = int(input('Please select an option: '))
            if command in optionlist:
                return Command(command)
            else:
                print('The selected option is not available.')
        except:
            print('Option must be an integer.')
            continue
         
            
def read_game_commands():
    global current_game
    global SINGLE_PLAYER
    
    print('######### Board View ############')
    current_game.draw(defaultdraw)
    command = -1
    optionlist = [0] + [k+1 for k in current_game.getavailmoves()]
    while True:
        
        try:
            print('Enter column number or 0 to return to main menu.')
            instr = 'Player {} >>'.format(current_game.getCurrentPlayer())
            command = int(input(instr))
            
            if command in optionlist:
                if command == 0:
                    return (Command.QUIT,None)
                else:
                    return (Command.PLAY,command)
            else:
                print('The selected move is not available.')
                continue
        except:
            print('Option must be an integer.')
            continue

def play_newgame():
    global current_game
    global BOARD_HEIGHT
    global BOARD_WIDTH
    global GAME_IN_PROGRESS
    
    current_game = SingleGame(BOARD_HEIGHT,BOARD_WIDTH)
    
    GAME_IN_PROGRESS = True
    
    play_current_game()
    

def play_current_game():
    global current_game
    global GAME_IN_PROGRESS
    global SINGLE_PLAYER
    
    while current_game.status == Status.INPROGRESS:
        
        if SINGLE_PLAYER and not current_game.player1:
                #computer's turn
                print('Your computer is playing!!')
                current_game.make_move(minimax(current_game))
                continue
        
        command = read_game_commands()
        if command[0] == Command.QUIT:
            return
        else:
            move = command[1]-1
            current_game.make_move(move)
    
    print('Player',current_game.status.value,'wins!!')
    current_game.draw(defaultdraw)
    GAME_IN_PROGRESS = False
            
            
def set_boardsize():
    global BOARD_HEIGHT
    global BOARD_WIDTH
    global MIN_DIM
    
    height = BOARD_HEIGHT
    width  = BOARD_WIDTH
    
    #set height
    while True:
        try:
            height = int(input('Enter new board height or r to return to main menu: '))
            if height < MIN_DIM:
                print("Height cannot be less than 6.")
                continue
            break
        except:
            print('Returning to main menu.')
            print('Current board size is ',BOARD_HEIGHT,'x',BOARD_WIDTH)
            return
        
    #set width
    while True:
        try:
            width = int(input('Enter new board with or r to return to main menu: '))
            if width < MIN_DIM:
                print("Width cannot be less than 6.")
                continue
            break
        except:
            print('Returning to main menu.')
            print('Current board size is ',BOARD_HEIGHT,'x',BOARD_WIDTH)
            return
    
    #set height and width
    BOARD_HEIGHT = height
    BOARD_WIDTH  = width 
    print('Board size set to ',BOARD_HEIGHT,'x',BOARD_WIDTH)

def set_playermode():
    global SINGLE_PLAYER
    
    print('########## Player Mode ###########')
    print('1 Single PLayer')
    print('2 2 PLayers')
    print('3 Return to Main Menu')
    options = [1,2,3]
    while True:
        try:
            command = int(input('Please enter an option: '))
            if command not in options:
                print('This option is not available.')
                continue
            else:
                if command == 1:
                    SINGLE_PLAYER = True
                    return
                elif command == 2:
                    SINGLE_PLAYER = False
                    return
                else:
                    return
        except:
            print('Option must be an integer!!')
            continue

#game loop
while True:
    command = read_mainmenu_commands()
        
    if command == Command.NEWGAME:
        play_newgame()
        continue
    if command == Command.QUIT:
        print('Goodbye!!')
        break
    if command == Command.PLAYERMODE:
        set_playermode()
        continue
    if command == Command.BOARDSIZE:
        set_boardsize()
        continue
    if command == Command.RESUME:
        play_current_game()
        continue




