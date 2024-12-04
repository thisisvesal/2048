import pygame
import sys
from Grid import Grid

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 4  # 4x4 grid
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

# Initialize Grid
grid = Grid(GRID_SIZE)
score = 0  # Initialize score


def draw_grid():
    """Draws the grid on the screen."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = MARGIN + col * (CELL_SIZE + MARGIN)
            y = MARGIN + row * (CELL_SIZE + MARGIN)
            pygame.draw.rect(screen, CELL_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
            
            # Display the cell value if it's not 0
            node = grid.get(row, col)
            if node == None: # if no node in the location
                continue

            value = node.value

            # Debug
            if value == 0:
                print(f"Game: draw_grid: Node at {row}, {col} is 0")
                continue
            
            text = FONT.render(str(value), True, FONT_COLOR)
            text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
            screen.blit(text, text_rect)


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
    
    return button_rect


def reset_game():
    """Resets the grid and score."""
    global grid, score
    grid = Grid(GRID_SIZE)
    score = 0


def get_current_grid():
    """Returns the current grid."""
    return grid