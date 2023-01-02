# Author: Phu Manh Nguyen
# Date: 12/17/2022

LINE_LEN = 60


def display_welcome_message() -> None:
    print("*" * LINE_LEN)
    print("\nWelcome to my monopoly game!\n")


def display_game_setting() -> None:
    print("How many players are playing today?")


def display_roll_order(players) -> None:
    print("\nThe rolling order is:")
    for i in range(len(players)):
        print(f"{i + 1}. {players[i].name}")
    print("*" * LINE_LEN)


def display_board(game) -> None:
    i = 0
    for card in game["board"]:
        print(f"Square# {i}: {card.name}")
        i = i + 1


def display_players(players) -> None:
    for player in players:
        print(f"{player}")


def display_start_turn(player) -> None:
    print(f"It's {player}'s TURN")
    print(f"{player}'s current balance: ${player.get_balance()}")
    display_player_assets(player)


def display_buying_options() -> None:
    print("6. Buy property")
    print("7. Place bid\n")


def display_earning_options() -> None:
    print("Choose one of the options below to get cash:")
    print("\n1. Sell house")
    print("2. Mortgage property")
    print("3. Declare Bankruptcy")


def display_player_options() -> None:
    print("\n0. End turn")
    print("1. Build house")
    print("2. Trade")
    print("3. Sell house")
    print("4. Mortgage property")
    print("5. Lift mortgage")


def display_end_turn(player) -> None:
    print(f"\n{player}'s turn ENDs")
    print(f"{player}'s current balance: ${player.get_balance()}")
    print("-" * LINE_LEN)


def display_jail_options(player) -> None:
    print(f"\n{player} is in jail. Below are {player}'s options to get out of jail: ")
    print("-" * LINE_LEN)
    print("1. Use Get Out of Jail Card")
    print("2. Paid $50")
    print("3. Roll dice\n")


def display_player_landing(player, card) -> None:
    print(f"{player.token.upper()} lands on {card.name}")


def display_player_assets(player) -> None:
    player_assets = player.get_assets()
    if len(player_assets) == 0:
        print(f"{player} does not have any assets")
    else:
        print(f"\nAll {player}'s current assets:")
        for category in player_assets.keys():
            assets = player_assets[category]
            if category == "Property":
                print(f"{category}:")
                for color, properties in assets.items():
                    print(f"\t{color}: ", end="")
                    for prop in properties:
                        print(
                            f"[{prop.name}, Price: ${prop.price}, Mortgaged? {prop.is_mortgaged()}]", end=" ")
                    print("")
            elif category == "Card":
                print(f"{category}: ", end="")
                for card in assets:
                    print(f"[{card.name}, Price: ${card.price}]", end=" ")
                print("")
            else:
                print(f"{category}: ", end="")
                for asset in assets:
                    print(
                        f"[{asset.name}, Price: ${asset.price}, Mortgaged? {asset.is_mortgaged()}]", end=" ")
                print("")


def display_player_properties(player) -> None:
    try:
        property_dict = player.get_assets()["Property"]
        for color, properties in property_dict.items():
            print(f"{color}: ", end="")
            for prop in properties:
                print(f"[{prop.name}, {prop.get_num_houses()}]", end=" ")
                print("")
    except KeyError:
        print(f"{player} does not have any properties")


def display_quit_message(player) -> None:
    print("*" * LINE_LEN)
    print(f"\n{player} has declared bankruptcy")
    print(f"{player} will no longer be in the game\n")
    print("*" * LINE_LEN)
