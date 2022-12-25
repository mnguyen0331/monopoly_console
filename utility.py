# Author: Phu Manh Nguyen
# Date: 12/17/2022

from land import Land


class Utility(Land):

    SINGLE_UTI_MULTIPLIER = 4
    DOUBLE_UTI_MULTIPLIER = 10

    def __init__(self, name, price, category, base_rent):
        super().__init__(name, price, category, base_rent)

    def calculateRent(self, num_on_dice, has_two_utility):
        if has_two_utility:
            self.set_rent(self.DOUBLE_UTI_MULTIPLIER * num_on_dice)
        else:
            self.set_rent(self.SINGLE_UTI_MULTIPLIER * num_on_dice)
