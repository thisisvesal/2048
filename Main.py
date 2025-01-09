import pygame
import sys
from Game import *
from pygame.locals import *

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
                    elif get_onGameOverScreen() and not get_onWinScreen() and undo_button.collidepoint(event.pos):
                        undo()
                        set_status("play")
                    elif not get_onGameOverScreen() and not get_onWinScreen() and undo_button.collidepoint(event.pos):
                        undo()
                    elif not get_onGameOverScreen() and not get_onWinScreen() and redo_button.collidepoint(event.pos):
                        redo()
                    elif get_onWinScreen() and continue_button.collidepoint(event.pos):
                        set_status("continue")
                    elif get_status() == "addict" and get_onGameOverScreen() and quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            elif event.type == pygame.KEYDOWN and not get_onGameOverScreen() and not get_onWinScreen():
                if event.key == K_UP or event.key == K_w:
                    move("up")
                elif event.key == K_DOWN or event.key == K_s:
                    move("down")
                elif event.key == K_LEFT or event.key == K_a:
                    move("left")
                elif event.key == K_RIGHT or event.key == K_d:
                    move("right")
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    undo() # on ctrl + z
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_y and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    redo() # on ctrl + y

            # Draw everything:
            screen.fill(BACKGROUND_COLOR)

            # Update the screen mode based on status. Necessary because an undo button was added to the game over page:
            set_screen()

            draw_grid()
            restart_button, undo_button, redo_button = draw_side_panel()

            if get_status() == "win":
                restart_button, continue_button = draw_win()
            elif get_status() == "gameOver":
                restart_button, undo_button = draw_game_over()
            elif get_status() == "addict":
                quit_button = draw_custom_text("Ok you win, now get a life :)", "Get a life")

            pygame.display.flip()

start()
update()
