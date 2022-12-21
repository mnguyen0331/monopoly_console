# Author: Phu Manh Nguyen
# Date: 12/17/2022

import random


class Corner:
    def __init__(self, name) -> None:
        self.name = name.upper()

    def __str__(self) -> str:
        return self.name


class Chance:
    def __init__(self, name) -> None:
        self.name = name.upper()
        self.__action = random.randint(1, 6)

    def get_action(self) -> int:
        return self.__action

    def __str__(self) -> str:
        return self.name


class Chest:
    def __init__(self, name) -> None:
        self.name = name.upper()
        self.__action = random.randint(1, 4)

    def get_action(self) -> int:
        return self.__action

    def __str__(self) -> str:
        return self.name


class Card:
    def __init__(self, name) -> None:
        self.name = name
        self.type = "Card"
