# Author: Phu Manh Nguyen
# Date: 12/17/2022

from gamecontroller import *


initialize_game()

while not game["over"]:
    for player in game["players"]:
        if not player.is_bankrupt():
            move_player(player)
    check_game_over()
