import pygame
import sys
from Game import *
from Nodes.Node import Node

def start():
    # Set the game icon
    icon = pygame.transform.scale(
        pygame.image.load("images/icon.ico"), (32, 32))
    pygame.display.set_icon(icon)

    grid = get_current_grid()
    grid.add_node(Node(2, 0, 0))
    grid.add_node(Node(2, 1, 0))
    grid.add_node(Node(2, 2, 0))
    grid.add_node(Node(2, 3, 0))
    grid = get_current_grid()
    newCell = grid.get_random_empty_cell() 
    x = newCell[0]
    y = newCell[1]
    print(x, y)
    grid.add_node(Node(2, x, y))


# Main Loop
def update():
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

start()
update()