import pygame
from MiniMax import *

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

        # Draw everything:
        screen.fill(BACKGROUND_COLOR)
        draw_grid()
        draw_side_panel()

        if get_status() == "play":
            best_move = find_best_move(get_current_grid())
            move(best_move)
        elif get_status() == "win":
            draw_win()
        elif get_status() == "gameOver":
            draw_game_over()

        pygame.display.flip()

start()
update()
