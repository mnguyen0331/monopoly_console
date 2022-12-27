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

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def get_released_card(self) -> int:
        return self.__released_card

    def get_balance(self):
        return self.__cash

    def get_pos(self):
        return self.__pos

    def add_card(self, card) -> None:
        # Adding card to player's asset
        # Does not have card category yet
        if self.__assets.get(card.type, "None") == "None":
            cards = list()
            cards.append(card)
            self.__assets.update({card.type: cards})
        else:
            self.__assets[card.type].append(card)
        print(f"{self} added {card.name} to current assets!")

    def get_required_card(self, card_name) -> object:
        # Returns card if player has a card_name
        try:
            cards = self.get_assets()["Card"]
            for card in cards:
                if card.name == card_name:
                    return card
            return None
        except KeyError:
            return None

    def use_card(self, card_name) -> bool:
        # Return true if player can use card_name
        card = self.get_required_card(card_name)
        if card is None:
            print(f"\n***{self} does not have a {card_name}***")
            return False
        else:
            self.__assets["Card"].remove(card)
            if len(self.__assets["Card"]) == 0:
                self.__assets.pop("Card")
            print(f"\n{self} successfully uses {card_name}")
            return True

    def own_color_group(self, asset) -> bool:
        # Returns true if player has all assets in the same color group
        return len(self.get_assets()[asset.type][asset.color]) == COLOR_GROUPS[asset.color]

    def check_num_houses(self, asset) -> bool:
        """ Checking the number of houses of other properties in 
        the same color group as the property param. """
        other_properties = self.get_assets()[asset.type][asset.color]
        current_houses = asset.get_num_houses()
        for prop in other_properties:
            other_houses = prop.get_num_houses()
            if current_houses > other_houses:
                print(
                    f"\n***Need to construct a house on {prop.name} first***")
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
        input(f"\n{self}, enter to roll dice: ")
        first_die = random.randrange(1, 6)
        second_die = random.randrange(1, 6)
        dice = first_die, second_die
        if len(self.last_three_rolls) > 2:
            self.last_three_rolls.pop(0)
        self.last_three_rolls.append(dice)
        print(f"{self} rolls {dice}")
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
                print(f"{self} has rolled doubles three times in a row!")
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
            if asset_category == "Property":
                # Color does not exist
                if self.__assets[asset_category].get(asset.color) is None:
                    property_list = list()  # Create a new list
                    property_list.append(asset)
                    self.__assets[asset_category].update(
                        {asset.color: property_list})
                else:  # Color exists
                    self.__assets[asset_category][asset.color].append(asset)
            else:
                self.__assets[asset_category].append(asset)
        else:  # keys do not exist
            if asset_category == "Property":
                property_dict = dict()
                if property_dict.get(asset.color) is None:  # Color does not exist
                    property_list = list()  # Create a new list
                    property_list.append(asset)
                    property_dict.update({asset.color: property_list})
                else:  # Color exists
                    property_dict[asset.color].append(asset)
                self.__assets.update({asset_category: property_dict})
            else:
                asset_list = list()
                asset_list.append(asset)
                self.__assets.update({asset_category: asset_list})
        print(f"\n{self}'s purchasing {asset.name} successfully!")
        asset.set_owner(self)
        print(asset)

    def sell_assets(self, asset, amount):
        self.add_balance(amount)
        asset.set_owner(None)
        assets = self.__assets[asset.type]
        if asset.type == "Property":
            assets[asset.color].remove(asset)
            if len(assets[asset.color]) == 0:
                assets.pop(asset.color)
        else:
            assets.remove(asset)
        if len(assets) == 0:
            self.__assets.pop(asset.type)
        print(f"\n{self} sold {asset.name} for ${amount}")

    def make_payment(self, to_whom, amount, reason):
        if type(to_whom) is Player:
            to_whom.add_balance(amount)
        print(f"\n{self} paid ${amount} to {to_whom.name} for {reason}!")

    def mortgage_property(self, mortgaged_property):
        mortgaged_property.set_mortgaged()
        mortgaged_property_value = mortgaged_property.price // 2
        self.add_balance(mortgaged_property_value)
        print(f"\nSucessfully mortgaged {mortgaged_property.name}")
        print(
            f"{self} received ${mortgaged_property_value} from mortgage {mortgaged_property.name}")

    def lift_mortgage(self, property_to_lift):
        property_to_lift.lift_mortgage()
        print(f"\nSucessfully lifting mortgage of {property_to_lift.name}")
