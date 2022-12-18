# Author: Phu Manh Nguyen
# Date: 12/17/2022

from abc import abstractmethod
from player import Player


class Land:
    def __init__(self, name, price, category, base_rent):
        self.name = name
        self.price = price
        self.type = category
        self.__rent = base_rent
        self.__owned = None
        self.__mortgaged = False

    def get_rent(self):
        return self.__rent

    def owned_by(self):
        return self.__owned

    def is_mortgaged(self):
        return self.__mortgaged

    def set_owner(self, owner):
        self.__owned = owner

    def set_mortgaged(self):
        self.__mortgaged = True
        self.__rent = 0

    def set_rent(self, new_rent):
        self.__rent = new_rent

    def __str__(self) -> None:
        if (self.price != 0):
            return f"{self.name}\nPrice: ${self.price}\nRent: ${self.get_rent()}\n"
        return f"{self.name}\n"

    @abstractmethod
    def calculateRent():
        pass
