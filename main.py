# Author: Phu Manh Nguyen
# Date: 12/17/2022

from gamecontroller import *


initialize_game()

i = 5

while i > 0:
    for player in game["players"]:
        move_player(player)
    i = i - 1
