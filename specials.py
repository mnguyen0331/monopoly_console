# Author: Phu Manh Nguyen
# Date: 12/17/2022

class Corner:
    def __init__(self, name) -> None:
        self.name = name.upper()

    def __str__(self) -> str:
        return self.name


class Chance:
    def __init__(self, name) -> None:
        self.name = name.upper()

    def __str__(self) -> str:
        return self.name


class Chest:
    def __init__(self, name) -> None:
        self.name = name.upper()

    def __str__(self) -> str:
        return self.name
