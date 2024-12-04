import pygame
import sys
from Game import *

# Main Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if restart_button.collidepoint(event.pos):
                    reset_game()

    # Draw everything
    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    restart_button = draw_side_panel()
    pygame.display.flip()
