from Game import *
from Nodes.Node import Node

def evaluate(grid: Grid): # Basically gives higher scores to grids with large tiles in the upper left,
                            # among other things
    if grid.hasWon():
        return float('inf')
    
    size = grid.size
    
    score = 0
    for i in range(size):
        score += grid.countEmptyInRow(i) * i * 2
        score += grid.countEmptyInCol(i) * i
        score += grid.sumOfRow(i) * (size - i) * 2
        score += grid.sumOfCol(i) * (size - i)

    score += grid.score
    score += len(grid.getEmptyCells())

    return score

def minimax(grid: Grid, depth, maximizing):
    if depth == 0 or grid.isGameOver():  # Base case
        return evaluate(grid)
    
    if maximizing:  # AI's move
        max_eval = float('-inf')
        for move in ["up", "down", "left", "right"]:
            new_grid = simulate_move(grid, move)
            if new_grid:  # Valid move
                eval = minimax(new_grid, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
        return max_eval
    else: # Tile spawn
        min_eval = float('inf')

        for tileValue in [2, 4]:
            emptyCell = grid.getUpperLeftMostEmpty() # Because if you like to keep the tiles to up and left like me,
                                                     # this is the most awful place for a new tile
                                                     # And, because it's a huge boost of performance to not check every possible case for a new tile
            new_grid = simulate_tile(grid, emptyCell, tileValue)
            eval = minimax(new_grid, depth - 1, True)
            min_eval = min(min_eval, eval)

        return min_eval


def find_best_move(grid: Grid):
    best_move = None
    best_value = float('-inf')
    for move in ["up", "down", "left", "right"]:
        new_grid = simulate_move(grid, move)
        if new_grid:  # Valid move
            move_value = minimax(new_grid, depth=3, maximizing=False)
            if move_value > best_value:
                best_value = move_value
                best_move = move
    return best_move

def simulate_tile(grid: Grid, cell, tileValue): # Mini: Where the game throws in a new tile
    gridCopy = deepcopy(grid)

    newNode = Node(tileValue, cell[0], cell[1])
    gridCopy.addNode(newNode)
    
    return gridCopy

def simulate_move(grid: Grid, direction): # Max: Where we move so we boost our score
    gridCopy = deepcopy(grid)

    if not is_move_valid(grid, direction):
        return None
    
    gridCopy.move(direction)
    
    return gridCopy

