# Author: Phu Manh Nguyen
# Date: 12/17/2022

from land import Land


class Property(Land):

    ONE_HOUSE_MULTIFLIER = 5
    TWO_HOUSE_MULTIFLIER = 15
    THREE_HOUSE_MULTIFLIER = 45
    FOUR_HOUSE_MULTIFLIER = 85
    HOTEL_MULTIFLIER = 125

    def __init__(self, name, price, category, base_rent, color, construction_cost):
        super().__init__(name, price, category, base_rent)
        self.color = color
        self.construction_cost = construction_cost
        self.__numHouses = 0
        self.__numHotel = 0

    def get_num_houses(self):
        return self.__numHouses

    def get_num_hotel(self):
        return self.__numHotel

    def build_house(self):
        self.__numHouses = self.__numHouses + 1

    def build_hotel(self):
        if self.__numHouses == 4:
            self.__numHotel = 1
        else:
            print(f"{self.name} must have 4 houses to construct one hotel!\n")

    def calculateRent(self):
        if self.__numHotel == 1:
            self.set_rent(self.get_rent() * self.HOTEL_MULTIFLIER)
        else:
            if self.__numHouses == 0:
                pass
            elif self.__numHouses == 1:
                self.set_rent(self.get_rent() * self.ONE_HOUSE_MULTIFLIER)
            elif self.__numHouses == 2:
                self.set_rent(self.get_rent() * self.TWO_HOUSE_MULTIFLIER)
            elif self.__numHouses == 3:
                self.set_rent(self.get_rent() * self.THREE_HOUSE_MULTIFLIER)
            else:
                self.set_rent(self.get_rent() * self.FOUR_HOUSE_MULTIFLIER)

    def __str__(self) -> str:
        return f"\nName: {self.name}\nColor: {self.color}\nPrice: ${self.price}\nRent: ${self.get_rent()}\nUpgrade: ${self.construction_cost}\nOwner: {self.owned_by()}\nHouses: {self.get_num_houses()}\nHotel: {self.get_num_hotel()}"
