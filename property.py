# Author: Phu Manh Nguyen
# Date: 12/17/2022

from land import Land

MAX_HOUSES = 5


class Property(Land):

    SAME_COLOR_MULTIFLIER = 2
    ONE_HOUSE_MULTIFLIER = 5
    TWO_HOUSE_MULTIFLIER = 15
    THREE_HOUSE_MULTIFLIER = 45
    FOUR_HOUSE_MULTIFLIER = 85
    HOTEL_MULTIFLIER = 125

    def __init__(self, name, price, category, base_rent, color, construction_cost):
        super().__init__(name, price, category, base_rent)
        self.color = color
        self.construction_cost = construction_cost
        self.__num_houses = 0
        self.__color_group = False

    def get_num_houses(self):
        return self.__num_houses

    def build_house(self):
        if self.get_num_houses() < MAX_HOUSES:
            self.__num_houses = self.__num_houses + 1
            if self.get_num_houses() == 5:
                print(
                    f"5 houses on {self.name} will be replaced with one hotel")
        else:
            print(
                f"\nMaximum houses reached. Cannot build anymore houses on {self.name}")

    def sell_house(self):
        self.__num_houses = self.__num_houses - 1

    def set_same_color_group(self, value) -> None:
        self.__color_group = value

    def calculateRent(self):
        num_houses = self.get_num_houses()
        if num_houses == 0:
            self.set_rent(self.get_base_rent())
        elif num_houses == 1:
            self.set_rent(self.get_base_rent() *
                          self.ONE_HOUSE_MULTIFLIER)
        elif num_houses == 2:
            self.set_rent(self.get_base_rent() *
                          self.TWO_HOUSE_MULTIFLIER)
        elif num_houses == 3:
            self.set_rent(self.get_base_rent() *
                          self.THREE_HOUSE_MULTIFLIER)
        elif num_houses == 4:
            self.set_rent(self.get_base_rent() *
                          self.FOUR_HOUSE_MULTIFLIER)
        elif num_houses == 5:
            self.set_rent(self.get_base_rent() *
                          self.HOTEL_MULTIFLIER)
        elif self.__color_group:
            self.set_rent(self.get_base_rent() * self.SAME_COLOR_MULTIFLIER)
        else:
            self.set_rent(self.get_base_rent())

    def __str__(self) -> str:
        building = "House"
        num_building = self.get_num_houses()
        if num_building == 5:
            building = "Hotel"
            num_building = 1
        return f"\nName: {self.name}\nColor: {self.color}\nPrice: ${self.price}\nRent: ${self.get_rent()}\nUpgrade: ${self.construction_cost}\nOwner: {self.owned_by()}\n{building}: {num_building}"
