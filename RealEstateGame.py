# Author: Joseph Shing
# GitHub username: misterp0p0
# Date: 06/03/2022
# Description: This program simulates a Monopoly game with a class object and included methods to play the Monopoly game. A function is used to guide the user through
# a simple way to play the game.


import random
import sys
from itertools import cycle
import itertools


class RealEstateGame:
	""" RealEstateGame class that simulates a monopoly game. This class includes methods to initialize the game, create players, move players, buy properties, and check to see if the game is over."""

	def __init__(self):
		""" constructor method """
		self._players = {}  # {name : [balance, current_square]}

	# ========================= Get Methods ==============================

	def get_players(self):
		""" returns all players and their information, which includes the players' name and their corresponding balance, current square they are on, and an iterator object storing their position."""
		return self._players


	def get_player_account_balance(self, player_name):
		""" returns the player's balance"""
		return self._players[player_name][0]


	def get_player_current_position(self, player_name):
		""" returns the player's current position on the _board. Returns 0 if the player is on the 'GO' square."""
		if self._players[player_name][1] == 'GO':
			return 0
		return self._players[player_name][1]

	def get__board_info(self):
		""" Returns information about the entire board, which shows all the squares on the board as well as the rent, purchase price, and owner for each square."""
		return list(self._board)

	# ========================= Set Methods ==============================

	def add_player_balance(self, player_name):
		""" method that adds a sum to the player's balance each time they pass the 'GO' square."""
		self._players[player_name][0] += self._bounty

	# ========================= Action Methods ===========================

	def create_spaces(self, bounty, rent_array):
		""" creates a _board and initializes the rent and purchase price for each square. There are a total of 25 squares and each square has a unique name along with a rent price and a purchase
		price that is five times the rent price. """

		self._board = {}  # initialize the _board spaces via dict data structure. {name : [rent_price, purchase price, owner]}
		self._board["GO"] = [bounty, 0, None]
		self._bounty = bounty

		for (square, rent) in zip(range(1, 25), rent_array):
			self._board[square] = [rent, rent * 5, None]


	def create_player(self, player_name, initial_balance):
		""" Creates a player and gives them a starting balance and starts them on the "GO" square """

		self._player_name = player_name
		self._initial_balance = initial_balance

		squares = list(self._board.keys())
		loop = cycle(squares)
		current = next(loop)

		self._players[player_name] = [initial_balance, current, loop]  # add the player to the player dictionary


	def buy_space(self, player_name):
		""" method to buy a space if the space is allowable to buy"""
		if self.get_player_current_position(player_name) != 0:  # check to make sure player is not on the GO square

			if self.get_player_account_balance(player_name) > self._board[self.get_player_current_position(player_name)][1]:  # if the player has enough money
				if self._board[self.get_player_current_position(player_name)][2] is None:  # if the square is not purchased
					self._players[player_name][0] -= self._board[self._players[player_name][1]][1]  # subtract purchase price from player balance
					self._board[self._players[player_name][1]][2] = player_name  # set the owner of the space to the player

					print("\nCongratulations! You just bought this property.\n")
					return True
				else:
					print("\nThis square is purchased.\n")
			else:
				print("\nYou don't have enough money.\n")

		else:
			print("\nSorry - you cannot buy the GO square.\n")
			return False	


	def move_player(self, player_name, num_move):
		""" method that takes in the player name and the number of squares they should move and then moves the character buy that number of moves. This will also cause
		players to pay rent if they land on a square that is owned by another player."""

		count = 0

		if self.get_player_account_balance(player_name) != 0:	# if the player's account balance is not 0
			while count < num_move:		# move the player by num_moves
				self._players[player_name][1] = next(self._players[player_name][2])

				if self._players[player_name][1] == "GO":	# if the player passes go, collect money
					self.add_player_balance(player_name)

				count += 1 

			if player_name != self._board[self._players[player_name][1]][2] and self.get_player_current_position(player_name) != "GO" :  # if the square doesn't belong to the player and is not GO
				# print("here")
				if self._board[self._players[player_name][1]][2] is not None:	# if the square is owned
					# print("there")
					if self.get_player_account_balance(player_name) > self._board[self._players[player_name][1]][0]:		# check to see if the player balance > rent price
						# print("lol")
						self._players[player_name][0] -= self._board[self._players[player_name][1]][0]		# subtract the rent from the player's balance
						
						self._players[self._board[self._players[player_name][1]][2]][0] += self._board[self._players[player_name][1]][0]		# pay rent to landlord

					else:	# pay all the balance of the player to the person they owe rent to. The player is then bankrupt and loses
						# print("yay")
						self._players[player_name][0] -= self._players[player_name][0]		# the player is now bankrupt: balance is 0.
						self._players[self._board[self._players[player_name][1]][2]][0] += self._players[player_name][0]		# pay the player's entire balance to the landlord

						for lots in self._board:		# iterate through _board and remove ownership from all properties that belong to player
							if self._board[lots][2] == player_name:
								self._board[lots][2] = None

		return	#  if the player's account balance is 0


	def check_game_over(self):
		""" method that checks if the game is over. The game is over when there is only one player with a balance greater than 0."""
		count = 0
		length = len(self._players)
		continue_playing = "Game is not over"

		for player in self._players:  # iterate through the player list
			if self._players[player][0] != 0:  # if the player still has money
				winner = player
			else:
				count += 1

		if count == length - 1:
			return f"The winner is {winner}"

		return continue_playing



# =========================

# Establish the game


def start_game():
	""" This function helps provide a friendly user-interface and structure for the Monopoly game. It also includes an auto-play option that will force the user to buy a square if they
	are able to and keep rolling the dice and moving players until there is a winner. Class methods can be called outside of the function for free use."""

	num_players = int(input("Welcome to the game of Monopoly. Enter the number of players: "))

	print(f"\nThank you. Initializing the game for {num_players} players...\n")

	rent_array = []

	for rent in range(1,25):
		seed = random.randrange(sys.maxsize)
		random.seed(seed)
		rent_array.append(random.randint(50, 350))  # initialize the range of the rent to be randomized numbers from 50 to 350. 


	game = RealEstateGame()

	game.create_spaces(500, rent_array)  # initialize the game so that players collect 500 dollars each time they pass the GO square

	for num in range(1, num_players+1):
		name = input(f"Enter player {num}'s name: ")

		while name in game.get_players():
			name = input(f"This player already exists. Please re-enter player {num}'s name: ")

		game.create_player(name, 1000)	# create each player with a starting balance of 1000.


	print("\nGreat! Now let's establish who goes first. We'll base it off of order of name entry, so:\n")
	
	names = game._players.keys()
	name_loop = cycle(names)
	number = 0
	for name in names:
		number += 1

		print(f"{number}. {name}")
	print("\nLet's start playing and rolling that dice!\n")

# =======================================================================
	current_player = next(name_loop)
	num_turns = 0

	while game.check_game_over() == "Game is not over":
 		
 		choices = ['1','2','3','4','5','6']

 		print("\n(1) Roll Dice\n(2) Check player balance\n(3) Check player's current position\n(4) Get player standings\n(5) Get the _board info\n(6) Auto-move until someone wins.\n")
 		action = input("What would you like to do? Enter a number from the menu: ")

 		while action not in choices:
 			action = input("That is an invalid entry. Please enter a valid entry: ")

	 	if action == '1':  # roll dice
	
	 		random_roll = random.randint(1,6)
	 		
	 		print(f"\nThe dice roll was: {random_roll}.\n")

	 		print(f"\n{current_player} moves {random_roll} spaces forward.\n")
	 		game.move_player(current_player, random_roll)

	 		decision = str(input("Would you like to see if you can buy this property? Enter Y or N (case-sensitive): "))
	 		
	 		while decision != "Y" and decision != "N":

	 			decision = str(input("That is an invalid entry. Please try again. Please enter Y or N: "))
	 			
	 		if decision == "Y":
	 			game.buy_space(current_player)
	 			current_player = next(name_loop)
	 		else:
	 			current_player = next(name_loop)
	 		
	 	if action == '2':

	 		print(f"\n{current_player}'s balance is: {game.get_player_account_balance(current_player)}\n")

	 	if action == '3':
	 		print(f"\n{current_player} is currently on square {game.get_player_current_position(current_player)}\n")
	 		
	 	if action == '4':
	 		print("Players and their information, which includes the players' name and their corresponding balance, current square they are on, and an iterator object storing their position are shown below.")
	 		print("\n")
	 		print(game.get_players())
	 		print("\n")

	 	if action == '5':
	 		print("The board starts with a GO square and is followed by the list of board spaces below. The players will cycle through the board.")
	 		print("\n")
	 		print(game.get__board_info())
	 		print("\n")

	 	if action == '6':

	 		while game.check_game_over() == "Game is not over":
	 			random_roll = random.randint(1,6)
	 			print(f"\nThe dice roll was: {random_roll}.\n")
	 			game.move_player(current_player, random_roll)
	 			game.buy_space(current_player)
	 			current_player = next(name_loop)
	 			num_turns += 1

	 		print(f"The automated game lasted a total of {num_turns} turns.\n")


	 		
	print(game.check_game_over())
	print("\n")


# =========================
start_game()
