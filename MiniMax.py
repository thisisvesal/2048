from Game import *
from Nodes.Node import Node

def eval_row(grid: Grid, row:int): # based on max tile, descending order, empty nodes in bottom rows
    score = 0
    head = grid.getRowHead(row)

    if not head:
        return 4 # the number of empty cells
    
    head = head.node

    

def evaluate(grid: Grid): # based on empty cells and max tile. Also try score
    # empty_cells = len(grid.getEmptyCells())
    # max_tile = grid.getPresentMaxValue()
    # return grid.score # can be countR1 * 4 + countR2 * 3 + countR3 * 2 + countR4 * 1 + the same thing for cols
    score = 0
    for i in range(4):
        # score += (grid.countRow(i) + grid.countCol(i))* (4 - i)
        score += (grid.countEmptyInRow(i) + grid.countEmptyInCol(i)) * i
        score += ((grid.sumOfRow(i) + grid.sumOfCol(i)) * (4 - i)) * 2

    score += grid.score # cherry on top?
    score += len(grid.getEmptyCells())

    return score

def minimax(grid: Grid, depth, maximizing):
    if depth == 0 or grid.isGameOver():  # Base case
        return evaluate(grid)
    
    # best_move = "up"
    
    if maximizing:  # AI's move
        max_eval = float('-inf')
        for move in ["up", "down", "left", "right"]:
            new_grid = simulate_move(grid, move)
            if new_grid:  # Valid move
                eval = minimax(new_grid, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    # best_move = move
        return max_eval
    else:  # Random tile generation
        min_eval = float('inf')
        # for emptyCell in grid.getEmptyCells():
        #     for tileValue in [2, 4]:
        #         new_grid = simulate_tile(grid, emptyCell, tileValue)
        #         eval = minimax(new_grid, depth - 1, True)
        #         min_eval = min(min_eval, eval)

        for tileValue in [2, 4]:
            emptyCell = grid.getUpperLeftMostEmpty()
            new_grid = simulate_tile(grid, emptyCell, tileValue)
            eval = minimax(new_grid, depth - 1, True)
            min_eval = min(min_eval, eval)

        return min_eval
    
    # so this is so funny it's so slow XD
    # what I'm thinking is maybe keep the last move,
    # and if it was like move up, try adding tiles at the bottom of each column
    # and if it's like move left, try adding tiles at the right of each row

    # actually no
    # I've played this quite a lot
    # worst case scenario is usually when like you move down and there's an empty spot at the top
    # that is, if your general strategy is keeping things to the top left

    # So that grading system of yours should change too
    # Generally, a good state is where nodes are organized from left to right, top to bottom in descending order
    # Most importantly the top row we don't really care about the other rows

    # So one way I can eval, is to subtract each two adjacent cells in the top row
    # then add these subtractions up
    # or not?
    # that would only result in leftmost of top - rightmost of top


def find_best_move(grid: Grid):
    best_move = None
    best_value = float('-inf')
    for move in ["up", "down", "left", "right"]:
        new_grid = simulate_move(grid, move)
        print(f"Simulated move {move}")
        print(new_grid)
        if new_grid:  # Valid move
            move_value = minimax(new_grid, depth=3, maximizing=False)
            if move_value > best_value:
                best_value = move_value
                best_move = move
    return best_move

def simulate_tile(grid: Grid, cell, tileValue): # Mini
    gridCopy = deepcopy(grid)

    newNode = Node(tileValue, cell[0], cell[1])
    gridCopy.addNode(newNode)
    
    return gridCopy

def simulate_move(grid: Grid, direction): # Max
    gridCopy = deepcopy(grid)

    if not is_move_valid(grid, direction):
        return None
    
    gridCopy.move(direction)
    
    return gridCopy

