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
BUTTON_COLOR = (142, 121, 102)
BUTTON_HOVER_COLOR = (170, 150, 130)
FONT = pygame.font.Font(None, 40)
BUTTON_FONT = pygame.font.Font(None, 35)

# Initialize Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2048")

# Initialize History
history = History(5)

# Initialize Grid
grid = Grid(GRID_SIZE)
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
    
    # return button_rect
    # Draw undo button
    undo_button_rect = pygame.Rect(panel_x + 20, 220, SIDE_PANEL_WIDTH - 40, 50)
    undo_button_color = BUTTON_HOVER_COLOR if undo_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, undo_button_color, undo_button_rect)
    
    # Undo button text
    undo_button_text = BUTTON_FONT.render("Undo", True, BACKGROUND_COLOR)
    undo_button_text_rect = undo_button_text.get_rect(center=undo_button_rect.center)
    screen.blit(undo_button_text, undo_button_text_rect)
    
    return button_rect, undo_button_rect


def reset_game():
    """Resets the grid and score."""
    global grid, score
    grid = Grid(GRID_SIZE)
    score = 0
    grid.addRandomNode()
    grid.addRandomNode()

def undo():
    """Undo the last move."""
    global grid, score
    grid = history.pop()
    score = grid.score


def get_current_grid():
    """Returns the current grid."""
    global grid
    return grid

def get_max_tile():
    """Returns the maximum tile value on the grid."""
    global grid
    return grid.max_tile

def move(direction):
    """Moves the grid in the specified direction."""
    history.clear()
    print(f"Game: move: Moving {direction}")
    global grid, score
    history.push(grid)
    print(f"Game: move: Pushed {grid} to history")

    grid = deepcopy(grid)
    grid.move(direction)
    print(f"Game: move: Moved {direction}")
    score = grid.score
    print(f"Game: move: \n{grid}")

def undo():
    """Undo the last move."""
    global grid, score
    lastGrid = history.pop()
    if lastGrid:
        grid = lastGrid
        score = lastGrid.score