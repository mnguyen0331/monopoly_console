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
        self.__base_rent = base_rent
        self.__owned = None
        self.__mortgaged = False

    def get_rent(self):
        return self.__rent

    def get_base_rent(self):
        return self.__base_rent

    def owned_by(self):
        return self.__owned

    def is_mortgaged(self):
        return self.__mortgaged

    def set_owner(self, owner):
        self.__owned = owner

    def set_mortgaged(self):
        self.__mortgaged = True

    def lift_mortgage(self):
        self.__mortgaged = False

    def set_rent(self, new_rent):
        self.__rent = new_rent

    def __str__(self) -> None:
        return f"\n{self.name}\nPrice: ${self.price}\nOwner: {self.owned_by()}"

    @abstractmethod
    def calculateRent():
        pass
