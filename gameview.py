# Author: Phu Manh Nguyen
# Date: 12/17/2022

LINE_LEN = 60


def display_welcome_message() -> None:
    print("*" * LINE_LEN)
    print("Welcome to my monopoly game!\n")


def display_game_setting() -> None:
    print("How many players are playing today?")


def display_roll_order(players) -> None:
    print("The rolling order is:")
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
        print(f"{player.name}")


def display_start_turn(player) -> None:
    print(f"It's {player.name}'s TURN")
    print(f"{player.name}'s current balance: ${player.get_balance()}\n")


def display_buying_options() -> None:
    print("7. Buy property")
    print("8. Place bid\n")


def display_earning_options() -> None:
    print("Choose one of the options below to get cash:")
    print("\n1. Sell house")
    print("2. Sell hotel")
    print("3. Mortgage property")


def display_player_options() -> None:
    print("\n0. End turn")
    print("1. Build house")
    print("2. Build hotel")
    print("3. Trade")
    print("4. Sell house")
    print("5. Sell hotel")
    print("6. Mortgage property")


def display_end_turn(player) -> None:
    print(f"\n{player.name}'s turn ENDs")
    print(f"{player.name}'s current balance: ${player.get_balance()}")
    print("-" * LINE_LEN)


def display_jail_options(player) -> None:
    print(f"\n{player.name} are in jail. Below are {player.name}'s options to get out of jail: ")
    print("-" * LINE_LEN)
    print("1. Use Get Out of Jail Card")
    print("2. Paid $50")
    print("3. Roll dice\n")


def display_player_landing(player, card) -> None:
    print(f"{player.token.upper()} lands on {card.name}")


def display_player_assets(player) -> None:
    player_assets = player.get_assets()
    if len(player_assets) == 0:
        print(f"\n{player.name} does not have any assets")
    else:
        print(f"All {player.name}'s current assets:")
        for asset_type, assets in player_assets.items():
            print(f"{asset_type}: ", end="")
            for asset in assets:
                if asset_type == "Property":
                    print(
                        f"[{asset.name},{asset.color},Price: ${asset.price}, Rent: ${asset.get_rent()}]", end=" ")
                else:
                    print(
                        f"[{asset.name},Price: ${asset.price}, Rent: ${asset.get_rent()}]", end=" ")
            print("")
