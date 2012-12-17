"""
Kevin Carbone
Purpose:  A backtracking solver for the Sudoku puzzle.
Language: Python 3
"""

from copy import *
from sys import argv
from math import *


class SudokuConfig:
    """
    A class that represents a sudoku configuration.
        DIM - square board DIMension (int)

    """
    __slots__ = ('DIM', 'board')
    
    """The empty cell value"""
    EMPTY = 0   # can be referenced anywhere as: SkyscraperConfig.EMPTY
    def __init__(self, DIM, board):
        """
        Constructor.
        """
        
        self.DIM = DIM
        self.board = board
        
        
                    
    def __str__(self):
        """
        Return a string representation of the config.
        """
        
        # top row
        result = '  '
        result += '\n  ' + '-' * (self.DIM*2-1) + '\n'
            
        # board rows
        for row in range(self.DIM):
            result +=  '|'
            for col in range(self.DIM):
                if self.board[row][col] == SkyscraperConfig.EMPTY:
                    result += '.'
                else:
                    result += str(str(self.board[row][col]))
                if col != self.DIM-1: result += ' '
            result += '|' + '\n'
            
        # bottom row
        result += '  ' + '-' * (self.DIM*2-1) + '\n'
        result += '  '

        result += '\n'
                  
        return result

def readBoard(filename):
    """
    Read the board file.  It is organized as follows:
        DIM     # square DIMension of board (1-9)

        row 1 values    # 0 for empty, (1-DIM) otherwise
        row 2 values    # 0 for empty, (1-DIM) otherwise
        ...
    
        filename: The file name (string)
    Returns: A config (SkyscraperConfig) containing the board info from file
    """
    
    f = open(filename)
    DIM = int(f.readline().strip())
    board = list()
    for _ in range(DIM):
        line = [int(val) for val in f.readline().split()]
        board.append(line)
    f.close()
    return SudokuConfig(DIM,board)



def isGoal(config):
    """
    Checks whether a config is a goal or not
        config: The config (SkyscraperConfig)
    Returns: True if config is a goal, False otherwise
    """
    for row in range(config.DIM):
        for col in range(config.DIM):
            if config.board[row][col] == config.EMPTY:
                return False
    if isValid(config):
        return True
    return False
    
def getSuccessors(config):
    """
    Get the successors of config
        config: The config (SkyscraperConfig)
    Returns: A list of successor configs (list of SkyscraperConfig)
    """
    candidate = None
    for row in range(config.DIM):
        for col in range(config.DIM):
            if config.board[row][col] == config.EMPTY:
                candidate = row,col
                break
        if candidate != None:
            break
    successors = []
    for row in range (1,config.DIM+1):
        newConfig = deepcopy(config)
        newConfig.board[candidate[0]][candidate[1]] = row
        c = newConfig
        successors.append(c)
    return successors 
    



def check_dups(lst):
    nlst = copy(lst)
    nlst = [value for value in nlst if value != 0]
    return len(nlst)!=len(set(nlst))

def check_cols(config):

    for row in range(config.DIM):
        column = []
        for col in range(config.DIM):
            val = config.board[col][row]
            column.append(val)
        if check_dups(column) :
            return False
    return True


def check_rows(config):
    for row in config.board:
        if check_dups(row) :
            return False

    return True

def check_squares(config):
    root = int(sqrt(config.DIM))
    for i in range(0,config.DIM,root):
        for j in range(0,config.DIM,root):
            square = []
            for row in range(i,i+root):
                for col in range(j,j+root):
                    square.append(config.board[row][col])
            if check_dups(square):
                return False
    return True

        
def isValid(config):
    """
    Checks the config to see if it is valid
        config: The config (SkyscraperConfig)
    Returns: True if the config is valid, False otherwise
    """

    return check_rows(config) and check_cols(config) and check_squares(config)

        
def solve(config, debug):
    """
    Generic backtracking solver.
        config: the current config (SkyscraperConfig)
        debug: print debug output? (Bool)
    Returns:  A config (SkyscraperConfig), if valid, None otherwise
    """
    
    if isGoal(config):
        return config
    else:
        if debug: print('Current:\n' + str(config))
        for successor in getSuccessors(config):
            #print(successor)
            if isValid(successor):
                if debug: print('Valid Successor:\n' + str(successor))
                solution = solve(successor, debug)
                if solution != None:
                    return solution
    
def main():
    """
    The main program.
        Usage: python3 sudoku.py [filename debug]
            filename: The name of the board file
            debug: True or False for debug output
    """
    
    # if no command line arguments specified, prompt for the filename
    # and set debug output to False
    if len(argv) == 1:
        filename = input('Enter board file: ')
        debug = eval(input("Debug output (True or False): "))
    # otherwise, use the command line arguments
    elif len(argv) == 3:
        filename = argv[1]
        debug = eval(argv[2])
    # incorrect number of command line arguments
    else:
        print("Usage: python3 skyscraper.py [filename debug]")
        print("optional command line arguments:" )
        print("  filename: The name of the board file")
        print("  debug: True or False for debug output")
        return -1
        
    # read and display the initial board
    
    initConfig = readBoard(filename)
    print(isValid(initConfig))
    print('Initial Config:\n' + str(initConfig))
    
    # solve the puzzle
    solution = solve(initConfig, debug)
    
    # display the solution, if one exists
    if solution != None:
        print('Solution:\n' + str(solution))
    else:
        print('No solution.')
    
if __name__ == '__main__':
    main()
