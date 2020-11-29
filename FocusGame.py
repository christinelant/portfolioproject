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
        board is set to None
        """
        self._player_A = tuple_1
        self._player_B = tuple_2
        self._player_turn = None

        self._captured_pieces_A = []
        self._caputured_pieces_B = []

        self._reserve_pieces_A = []
        self._reserve_pieces_B = []

        # self._board = [[None for i in range(0, 5)] for i in range(0, 5)]
        self._board = [
            [[], [], [], [], [], []],
            [[], [], [], [], [], []],
            [[], [], [], [], [], []],
            [[], [], [], [], [], []],
            [[], [], [], [], [], []],
            [[], [], [], [], [], []],
        ]

        print(self._board)


    def move_piece(self, player, new_location, current_location, spaces_to_move):
        """
        moves specified player's piece if move is possible
        otherwise, returns an error based on any of the following:
        player turn, invalid locations (new or current location),
        invalid number of places being moved
        """

        current_player_turn = self.get_current_player(player)

        if player != current_player_turn:
            return False

        player_piece = self.get_player_piece(player)

        #cycle to next player
        self.change_player()

    def get_current_player(self, player):
        """
        returns the current turn’s player, if no current player, will set self._player_turn
        """

        # first move of the game
        if self._player_turn is None:
            self._player_turn = player
            return player

        return self._player_turn

    def change_player(self):
        """updates player_turn from current player to next player"""

        turn = self._player_turn

        if turn == self._player_A[0]:
            self._player_turn = self._player_B[0]
        else:
            self._player_turn = self._player_A[0]

    def get_player_piece(self, player):
        """grabs the specified player's piece"""

        turn = self._player_turn

        if turn == self._player_A[0]:
            return self._player_A[1]
        else:
            return self._player_B[1]



game = FocusGame(('Unicorn', 'G'), ('PlayerB', 'R'))
game.move_piece('Unicorn', (0, 0), (0, 1), 1)  # Returns message "successfully moved"
game.move_piece('PlayerB', (0, 0), (0, 1), 1)
