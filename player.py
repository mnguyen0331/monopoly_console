# Author: Phu Manh Nguyen
# Date: 12/17/2022

import random

COLOR_GROUPS = {"Brown": 2, "Teal": 3, "Pink": 3,
                "Orange": 3, "Red": 3, "Yellow": 3, "Green": 3, "Blue": 2}


class Player:
    def __init__(self, name, token):
        self.name = name
        self.token = token
        self.turn = 0
        self.last_three_rolls = list()
        self.__cash = 1500
        self.__pos = 0
        self.__in_jail = 0
        self.__bankrupt = False
        self.__assets = dict()
        self.__property_color_groups = dict()

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def get_released_card(self) -> int:
        return self.__released_card

    def get_balance(self):
        return self.__cash

    def get_pos(self):
        return self.__pos

    def get_property_color_groups(self) -> dict:
        return self.__property_color_groups

    def own_color_group(self, asset) -> bool:
        # Returns true if player has all assets in the same color group
        return self.__property_color_groups[asset.color] == COLOR_GROUPS[asset.color]

    def check_num_houses(self, asset) -> bool:
        """ Checking the number of houses of other properties in 
        the same color group as the property param. """
        property_list = self.get_assets()["Property"]
        same_color_list = list()
        for prop in property_list:
            if prop.color == asset.color:
                same_color_list.append(prop)
        for prop in same_color_list:
            if asset.get_num_houses() - prop.get_num_houses() > 1:
                return False
        return True

    def is_bankrupt(self):
        return self.__bankrupt

    def is_in_jail(self):
        return self.__in_jail != 0

    def turn_left_in_jail(self):
        return self.__in_jail

    def set_turn_in_jail(self, turn):
        self.__in_jail = turn

    def set_free(self):
        self.__in_jail = 0

    def get_assets(self):
        return self.__assets

    def set_balance(self, new_balance):
        self.__cash = new_balance

    def add_balance(self, amount) -> None:
        self.__cash = self.__cash + amount

    def deduct_balance(self, amount) -> bool:
        self.__cash = self.__cash - amount

    def roll_dice(self) -> tuple:
        # Roll the dice. Return a tuple of two integers
        input(f"\n{self.name}, enter to roll dice: ")
        first_die = random.randrange(1, 6)
        second_die = random.randrange(1, 6)
        dice = first_die, second_die
        if len(self.last_three_rolls) > 2:
            self.last_three_rolls.pop(0)
        self.last_three_rolls.append(dice)
        print(f"{self.name} rolls {dice}")
        return dice

    def has_rolled_doubles(self, dice):
        return dice[0] == dice[1]

    def has_doubles_three_times(self):
        if len(self.last_three_rolls) > 2:
            third_to_last = self.last_three_rolls[0]
            second_to_last = self.last_three_rolls[1]
            last = self.last_three_rolls[2]
            if self.has_rolled_doubles(third_to_last) and \
                    self.has_rolled_doubles(second_to_last) and \
                    self.has_rolled_doubles(last):
                print(f"{self.name} has rolled doubles three times in a row!")
                return True
        return False

    def set_pos(self, new_pos):
        self.__pos = new_pos

    def set_bankrupt(self):
        self.__bankrupt = True

    def __str__(self) -> str:
        return f"{self.name}"

    def buy_assets(self, asset):
        asset_category = asset.type
        existed_asset_category = self.__assets.keys()
        if asset_category in existed_asset_category:
            self.__assets[asset_category].append(asset)
        else:
            asset_list = list()
            asset_list.append(asset)
            self.__assets.update({asset_category: asset_list})
        if asset.type == "Property":
            existed_color_groups = self.get_property_color_groups().keys()
            if asset.color in existed_color_groups:
                previous_color_count = self.__property_color_groups[asset.color]
                self.__property_color_groups.update(
                    {asset.color: previous_color_count + 1})
            else:
                self.__property_color_groups.update({asset.color: 1})
            if self.own_color_group(asset):
                asset.set_same_color_group()
        print(f"\n{self.name}'s purchasing {asset.name} successfully!")
        if asset.type != "Card":
            asset.set_owner(self)
            print(asset)

    def sell_assets(self, asset, amount):
        self.add_balance(amount)
        asset.set_owner(None)
        assets = self.__assets[asset.type]
        assets.remove(asset)
        if len(assets) == 0:
            self.__assets.pop(asset.type)
        print(f"\n{self.name} sold {asset.name} for ${amount}")

    def make_payment(self, to_whom, amount, reason):
        if type(to_whom) is Player:
            to_whom.add_balance(amount)
        print(f"\n{self.name} paid ${amount} to {to_whom.name} for {reason}!")

    def mortgage_property(self, mortgaged_property):
        mortgaged_property.set_mortgaged()
        mortgaged_property_value = mortgaged_property.price // 2
        self.add_balance(mortgaged_property_value)
        print(f"nSucessfully mortgaged {mortgaged_property.name}")
        print(
            f"{self.name} received ${mortgaged_property_value} from mortgage {mortgaged_property.name}")
