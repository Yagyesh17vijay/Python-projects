import random

def roll_dice():
    return random.randint(1, 6)

def move_player(player_position, dice_roll, snakes, ladders):
    player_position += dice_roll
    if player_position in snakes:
      print("Oops! Snake bite!")
      player_position = snakes[player_position]
    elif player_position in ladders:
      print("Yay! Climbed a ladder!")
      player_position = ladders[player_position]
    if player_position > 100:
        player_position = 200 - player_position
    return player_position

def snake_ladder_game():
    snakes = {17: 7, 54: 34, 62: 19, 98: 79}
    ladders = {3: 21, 8: 30, 28: 84, 58: 77, 75: 86, 80: 100}
    player1_name = input("Enter player 1 name: ")
    player2_name = input("Enter player 2 name: ")
    player1_position = 0
    player2_position = 0
    turn = 0

    while True:
        turn += 1
        print(f"\nTurn {turn}:")
        if turn % 2 != 0:
            print(f"{player1_name}'s turn")
            input("Press Enter to roll the dice...")
            dice_roll = roll_dice()
            print(f"You rolled a {dice_roll}")
            player1_position = move_player(player1_position, dice_roll, snakes, ladders)
            print(f"{player1_name}'s new position: {player1_position}")
            if player1_position == 100:
                print(f"{player1_name} wins!")
                break
        else:
            print(f"{player2_name}'s turn")
            input("Press Enter to roll the dice...")
            dice_roll = roll_dice()
            print(f"You rolled a {dice_roll}")
            player2_position = move_player(player2_position, dice_roll, snakes, ladders)
            print(f"{player2_name}'s new position: {player2_position}")
            if player2_position == 100:
                print(f"{player2_name} wins!")
                break

snake_ladder_game()