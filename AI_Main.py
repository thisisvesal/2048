import pygame
from pygame.locals import *
from MiniMax import *
import sys

'''

This is an AI player for 2048.
It is usually able to reach 1024 (~90% of the time in my tests),
And it can sometimes reach 2048 (~40% to 50% of the time in the tests that I ran)

'''

def start():
    print("2048 by Vesal")
    # Set the game icon
    icon = pygame.transform.scale(
        pygame.image.load("images/icon.ico"), (32, 32))
    pygame.display.set_icon(icon)

    grid.addRandomNode()
    grid.addRandomNode()
    
def update():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == K_q):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    if get_status() != "addict" and restart_button.collidepoint(event.pos):
                        reset_game()
                    elif not get_onGameOverScreen() and not get_onWinScreen() and undo_button.collidepoint(event.pos):
                        undo()
                    elif not get_onGameOverScreen() and not get_onWinScreen() and redo_button.collidepoint(event.pos):
                        redo()

        # Draw everything:
        screen.fill(BACKGROUND_COLOR)
        draw_grid()
        restart_button, undo_button, redo_button = draw_side_panel()

        if get_status() == "play":
            best_move = find_best_move(get_current_grid())
            move(best_move)
        elif get_status() == "win":
            restart_button, continue_button = draw_win()
        elif get_status() == "gameOver":
            restart_button = draw_game_over()

        pygame.display.flip()

start()
update()
