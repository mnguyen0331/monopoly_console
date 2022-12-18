# Author: Phu Manh Nguyen
# Date: 12/17/2022

from land import Land


class RailRoad(Land):

    OWN_ONE_MULTIFLIER = 1
    OWN_TWO_MULTIFLIER = 2
    OWN_THREE_MULTIFLIER = 4
    OWN_FOUR_MULTIFLIER = 8

    def __init__(self, name, price, category, base_rent):
        super().__init__(name, price, category, base_rent)

    def calculateRent(self, num_own):
        if num_own == 2:
            self.set_rent(self.get_rent * self.OWN_TWO_MULTIFLIER)
        elif num_own == 3:
            self.set_rent(self.get_rent * self.OWN_THREE_MULTIFLIER)
        elif num_own == 4:
            self.set_rent(self.get_rent * self.OWN_FOUR_MULTIFLIER)
        else:
            self.set_rent(self.get_rent * self.OWN_ONE_MULTIFLIER)
