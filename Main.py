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

    # grid.addNode(Node(4, 0, 2))
    # print(grid)
    # grid.addNode(Node(2, 0, 0))
    # print(grid)
    # grid.addNode(Node(8, 0, 3))
    # print(grid)
    # grid.addNode(Node(2, 1, 1))
    # print(grid)
    # grid.addNode(Node(4, 2, 2))
    # print(grid)
    # grid.addNode(Node(2, 3, 3))
    # print(grid)
    # grid.addNode(Node(16, 1, 2))
    # print(grid)
    # grid.addNode(Node(8, 2, 1))
    # print(grid)
    # grid.addNode(Node(4, 3, 0))
    # print(grid)

    grid.addRandomNode()
    grid.addRandomNode()


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
                    elif not get_onGameOverScreen() and not get_onWinScreen() and undo_button.collidepoint(event.pos):
                        undo()
                    elif get_onWinScreen() and continue_button.collidepoint(event.pos):
                        set_status("continue")
            elif event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    move("up")
                elif event.key == K_DOWN:
                    move("down")
                elif event.key == K_LEFT:
                    move("left")
                elif event.key == K_RIGHT:
                    move("right")
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    undo()

            # Draw everything

            screen.fill(BACKGROUND_COLOR)
            
            draw_grid()
            restart_button, undo_button = draw_side_panel()

            if get_status() == "win":
                restart_button, continue_button = draw_win()
            elif get_status() == "gameOver":
                restart_button = draw_game_over()

            pygame.display.flip()

start()
update()