# Author: Phu Manh Nguyen
# Date: 12/17/2022

from property import Property
from specials import *
from railroad import RailRoad
from tax import Tax
from utility import Utility
from player import Player
from gameview import *
from helpers import *

MIN_PLAYER = 2
MAX_PLAYER = 6
JAIL_FEE = 50
GO_CREDIT = 200
MIN_TRADE = 60
MAX_TRADE = 400

game = {"board": list(), "players": list(), "over": False}


def initialize_board():

    game["board"].append(Corner("GO"))
    game["board"].append(Property("Mediterannean Ave",
                         60, "Property", 2, "Brown", 50))
    game["board"].append(Chest("Community Chest"))
    game["board"].append(
        Property("Baltic Ave", 60, "Property", 4, "Brown", 50))
    game["board"].append(Tax("Income Tax", 200))
    game["board"].append(RailRoad("Reading Railroad", 200, "RailRoad", 25))
    game["board"].append(
        Property("Oriental Ave", 100, "Property", 6, "Teal", 50))
    game["board"].append(Chance("Chance"))
    game["board"].append(
        Property("Vermont Ave", 100, "Property", 6, "Teal", 50))
    game["board"].append(
        Property("Connecticut Ave", 120, "Property", 8, "Teal", 50))

    game["board"].append(Corner("JAIL"))
    game["board"].append(Property("St. Charles Place",
                                  140, "Property", 10, "Pink", 100))
    game["board"].append(Utility("Electric Company", 150, "Utility", 0))
    game["board"].append(
        Property("State Ave", 140, "Property", 10, "Pink", 100))
    game["board"].append(Property("Virginia Ave", 160,
                         "Property", 12, "Pink", 100))
    game["board"].append(
        RailRoad("Pennsylvania Railroad", 200, "RailRoad", 25))
    game["board"].append(Property("St. James Place", 180,
                                  "Property", 14, "Orange", 100))
    game["board"].append(Chest("Community Chest"))
    game["board"].append(Property("Tennessee Ave", 180,
                         "Property", 14, "Orange", 100))
    game["board"].append(Property("New York Ave", 200,
                         "Property", 16, "Orange", 100))

    game["board"].append(Corner("FREE PARKING"))
    game["board"].append(
        Property("Kentucky Ave", 220, "Property", 18, "Red", 150))
    game["board"].append(Chance("Chance"))
    game["board"].append(
        Property("Indiana Ave", 220, "Property", 18, "Red", 150))
    game["board"].append(
        Property("Illinois Ave", 240, "Property", 20, "Red", 150))
    game["board"].append(RailRoad("B & 0 Railroad", 200, "RailRoad", 25))
    game["board"].append(Property("Atlantic Ave", 260,
                         "Property", 22, "Yellow", 150))
    game["board"].append(
        Property("Ventnor Ave", 260, "Property", 22, "Yellow", 150))
    game["board"].append(Utility("Water Works", 150, "Utility", 0))
    game["board"].append(Property("Marvin Gardens", 280,
                                  "Property", 24, "Yellow", 150))

    game["board"].append(Corner("GO TO JAIL"))
    game["board"].append(
        Property("Pacific Ave", 300, "Property", 26, "Green", 200))
    game["board"].append(Property("North Carolina Ave",
                                  300, "Property", 26, "Green", 200))
    game["board"].append(Chest("Community Chest"))
    game["board"].append(Property("Pennsylvania Ave", 320,
                                  "Property", 28, "Green", 200))
    game["board"].append(RailRoad("Short Line", 200, "RailRoad", 25))
    game["board"].append(Chance("Chance"))
    game["board"].append(
        Property("Park Place", 350, "Property", 35, "Blue", 200))
    game["board"].append(Tax("Luxury Tax", 100))
    game["board"].append(
        Property("Broadwalk", 400, "Property", 50, "Blue", 200))


def get_card_pos(card_name):
    # Returns the index of card_name in game["board"]
    card_pos = 40  # A random index number that is greater than board_length
    for i in range(0, len(game["board"])):
        card = game["board"][i]
        if (card.name == card_name):
            card_pos = i
            break
    return card_pos


def initialize_game():
    display_welcome_message()
    initialize_board()
    display_game_setting()
    num_players = get_int(MIN_PLAYER, MAX_PLAYER, "number of players")
    for i in range(num_players):
        player_name = input(f"Enter player {i + 1}'s name: ")
        player_token = input(f"Enter player {i + 1}'s token: ")
        new_player = Player(player_name, player_token)
        game["players"].append(new_player)
    clean_console(1, "Setting up game...")
    sort_player_turn()


def sort_player_turn() -> None:
    # Sort a list of players in decending order
    print("Let's determine the turn by throwing dice.")
    print("The player with highest number will go first.\n")
    players = game["players"]
    for player in players:
        dice = player.roll_dice()
        player.last_three_rolls.pop()
        player.turn = dice[0] + dice[1]
    players.sort(key=lambda player: player.turn, reverse=True)
    display_roll_order(players)
    input("Enter to continue: ")


def set_game_over() -> None:
    # Game is over when one of the players is bankcrupt
    for player in game["players"]:
        if player.is_bankcrupt():
            game["over"] = True
            break


def move_player(player) -> None:
    clean_console(3, "LOADING...")
    display_start_turn(player)
    if player.is_in_jail():
        handle_player_in_jail(player)
    else:
        dice = player.roll_dice()
        set_new_pos(player, dice)
        handle_player_pos(player)
        player_request = get_player_request(player)
        while player_request != 0:
            handle_player_request(player, player_request)
            player_request = get_player_request(player)
        while player.has_rolled_doubles(dice) and not player.is_in_jail():
            clean_console(3, "LOADING...")
            print(f"{player.name} has rolled doubles, thus has an additional turn")
            dice = player.roll_dice()
            set_new_pos(player, dice)
            handle_player_pos(player)
            player_request = get_player_request(player)
            while player_request != 0:
                handle_player_request(player, player_request)
                player_request = get_player_request(player)
    display_end_turn(player)


def set_new_pos(player, dice) -> None:
    # Set new position for player.
    move_step = dice[0] + dice[1]
    new_pos = move_step + player.get_pos()
    if new_pos >= len(game["board"]):  # Passing GO
        new_pos = new_pos - len(game["board"])
        add_balance(player, GO_CREDIT)
    landed_card = game["board"][new_pos]
    display_player_landing(player, landed_card)
    if landed_card.name == "GO TO JAIL" or player.has_doubles_three_times():
        print(f"{player.name} is sent to Jail")
        player.set_turn_in_jail(3)
        new_pos = get_card_pos("JAIL")
    player.set_pos(new_pos)


def add_balance(player, amount) -> None:
    player.set_balance(player.get_balance() + amount)


def deduct_balance(player, amount) -> None:
    player.set_balance(player.get_balance() - amount)


def handle_player_in_jail(player) -> None:
    display_jail_options(player)
    user_selection = get_int(1, 3, "selection")
    if user_selection == 1:  # Use card
        pass
    elif user_selection == 2:  # Paid fee
        print(f"{player.name} paid ${JAIL_FEE} to get out of jail")
        player.set_balance(player.get_balance() - JAIL_FEE)
        player.set_free()
    else:  # Roll dice
        dice = player.roll_dice()
        if player.has_rolled_double(dice):
            player.set_free()
            set_new_pos(player, dice)
            handle_player_pos(player)
            player_request = get_player_request(player)
            while player_request != 0:
                handle_player_request(player, player_request)
                player_request = get_player_request(player)
        else:
            jail_turn_left = player.turn_left_in_jail()
            if jail_turn_left == 0:
                print(
                    f"No more turn left. {player.name} has to pay ${JAIL_FEE} fee")
                player.set_balance(player.get_balance() - JAIL_FEE)
                player.set_free()
            else:
                jail_turn_left == jail_turn_left - 1
                player.set_turn_in_jail(jail_turn_left)


def handle_player_pos(player) -> None:
    """ Handle all possible fees that player incurs depends on his/her position on the board"""
    card = game["board"][player.get_pos()]
    if type(card) in [Property, Utility, RailRoad]:
        rent = card.get_rent()
        if card.owned_by() is not None and player.name != card.owned_by().name and rent != 0:  # Player is not property owner
            property_owner = card.owned_by()
            deduct_balance(player, rent)  # Pay rent
            add_balance(property_owner, rent)  # Collect rent
            print(f"{player.name} paid {property_owner.name} ${rent} for rent!\n")
    elif type(card) is Tax:
        print(card)
        print(f"{player.name} must pay ${card.get_tax_amount()}\n")
        deduct_balance(player, card.get_tax_amount())
    elif type(card) in [Chance, Chest]:
        pass  # Nothing for now
    else:
        pass


def get_player_request(player) -> int:
    """ Display all possible options for player. Return player's request. """
    player_request = 0
    card = game["board"][player.get_pos()]
    # Property has no owner
    if type(card) in [Property, Utility, RailRoad] and card.owned_by() is None:
        display_player_options()
        display_buying_options()
        player_request = get_int(0, 8, "request")
    else:
        display_player_options()
        player_request = get_int(0, 6, "request")
    return player_request


def handle_player_request(player, player_request) -> None:
    """ Handle all possible requests from player """
    card = game["board"][player.get_pos()]
    if player_request == 1:  # Build house
        pass
    elif player_request == 2:  # Build hotel
        pass
    elif player_request == 3:  # Trade
        handle_trade(player)
    elif player_request == 4:  # Sell house
        pass
    elif player_request == 5:  # Sell hotel
        pass
    elif player_request == 6:  # Mortgage
        handle_mortgage(player)
    elif player_request == 7:  # Buy property
        handle_buying_property(player, card)
    else:  # Place bid
        pass


def handle_buying_property(player, landed_property) -> None:
    print()
    print(landed_property)
    response = get_response()
    if response.upper() == "Y":
        deduct_balance(player, landed_property.price)
        landed_property.set_owner(player)
        player.buy_assets(landed_property)
        print(f"Purchase {landed_property.name} successfully!\n")
        display_player_assets(player)
    else:
        print("Cancel request\n")


def handle_trade(player) -> None:
    print()
    other_players = get_other_players(player)
    print("All players' names:")
    display_players(other_players)
    other_player = get_player_by_name(other_players)
    if other_player is not None:
        display_player_assets(other_player)
        if len(other_player.get_assets()) != 0:
            asset_to_trade = get_asset_from_input(other_player)
            if (asset_to_trade is not None):
                trade_value = get_int(MIN_TRADE, MAX_TRADE, "trade value")
                trade_asset(player, other_player, asset_to_trade, trade_value)
            else:
                print(f"{player.name} cancels trade")
    else:
        print(f"{player.name} cancels trade")


def get_other_players(current_player) -> list:
    # Return a list of players that does not contain the current player
    others = list()
    for player in game["players"]:
        if not player == current_player:
            others.append(player)
    return others


def get_player_by_name(player_list) -> Player:
    # Return the player based on name entered
    player_name = input("Enter player's name (Q to quit): ")
    return_player = None
    while player_name.upper() != "Q":
        for player in player_list:
            if player.name == player_name:
                return_player = player
                player_name = "Q"  # Exit while loop
                break
        if return_player is None:
            print(f"Cannot find {player_name}. Please try again!")
            player_name = input("Enter player's name (Q to quit): ")
    return return_player


def get_asset_from_input(player):
    # Return asset based on name and category entered
    asset_category = input("Enter asset's type (Q to cancel): ")
    asset = None
    while asset_category.upper() != "Q":
        try:
            assets = player.get_assets()[asset_category]
            asset_name = input("Enter asset's name (Q to cancel): ")
            if asset_name.upper() == "Q":
                asset_category = "Q"  # Exit while loop
            else:
                for player_asset in assets:
                    if player_asset.name == asset_name:
                        asset = player_asset
                        asset_category = "Q"  # Exit while loop
                        break
                if asset is None:  # Cannot find asset_name
                    print(f"{asset_name} does not exist\n")
        except KeyError:
            print(f"{asset_category} category does not exist\n")
            asset_category = input("Enter asset's type (Q to cancel): ")
    return asset


def trade_asset(current_player, other_player, asset_to_trade, trade_value):
    print(
        f"\n{current_player.name} wants to trade ${trade_value} for {asset_to_trade.name}")
    response = get_response()
    if response.upper() == "Y":
        asset_category = asset_to_trade.type
        other_player.get_assets()[asset_category].remove(
            asset_to_trade)  # remove asset
        other_player.set_balance(
            other_player.get_balance() + trade_value)  # add balance
        current_player.set_balance(current_player.get_balance() - trade_value)
        current_player.buy_assets(asset_to_trade)
        print("Trade successfully!\n")
        asset_to_trade.set_owner(current_player)  # Set new owner
        print(asset_to_trade)
        display_player_assets(current_player)
        display_player_assets(other_player)
    else:
        print(f"{other_player.name} refuses  to trade.")


def handle_mortgage(player):
    player_assets = player.get_assets()
    if len(player_assets) == 0:  # Player does not have any asset to mortgage
        print(f"{player.name} does not have any properties to mortgage!")
    else:
        display_player_assets(player)
        property_to_mortgage = get_asset_from_input(player)
        while property_to_mortgage is not None and property_to_mortgage.is_mortgaged():  # Property already mortgaged
            print(f"{property_to_mortgage.name} was already mortgaged!\n")
            property_to_mortgage = get_asset_from_input(player)
        if property_to_mortgage is None:  # Player cancels mortgage request
            print(f"{player.name} cancels mortgage request")
        else:  # Property is found and not mortgaged yet
            property_to_mortgage.set_mortgaged()  # Set property to mortgaged
            print(f"Sucessfully mortgage {property_to_mortgage.name}")
            mortgage_value = property_to_mortgage.price // 2
            add_balance(player, mortgage_value)
            print(
                f"{player.name} received ${mortgage_value} from mortgage {property_to_mortgage.name}\n")
