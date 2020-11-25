# Author: Christine Lantigua
# Date: 11/24/2020
# Description:


class FocusGame:
    """
    Two player game where either player's goal is to capture all of
    their opponents pieces or make it so their opponent can no longer move
    """

    def __init__(self, tuple_1, tuple_2):
        """
        initializes game board with the player and the player's color
        and starting position for game pieces
        """
        self._player_A = None
        self._player_B = None
        self._player_turn = None
        self._board = [
            ['R', 'R', 'G', 'G', 'R', 'R'],
            ['G', 'G', 'R', 'R', 'G', 'G'],
            ['R', 'R', 'G', 'G', 'R', 'R'],
            ['G', 'G', 'R', 'R', 'G', 'G'],
            ['R', 'R', 'G', 'G', 'R', 'R'],
            ['G', 'G', 'R', 'R', 'G', 'G'],
        ]

        if tuple_1[1] == 'R' or tuple_1[1] == 'r':
            self._player_A = tuple_1
            self._player_B = tuple_2
        else:
            self._player_A = tuple_2
            self._player_B = tuple_1

    def move_piece(self, player, new_location, current_location, spaces_to_move):
        """
        moves specified player's piece if move is possible
        otherwise, returns an error.
        """

        current_player = self.get_current_player(player)

        if player != current_player:
            return "not your turn"

        self.change_player(player)

    def get_current_player(self, player):
        """helps determine which player's turn it is"""

        # first move of the game
        if self._player_turn is None:
            self._player_turn = player
            return player

        return self._player_turn

    def change_player(self, player):
        """updates player_turn from current player to next player"""
        print('i am here')
        if self._player_turn == 'PlayerA':
            return self._player_turn == 'PlayerB'
        else:
            return self._player_turn == 'PlayerA'

game = FocusGame(('PlayerA', 'G'), ('PlayerB', 'R'))
game.move_piece('PlayerA', (0, 0), (0, 1), 1)  # Returns message "successfully moved"
game.move_piece('PlayerB', (0, 0), (0, 1), 1)