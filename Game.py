import pygame
import sys
from Grid import Grid
from History import History
from copy import deepcopy

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 4  # 4x4 grid
MAX_TILE = 2048
CELL_SIZE = 100  # Cell dimensions in pixels
MARGIN = 5  # Margin between cells
GRID_WIDTH = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * MARGIN
SIDE_PANEL_WIDTH = 200
SCREEN_WIDTH = GRID_WIDTH + SIDE_PANEL_WIDTH
SCREEN_HEIGHT = GRID_WIDTH
BACKGROUND_COLOR = (187, 173, 160)
CELL_COLOR = (205, 193, 180)
FONT_COLOR = (119, 110, 101)
# BUTTON_COLOR = (142, 121, 102)
BUTTON_COLOR = (112, 91, 72)
BUTTON_HOVER_COLOR = (170, 150, 130)
FONT = pygame.font.Font(None, 40)
BUTTON_FONT = pygame.font.Font(None, 35)

# Initialize Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2048")

onGameOverScreen = False
onWinScreen = False

# Initialize History
history = History(5)
redoStack = History(5)
last_undo = False
status = "play" # play, win, gameOver, continue

# Initialize Grid
grid = Grid(GRID_SIZE, MAX_TILE)
score = grid.score  # Initialize score


def draw_grid():
    """Draws the grid on the screen."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = MARGIN + col * (CELL_SIZE + MARGIN)
            y = MARGIN + row * (CELL_SIZE + MARGIN)
            
            # Display the cell value if it
            node = grid.getNode(row, col)

            pygame.draw.rect(screen, get_tile_style(node)[1], (x, y, CELL_SIZE, CELL_SIZE))

            if node == None: # if no node in the location
                # print(f"Game: draw_grid: {row}, {col} is None")
                continue

            value = node.value

            # Debug
            if value == 0:
                # print(f"Game: draw_grid: {node} is 0")
                continue
            
            text = FONT.render(str(value), True, get_tile_style(node)[0])
            text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
            screen.blit(text, text_rect)

def draw_game_over():
    """Displays the game over screen."""
    global onGameOverScreen

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.set_alpha(128)  # Set transparency level
    overlay.fill((238, 228, 218, 200)) 
    screen.blit(overlay, (0, 0))

    # Draw "Game Over" text
    game_over_text = FONT.render("Game Over", True, BUTTON_COLOR)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(game_over_text, game_over_rect)

    # Draw restart button
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    mouse_pos = pygame.mouse.get_pos()
    button_color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, button_rect)

    # Button text
    button_text = BUTTON_FONT.render("Restart", True, (237, 224, 200))
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)

    onGameOverScreen = True

    return button_rect

def draw_win():
    """Displays the game over screen."""
    global onWinScreen

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.set_alpha(128)  # Set transparency level
    overlay.fill((238, 228, 218, 200)) 
    screen.blit(overlay, (0, 0))

    # Draw "You Win!" text
    win_text = FONT.render("You Win!", True, BUTTON_COLOR)
    win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(win_text, win_rect)

    # Draw restart button
    restart_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30, 200, 50)
    mouse_pos = pygame.mouse.get_pos()
    button_color = BUTTON_HOVER_COLOR if restart_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, restart_button_rect)

    # Button text
    button_text = BUTTON_FONT.render("Restart", True, (237, 224, 200))
    button_text_rect = button_text.get_rect(center=restart_button_rect.center)
    screen.blit(button_text, button_text_rect)

    # Draw continue button
    continue_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, 200, 50)
    continue_button_color = BUTTON_HOVER_COLOR if continue_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, continue_button_color, continue_button_rect)

    # Continue button text
    continue_button_text = BUTTON_FONT.render("Continue", True, (237, 224, 200))
    continue_button_text_rect = continue_button_text.get_rect(center=continue_button_rect.center)
    screen.blit(continue_button_text, continue_button_text_rect)

    onWinScreen = True

    return restart_button_rect, continue_button_rect

def get_tile_style(node):
    """Returns the font and background color for a tile based on its value."""
    if node == None:
        return (FONT_COLOR, CELL_COLOR)
    tile_styles = [
        ((119, 110, 101), (238, 228, 218)),  # 2
        ((119, 110, 101), (237, 224, 200)),  # 4
        ((249, 246, 242), (242, 177, 121)),  # 8
        ((249, 246, 242), (245, 149, 99)),   # 16
        ((249, 246, 242), (246, 124, 95)),   # 32
        ((249, 246, 242), (246, 94, 59)),    # 64
        ((249, 246, 242), (237, 207, 114)),  # 128
        ((249, 246, 242), (237, 204, 97)),   # 256
        ((249, 246, 242), (237, 200, 80)),   # 512
        ((249, 246, 242), (237, 197, 63)),   # 1024
        ((249, 246, 242), (237, 194, 46)),   # 2048
    ]
    index = int(node.value).bit_length() - 2
    if 0 <= index % 11 < len(tile_styles):
        return tile_styles[index % 11]
    return (FONT_COLOR, CELL_COLOR)
    # return tile_styles.get(node.value, ((249, 246, 242), (60, 58, 50)))


def draw_side_panel():
    """Draws the score and restart button on the right side."""
    panel_x = GRID_WIDTH + MARGIN
    # Draw score label
    score_label = FONT.render("Score:", True, FONT_COLOR)
    screen.blit(score_label, (panel_x + 10, 20))
    
    # Draw score value
    score_value = FONT.render(str(score), True, FONT_COLOR)
    screen.blit(score_value, (panel_x + 10, 60))
    
    # Draw restart button
    button_rect = pygame.Rect(panel_x + 20, 150, SIDE_PANEL_WIDTH - 40, 50)
    mouse_pos = pygame.mouse.get_pos()
    button_color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, button_rect)
    
    # Button text
    button_text = BUTTON_FONT.render("Restart", True, BACKGROUND_COLOR)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)
    
    # Draw undo button
    undo_button_rect = pygame.Rect(panel_x + 20, 220, SIDE_PANEL_WIDTH - 40, 50)
    undo_button_color = BUTTON_HOVER_COLOR if undo_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, undo_button_color, undo_button_rect)
    
    # Undo button text
    undo_button_text = BUTTON_FONT.render("Undo", True, BACKGROUND_COLOR)
    undo_button_text_rect = undo_button_text.get_rect(center=undo_button_rect.center)
    screen.blit(undo_button_text, undo_button_text_rect)
    
    # Draw redo button
    redo_button_rect = pygame.Rect(panel_x + 20, 290, SIDE_PANEL_WIDTH - 40, 50)
    redo_button_color = BUTTON_HOVER_COLOR if redo_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, redo_button_color, redo_button_rect)
    
    # Redo button text
    redo_button_text = BUTTON_FONT.render("Redo", True, BACKGROUND_COLOR)
    redo_button_text_rect = redo_button_text.get_rect(center=redo_button_rect.center)
    screen.blit(redo_button_text, redo_button_text_rect)
    
    return button_rect, undo_button_rect, redo_button_rect


def reset_game():
    """Resets the grid and score."""
    global grid, score, history, last_undo, status, onGameOverScreen, onWinScreen
    onGameOverScreen = False
    onWinScreen = False
    history.clear()
    last_undo = False
    status = "play"
    grid = Grid(GRID_SIZE, MAX_TILE)
    score = 0
    grid.addRandomNode()
    grid.addRandomNode()

def get_current_grid():
    """Returns the current grid."""
    global grid
    return grid

def get_max_tile():
    """Returns the maximum tile value on the grid."""
    global grid
    return grid.max_tile

def get_status():
    global status
    return status

def set_status(newStatus):
    global status
    status = newStatus

def get_onGameOverScreen():
    global onGameOverScreen
    return onGameOverScreen

def get_onWinScreen():
    global onWinScreen
    return onWinScreen

def move(direction):
    """Moves the grid in the specified direction."""
    global grid, score, history, last_undo, status

    print(f"Moving {direction}")

    if not is_move_valid(grid, direction):
        print("Invalid move")
        return
    
    if last_undo:
        history.clear()
        redoStack.clear()
        grid.prev = None
        grid.next = None
        last_undo = False
        print("Cleared history")
        print(f"Last_undo: {last_undo}")

    history.push(grid)

    # print(f"Game: move: Moving {direction}")
    # print(f"Game: move: Pushed {grid} to history")

    grid = deepcopy(grid)
    grid.move(direction)
    grid.addRandomNode()
    score = grid.score

    print(f"Moved {direction}")
    print(grid)

    if grid.hasWon() and status != "continue":
        status = "win"
        print("You Win!")
    elif grid.isGameOver():
        status = "gameOver"
        print("Game Over")

def undo():
    """Undo the last move."""
    print("Undoing last move")
    global grid, score, last_undo, history
    lastGrid = history.top
    if lastGrid != None:
        history.pop()
        redoStack.push(grid)
        grid = lastGrid
        score = lastGrid.score
        last_undo = True
        print("Last move undone")
    else:
        print("No more moves to undo")

def redo():
    """Redo the last undo."""
    print("Redoing last undo")
    global grid, score, last_undo, redoStack
    lastGrid = redoStack.top
    if lastGrid != None:
        redoStack.pop()
        history.push(grid)
        grid = lastGrid
        score = lastGrid.score
        if redoStack.top == None:
            last_undo = False
        print("Last undo redone")
    else:
        print("No more undos to redo")

def is_move_valid(somegrid, direction):
    """Returns True if the last move was valid."""

    gridCopy = deepcopy(somegrid)
    gridCopy.move(direction)
    # print(f"The grids are {'not ' if gridCopy != somegrid else ''}equal")

    return gridCopy != somegrid