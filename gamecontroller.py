# Author: Phu Manh Nguyen
# Date: 12/17/2022

from property import Property
from specials import Corner, Chance, Chest, Card
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
BIRTHDATE_GIFT = 50
INCOME_TAX_REFUND = 50
STOCK_MATURE = 100
DENTIST_FEE = 50
COLLEGE_DEBT = 100


CHANCES = {1: f"It's your birthdate. Everyone gives you ${BIRTHDATE_GIFT} for birthday gifts!",
           2: f"Income tax refund. Received ${INCOME_TAX_REFUND}.",
           3: f"Stock matures. Received ${STOCK_MATURE}",
           4: f"Dentist Fee. Paid ${DENTIST_FEE}",
           5: f"College Debt. Paid ${COLLEGE_DEBT}",
           6: "Run over the red light under DUI. Go to Jail"
           }

CHESTS = {1: "Get out of jail free card",
          2: "Rent Waiver Card",
          3: f"Advance to GO and collect ${GO_CREDIT}",
          4: "Building House Discount. One house can be constructed with half the price"
          }

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
    print("The player with highest number will go first.")
    players = game["players"]
    for player in players:
        dice = player.roll_dice()
        player.last_three_rolls.pop()
        player.turn = dice[0] + dice[1]
    players.sort(key=lambda player: player.turn, reverse=True)
    display_roll_order(players)
    input("Enter to continue: ")


def check_game_over() -> None:
    # Game is over when one of the players is bankcrupt
    for player in game["players"]:
        if player.is_bankrupt():
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
        handle_player_pos(player, dice)
        player_request = get_player_request(player)
        while player_request != 0:  # Service player's request until turn ends
            handle_player_request(player, player_request)
            player_request = get_player_request(player)
        while player.has_rolled_doubles(dice) and not player.is_in_jail():
            clean_console(3, "LOADING...")
            print(f"{player} has rolled doubles, thus has an additional turn")
            dice = player.roll_dice()
            set_new_pos(player, dice)
            handle_player_pos(player, dice)
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
        player.add_balance(GO_CREDIT)
    landed_card = game["board"][new_pos]
    display_player_landing(player, landed_card)
    if landed_card.name == "GO TO JAIL" or player.has_doubles_three_times():
        print(f"{player} is sent to Jail")
        player.set_turn_in_jail(3)
        new_pos = get_card_pos("JAIL")
    player.set_pos(new_pos)


def handle_deduct_balance(player, amount) -> None:
    while player.get_balance() < amount and not player.is_bankrupt():
        print(f"\n{player} does not have sufficient fund to cover ${amount}")
        display_earning_options()
        player_selection = get_int(1, 3, "selection")
        handle_earning_options(player, player_selection)
    if not player.is_bankrupt():
        player.deduct_balance(amount)


def handle_earning_options(player, player_selection):
    if player_selection == 1:
        handle_sell_house(player)
    elif player_selection == 2:
        handle_mortgage(player)
    else:  # Declare bankcruptcy
        if len(player.get_assets()) > 0:
            print(f"\n{player} still has some assets left!!!")
        else:
            confirmation = get_response()
            if confirmation.upper() == "Y":
                display_quit_message(player)
                player.set_bankrupt()
            else:
                print("Cancel request")


def handle_player_in_jail(player) -> None:
    display_jail_options(player)
    user_selection = get_int(1, 3, "selection")
    if user_selection == 1:  # Use card
        valid_usage = player.use_card("Jail Free Card")
        if valid_usage:
            player.set_free()
            print(f"{player} is free!")
        else:
            handle_player_in_jail(player)
    elif user_selection == 2:  # Paid fee
        print(f"{player} paid ${JAIL_FEE} to get out of jail")
        handle_deduct_balance(player, JAIL_FEE)
        player.set_free()
        print(f"{player} is free!")
    else:  # Roll dice
        dice = player.roll_dice()
        if player.has_rolled_doubles(dice):
            player.set_free()
            set_new_pos(player, dice)
            handle_player_pos(player, dice)
            player_request = get_player_request(player)
            while player_request != 0:
                handle_player_request(player, player_request)
                player_request = get_player_request(player)
        else:  # Does not roll doubles
            jail_turn_left = player.turn_left_in_jail()
            if jail_turn_left == 0:
                print(
                    f"No more turn left. {player} has to pay ${JAIL_FEE} fee")
                handle_deduct_balance(player, JAIL_FEE)
                player.set_free()
            else:
                jail_turn_left == jail_turn_left - 1
                player.set_turn_in_jail(jail_turn_left)


def handle_player_pos(player, dice) -> None:
    """ Handle all possible fees that player incurs depends on his/her position on the board"""
    card = game["board"][player.get_pos()]
    if type(card) in [Property, Utility, RailRoad]:
        property_owner = card.owned_by()
        if property_owner is not None and player != property_owner and not card.is_mortgaged():
            if type(card) is Property:
                if property_owner.own_color_group(card):
                    card.set_same_color_group(True)
                else:
                    card.set_same_color_group(False)
                card.calculateRent()
            elif type(card) is Utility:
                num_own = len(property_owner.get_assets()["Utility"])
                card.calculateRent(dice[0] + dice[1], num_own == 2)
            else:
                num_own = len(property_owner.get_assets()["RailRoad"])
                card.calculateRent(num_own)
            rent_waiver_card = player.get_required_card("Rent Waiver Card")
            if rent_waiver_card is not None:
                print(
                    f"\n{player} has a Rent Waiver Card. Using it to waive rent?")
                confirmation = get_response()
                if confirmation.upper() == "Y":
                    player.use_card("Rent Waiver Card")
                else:
                    print(f"\n{player} does not want to use Rent Waiver Card")
            else:
                handle_deduct_balance(player, card.get_rent())
                player.make_payment(property_owner, card.get_rent(), "rent")
    elif type(card) is Tax:
        print(card)
        handle_deduct_balance(player, card.get_tax_amount())
        player.make_payment(card, card.get_tax_amount(), "tax")
    elif type(card) is Chance:
        action_num = card.get_action()
        handle_chances(player, action_num)
    elif type(card) is Chest:
        action_num = card.get_action()
        handle_chests(player, action_num)
    else:  # Corner
        pass


def handle_chances(player, action_num):
    """ Handle all possible actions from chances """
    print(CHANCES[action_num])
    if action_num == 1:
        other_players = get_other_players(player)
        for other_player in other_players:
            handle_deduct_balance(other_player, BIRTHDATE_GIFT)
            other_player.make_payment(
                player, BIRTHDATE_GIFT, f"{player}'s birthday")
    elif action_num == 2:
        player.add_balance(INCOME_TAX_REFUND)
    elif action_num == 3:
        player.add_balance(STOCK_MATURE)
    elif action_num == 4:
        handle_deduct_balance(player, DENTIST_FEE)
    elif action_num == 5:
        handle_deduct_balance(player, COLLEGE_DEBT)
    else:
        player.set_turn_in_jail(3)
        player.set_pos(get_card_pos("JAIL"))


def handle_chests(player, action_num):
    """ Handle all possible actions from chests """
    print(CHESTS[action_num])
    if action_num == 1:
        player.add_card(Card("Jail Free Card", 50))
    elif action_num == 2:
        player.add_card(Card("Rent Waiver Card", 100))
    elif action_num == 3:
        player.set_pos(get_card_pos("GO"))
        player.add_balance(GO_CREDIT)
    else:
        player.add_card(Card("House Discount Card", 100))


def get_player_request(player) -> int:
    """ Display all possible options for player. Return player's request. """
    player_request = 0
    card = game["board"][player.get_pos()]
    # Property has no owner
    if type(card) in [Property, Utility, RailRoad] and card.owned_by() is None:
        display_player_options()
        display_buying_options()
        player_request = get_int(0, 7, "request")
    else:
        display_player_options()
        print("")
        player_request = get_int(0, 5, "request")
    return player_request


def handle_player_request(player, player_request) -> None:
    """ Handle all possible requests from player """
    card = game["board"][player.get_pos()]
    if player_request == 1:  # Build house
        handle_build_house(player)
    elif player_request == 2:  # Trade
        handle_trade(player)
    elif player_request == 3:  # Sell house
        handle_sell_house(player)
    elif player_request == 4:  # Mortgage
        handle_mortgage(player)
    elif player_request == 5:  # Lift mortgage
        handle_lift_mortgage(player)
    elif player_request == 6:  # Buy property
        handle_buying_property(player, card)
    else:  # Place bid
        handle_bidding(player, card)


def handle_build_house(player):
    try:
        player.get_assets()["Property"]
        display_player_assets(player)
        property_to_build = get_asset_from_input(player)
        while type(property_to_build) is not Property:
            print("\n***Incorrect type. Can only construct houses on properties only***")
            property_to_build = get_asset_from_input(player)
        if property_to_build.is_mortgaged():
            print(f"\n***Cannot build house on mortgaged property***")
        else:
            if player.own_color_group(property_to_build):
                if player.check_num_houses(property_to_build):
                    building_cost = property_to_build.construction_cost
                    print(
                        f"\nHouse construction on {property_to_build.name} costs ${building_cost}")
                    confirmation = get_response()
                    if confirmation.upper() == "Y":
                        house_discount_card = player.get_required_card(
                            "House Discount Card")
                        if house_discount_card is not None:
                            print(
                                f"\n{player} has a House Discount Card. Using it to build house with half its construction price?")
                            confirmation = get_response()
                            if confirmation.upper() == "Y":
                                player.use_card("House Discount Card")
                                handle_deduct_balance(
                                    player, building_cost // 2)
                                property_to_build.build_house()
                            else:
                                print(
                                    f"\n{player} does not want to use House Discount Card")
                                handle_deduct_balance(player, building_cost)
                                property_to_build.build_house()
                        else:
                            handle_deduct_balance(player, building_cost)
                            property_to_build.build_house()
                    else:
                        print(f"\n{player} cancels building request")
                else:
                    print(f"Unable to build house. Houses must be built linearly")
            else:
                print(
                    f"\nUnable to build house. {player} does not own a complete color set of properties")
    except KeyError:
        print(f"\n{player} does not have any properties to build houses")


def handle_sell_house(player):
    try:
        player.get_assets()["Property"]
        display_player_assets(player)
        property_to_sell = get_asset_from_input(player)
        while type(property_to_build) is not Property:
            print("\n***Incorrect type. Can only sell houses on properties only***")
            property_to_build = get_asset_from_input(player)
        if property_to_sell.get_num_houses() > 0:
            sold_value = property_to_sell.construction_cost // 2
            print(
                f"\n!!!Sold one house on {property_to_sell.name} for ${sold_value}!!!")
            confirmation = get_response()
            if confirmation.upper() == "Y":
                property_to_sell.sell_house()
                player.add_balance(sold_value)
                print(
                    f"\nSold house successfully. {player} received ${sold_value}")
                print(property_to_sell)
            else:
                print("\nCancel request")
        else:
            print(f"\n{property_to_sell.name} does not have any houses to sell!")
    except KeyError:
        print(f"\n{player} does not have any properties to sell houses")


def handle_bidding(current_player, card):
    other_players = get_other_players(current_player)
    print(f"\n{current_player} wants to buy {card.name} through bidding!")
    print("Each subsequent bid must be $10 greater than the previous bid!")
    print(f"{card.name} will belong to the highest bid or who double {card.name} price first!\n")
    min_bid = card.price // 2
    max_bid = card.price * 2
    other_players.insert(0, current_player)
    current_bid = min_bid - 10
    highest_bidder = current_player
    index = 0
    while len(other_players) > 1:
        if index >= len(other_players):
            index = 0
        player = other_players[index]
        print(f"\nThe current bid for {card.name} is ${current_bid}")
        print(f"{player}, place your bid:")
        player_response = get_response()
        if player_response.upper() == "Y":
            current_bid = get_int(current_bid + 10, max_bid, "bidding value")
            highest_bidder = player
            if current_bid == max_bid:
                print(f"\n{player} has doubled {card.name} price!")
                break
        else:
            print(f"\n{player} quits bidding!")
            # Remove player who does not participate in bidding
            other_players.pop(index)
            index = index - 1
        index = index + 1
    print(
        f"\n{card.name} was sold to {highest_bidder.name} with ${current_bid} in cash!")
    handle_deduct_balance(highest_bidder, current_bid)
    highest_bidder.buy_assets(card)


def handle_buying_property(player, landed_property) -> None:
    print(landed_property)
    response = get_response()
    if response.upper() == "Y":
        handle_deduct_balance(player, landed_property.price)
        player.buy_assets(landed_property)
    else:
        print("Cancel request")


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
                if (asset_to_trade.type == "Property" and asset_to_trade.get_num_houses() > 0):
                    print(f"\n***Cannot trade properties that have buildings on it***")
                else:
                    trade_value = get_int(MIN_TRADE, MAX_TRADE, "trade value")
                    trade_asset(player, other_player,
                                asset_to_trade, trade_value)
            else:
                print(f"\n{player} cancels trade")
    else:
        print(f"\n{player} cancels trade")


def get_other_players(current_player) -> list:
    # Return a list of players that does not contain the current player
    others = list()
    for player in game["players"]:
        if not player == current_player:
            others.append(player)
    return others


def get_player_by_name(player_list) -> Player:
    # Return the player based on name entered
    player_name = input("\nEnter player's name (Q to quit): ")
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
    asset_category = input("\nEnter asset's type (Q to cancel): ")
    asset = None
    while asset_category.upper() != "Q":
        try:
            assets = player.get_assets()[asset_category]
            if asset_category == "Property":
                color = input("Enter property's color group (Q to cancel): ")
                while color.upper() != "Q":
                    try:
                        property_list = player.get_assets()[
                            asset_category][color]
                        property_name = input(
                            "Enter property's name (Q to cancel): ")
                        if property_name.upper() == "Q":
                            color = "Q"  # Exit
                            asset_category = "Q"  # Exit
                        else:
                            for prop in property_list:
                                if prop.name == property_name:
                                    asset = prop
                                    color = "Q"  # Exit
                                    asset_category = "Q"  # Exit
                                    break
                            if asset is None:
                                print(f"\n{property_name} does not exist!!!")
                    except KeyError:
                        print(f"\n{color} group does not exist!!!")
                        color = input(
                            "Enter property's color group (Q to cancel): ")
            else:
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
                        print(f"\n{asset_name} does not exist")
        except KeyError:
            print(f"\n{asset_category} category does not exist")
            asset_category = input("\nEnter asset's type (Q to cancel): ")
    return asset


def trade_asset(current_player, other_player, asset_to_trade, trade_value):
    print(
        f"\n{current_player} wants to trade ${trade_value} for {asset_to_trade.name}")
    print(f"\n{other_player}", end=", ")
    response = get_response()
    if response.upper() == "Y":
        handle_deduct_balance(current_player, trade_value)
        other_player.sell_assets(asset_to_trade, trade_value)
        current_player.buy_assets(asset_to_trade)
    else:
        print(f"\n{other_player} refuses  to trade.")


def handle_mortgage(player):
    player_assets = player.get_assets()
    if len(player_assets) == 0:  # Player does not have any asset to mortgage
        print(f"\n{player} does not have any properties to mortgage!")
    else:
        display_player_assets(player)
        property_to_mortgage = get_asset_from_input(player)
        while property_to_mortgage is not None and property_to_mortgage.is_mortgaged():  # Property already mortgaged
            print(f"{property_to_mortgage.name} was already mortgaged!\n")
            property_to_mortgage = get_asset_from_input(player)
        if property_to_mortgage is None:  # Player cancels mortgage request
            print(f"\n{player} cancels mortgage request")
        elif property_to_mortgage.get_num_houses() > 0:
            print(
                f"\nAll houses on {property_to_mortgage.name} must be sold prior to mortgage")
        else:  # Property is found and not mortgaged yet
            player.mortgage_property(property_to_mortgage)


def handle_lift_mortgage(player):
    player_assets = player.get_assets()
    if len(player_assets) == 0:  # Player does not have any asset to lift mortgage
        print(f"\n{player} does not have any properties!")
    else:
        display_player_assets(player)
        property_to_lift = get_asset_from_input(player)
        while property_to_lift is not None and not property_to_lift.is_mortgaged():
            print(f"{property_to_lift.name} was not mortgaged!\n")
            property_to_lift = get_asset_from_input(player)
        if property_to_lift is None:  # Player cancels request
            print(f"\n{player} cancels lifting mortgage request")
        else:
            mortgaged_price = property_to_lift.price // 2
            interest = (mortgaged_price * 10) // 100
            print(
                f"\n{player} has to pay mortgaged value ${mortgaged_price} plus interest ${interest} in order to lift")
            confirmation = get_response()
            if confirmation.upper() == "Y":
                handle_deduct_balance(player, mortgaged_price + interest)
                player.lift_mortgage(property_to_lift)
            else:
                print(f"\n{player} cancels lifting mortgage request")
