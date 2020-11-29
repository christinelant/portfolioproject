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

        # self._board = [[None for i in range(self._board_size)] for i in range(self._board_size)]

        # hard coded for now -- have to change this later to populate in colors
        self._board = [
            [['R'], ['R'], ['G'], ['G'], ['R'], ['R']],
            [['G'], ['G'], ['R'], ['R'], ['G'], ['G']],
            [['R'], ['R'], ['G'], ['G'], ['R'], ['R']],
            [['G'], ['G'], ['R'], ['R'], ['G'], ['G']],
            [['R'], ['R'], ['G'], ['G'], ['R'], ['R']],
            [['G'], ['G'], ['R'], ['R'], ['G'], ['G']],
        ]


    def move_piece(self, player, current_location, new_location, spaces_to_move):
        """
        moves specified player's piece if move is possible
        otherwise, returns an error based on any of the following:
        player turn, invalid locations (new or current location),
        invalid number of places being moved
        """

        # grab current turn
        current_player_turn = self.get_current_player(player)

        # check to see if player matches current_turn
        if player != current_player_turn:
            return False

        ## VALIDATE MOVE
        # grab player piece at the top of stack to see if move from starting location is valid
        player_piece = self.get_player_piece(player)

        # may want to change this to grab the stack and then check if player_piece is in list
        piece_at_location = self.top_of_stack_to_string(current_location)

        # current_location is empty
        if piece_at_location is False:
            return False

        if player_piece != piece_at_location:
            return False

        # check new location to see if current location - new location = spaces to move
        check_for_move = self.check_new_position(new_location, current_location, spaces_to_move)

        if check_for_move is False:
            return False

        ## END VALIDATE MOVE

        # make move
        self.update_stack(new_location, current_location, player_piece)

        # switch turn to other player if move is made successfully
        self.change_player()

        return 'successfully moved'

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

    def top_of_stack_to_string(self, location):
        """converts the piece at the top of a stack into a string"""

        # grabs the stack at this location
        stack = self.show_pieces(location)

        if stack == []:
            return False

        length_of_stack = self.stack_length(location)

        top_piece = stack[length_of_stack - 1]

        # convert list to a string
        convert_to_string = ''.join(top_piece)

        return convert_to_string

    def stack_length(self, location):
        """grabs the stack length"""

        stack = self.show_pieces(location)

        return len(stack)

    def check_new_position(self, new_position, current_position, spaces_to_move):
        """
        validates getting to the new position, from the current position
        (horizontally/vertically) using spaces to move
        """

        ##MAY NOT NEED
        # check if stack at current location is
        stack_check = self.validate_move(current_position, spaces_to_move)

        # spaces to move invalid
        if stack_check is False:
            return False
        ##MAY NOT NEED

        # grab the row and column of new and current position
        row_1 = new_position[0]
        row_2 = current_position[0]

        column_1 = new_position[1]
        column_2 = current_position[1]

        # get the subtraction of the two (can only move horizontal or vertically)
        horizontal = row_1 - row_2
        vertical = column_1 - column_2

        if abs(horizontal) == spaces_to_move or abs(vertical) == spaces_to_move:
            return True

        return False


    def validate_move(self, stack_location, spaces_to_move):
        """
        checks to see if stack at current position is equal to the amount of spaces
        to move
        """

        # grabs the length of stack
        length = self.stack_length(stack_location)

        # checks to see if the spaces to move is equal to stack length
        if length != spaces_to_move:
            return False

        return True

    def show_pieces(self,location):
        """shows pieces stacked at specified location"""

        # get the row to go into and then the column via tuple
        row = location[0]
        column = location[1]

        # using row and column, get the piece at that location on board
        pieces = self._board[row][column]

        return pieces

    def update_stack(self, new_location, old_location, player_piece):
        """
        Updates new and old location stacks by adding or removing a
        piece, respectively.
        """

        # grabs array at new location
        new_board_location = self.show_pieces(new_location)

        # updates board location array with player piece (top of stack)
        new_board_location.append(player_piece)

        # grabs array at old location
        old_board_location = self.show_pieces(old_location)

        # pops off the last item on a list
        old_board_location.pop()

        print(self._board)


game = FocusGame(('Unicorn', 'R'), ('PlayerB', 'G'))
print(game.move_piece('Unicorn', (0, 0), (0, 1), 1))  # Returns message "successfully moved"
print(game.move_piece('PlayerB', (0, 2), (0, 3), 1))
print(game.move_piece('Unicorn', (0, 1), (0, 3), 2))  # Returns message "successfully moved"
print(game.move_piece('PlayerB', (1, 0), (1, 1), 1))
print(game.move_piece('Unicorn', (0, 4), (0, 3), 1))
game.show_pieces((0,3)) #Returns ['R'])
