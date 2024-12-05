import pygame
import sys
from Game import *
from pygame.locals import *
from Nodes.Node import Node

def start():
    # Set the game icon
    icon = pygame.transform.scale(
        pygame.image.load("images/icon.ico"), (32, 32))
    pygame.display.set_icon(icon)

    grid = get_current_grid()
    print(grid)
    # grid.add_node(Node(2, 0, 0))
    # grid.add_node(Node(2, 1, 0))
    # grid.add_node(Node(2, 2, 0))
    # grid.add_node(Node(2, 3, 0))
    grid.add_node(Node(2, 0, 2))
    print(grid)
    grid.add_node(Node(2, 0, 1))
    print(grid)


# Main Loop
def update():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == K_q):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if restart_button.collidepoint(event.pos):
                        reset_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    move("up")
                elif event.key == K_DOWN:
                    move("down")
                elif event.key == K_LEFT:
                    move("left")
                elif event.key == K_RIGHT:
                    move("right")
                elif event.key == K_u:
                    undo()

            # Draw everything
            screen.fill(BACKGROUND_COLOR)
            draw_grid()

            restart_button = draw_side_panel()

            pygame.display.flip()

start()
update()