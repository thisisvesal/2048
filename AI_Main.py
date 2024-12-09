import pygame
import time
import sys
from pygame.locals import *
from MiniMax import *

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

        # Draw everything:
        screen.fill(BACKGROUND_COLOR)
        draw_grid()
        restart_button, undo_button, redo_button = draw_side_panel()

        if get_status() == "win":
            restart_button, continue_button = draw_win()
        elif get_status() == "gameOver":
            restart_button = draw_game_over()
        elif get_status() == "addict":
            quit_button = draw_custom_text("Ok you win, now get a life :)", "Get a life")

        if not is_AI_mode():
            print("Not AI, use the other Main.py to play yourself")
            break

        if get_status() == "play":
            best_move = find_best_move(get_current_grid())
            print(f"Best move: {best_move}")
            move(best_move)

        pygame.display.flip()

start()
update()
