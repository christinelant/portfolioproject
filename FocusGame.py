# Author: Christine Lantigua
# Date: 11/24/2020
# Description:

class FocusGame:
    """
    Two player game where either player's goal is to capture all of
    their opponents pieces or make it so their opponent can no longer move
    """

    def __init__(self, player_info_1, player_info_2):
        """
        initializes game board with the player and the player's color
        and starting position for game pieces
        board is set to None
        """
        self._player_A = player_info_1
        self._player_B = player_info_2
        self._player_turn = None

        self._captured_pieces_A = 0
        self._captured_pieces_B = 0

        self._reserve_pieces_A = 0
        self._reserve_pieces_B = 0

        self._board = self._populate_board()
        for row in self._board:
            print(row)
        print("")

    def _populate_board(self):
        """
        Fills FocusGame board with specified player pieces
        """
        board = []

        players = [self._player_A[1], self._player_B[1]]

        for row in range(0, 6):
            row_contents = []
            play_amount = 0
            if row == 1 or row == 3 or row == 5:
                selected_player = players[1]
            else:
                selected_player = players[0]

            for col in range(0, 6):
                if play_amount == 2:
                    if selected_player == players[1]:
                        selected_player = players[0]

                    elif selected_player == players[0]:
                        selected_player = players[1]

                    play_amount = 0

                play_amount += 1
                row_contents.append([selected_player])

            board.append(row_contents)

        return board

    def move_piece(self, player, current_location, new_location, pieces_to_move):
        """
        moves specified player's piece if move is possible
        otherwise, returns an error based on any of the following:
        player turn, invalid locations (new or current location),
        invalid number of places being moved
        """

        # grab current turn
        current_player_turn = self.set_current_player(player)

        # check to see if player matches current_turn
        if player != current_player_turn:
            return False

        # grab player piece at the top of stack to see if move from starting location is valid
        player_piece = self.get_player_piece()

        # grab the top stack piece at current location to see if it matches player piece
        top_of_stack = self.top_piece(current_location)

        # stack is empty
        if top_of_stack is False:
            return False

        if player_piece != top_of_stack:
            return False

        # check new location to see if current location - new location = spaces to move
        check_for_move = self.check_move_valid(new_location, current_location, pieces_to_move)

        if check_for_move is False:
            return False

        # moves the piece, after validation above is complete
        self.update_stack(new_location, current_location, player_piece, pieces_to_move)

        # check for win
        win = self.check_for_win(player)

        if win:
            return player.upper() + " WINS"

        # switch turn to other player after successful move and no win
        self.change_player()

        return 'successfully moved'

    def set_current_player(self, player):
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

    def get_player_piece(self):
        """grabs the specified player's piece"""

        turn = self._player_turn

        if turn == self._player_A[0]:
            return self._player_A[1]
        else:
            return self._player_B[1]

    def top_piece(self, location):
        """converts the piece at the top of a stack into a string"""

        # grabs the stack at this location
        stack = self.show_pieces(location)

        if stack == []:
            return False

        length_of_stack = self.stack_length(location)

        top_piece = stack[length_of_stack - 1]

        return top_piece

    def stack_length(self, location):
        """grabs the stack length"""

        stack = self.show_pieces(location)

        return len(stack)

    def check_move_valid(self, move_piece_from, move_piece_to, pieces_to_move):
        """
        validates getting to the new position, from the current position
        (horizontally/vertically) using spaces to move
        """

        ##MAY NOT NEED
        # check if stack length at old/current location is equal or less than spaces to move
        stack_check = self.validate_move(move_piece_to, pieces_to_move)

        # spaces to move invalid
        if stack_check is False:
            return False
        ##MAY NOT NEED

        # grab the row and column of new and current position
        row_1 = move_piece_from[0]
        row_2 = move_piece_to[0]

        column_1 = move_piece_from[1]
        column_2 = move_piece_to[1]

        # get the subtraction of the two (can only move horizontal or vertically)
        horizontal = row_1 - row_2
        vertical = column_1 - column_2

        # cannot move diagonally, if both X and Y change, move is diagonal
        if abs(horizontal) and abs(vertical) > 0:
            return False

        # horizontal or vertical move has to be less than or equal to amount of pieces to move
        if abs(horizontal) <= pieces_to_move or abs(vertical) <= pieces_to_move:
            return True

        return False

    def validate_move(self, stack_location, pieces_to_move):
        """
        checks to see if stack at current position is equal to the amount of spaces
        to move
        """

        # grabs the length of stack
        length = self.stack_length(stack_location)

        # checks to see if the spaces to move is equal to stack length
        if pieces_to_move <= length:
            return True

        return False

    def show_pieces(self, location):
        """shows pieces stacked at specified location"""

        # get the row to go into and then the column via tuple
        row = location[0]
        column = location[1]

        # using row and column, get the piece at that location on board
        stack = self._board[row][column]

        return stack

    def update_stack(self, new_location, old_location, player_piece, pieces_to_move):
        """
        Updates new and old location stacks by adding or removing a
        piece(s), respectively. Piece(s) to be moved are determined by the total
        pieces within the old_stack (after being validated against stack, previously).
        """

        # grabs array at new location
        new_board_location = self.show_pieces(new_location)

        # grabs array at old location
        old_board_location = self.show_pieces(old_location)

        length_old_stack = self.stack_length(old_location)
        length_new_stack = self.stack_length(new_location)

        for piece in range(0, pieces_to_move):
            piece_to_move = old_board_location.pop()
            new_board_location.append(piece_to_move)


        if (length_old_stack + length_new_stack) > 5:
            self.set_reserve_capture(new_location, player_piece)

        #
        ##REMOVE LATER
        for row in self._board:
            print(row)
        print("")
        ##REMOVE LATER
        #

    def set_reserve_capture(self, location, player_piece):
        """
        Grabs the stack that player had made a move to and check whether or not the stack
        is more than 5. if piece at the bottom of the stack is player piece, add to reserve.
        If piece at bottom of stack is opponent piece, add to captured.
        """

        stack = self.show_pieces(location)
        stack_length = self.stack_length(location)
        current_turn = self.get_current_player()

        while stack_length > 5:
            bottom_of_stack = stack[0]

            if bottom_of_stack == player_piece:
                self.set_reserve(current_turn)
            else:
                self.set_captured(current_turn)

            stack.pop(0)

            stack_length -= 1

    def set_captured(self, current_player_turn):
        """updates the number of captured pieces by a player"""
        if current_player_turn == self._player_A[0]:
            self._captured_pieces_B += 1
        else:
            self._captured_pieces_A += 1

    def set_reserve(self, current_player_turn):
        """updates the number of reserve pieces by a player"""

        if current_player_turn == self._player_A[0]:
            self._reserve_pieces_A += 1
        else:
            self._reserve_pieces_B += 1

    def show_captured(self, player):
        """show current amount of pieces captured by player"""

        if self.check_if_player(player) is False:
            return 'Player Not Found'

        if player == self._player_A[0]:
            return self._captured_pieces_B
        else:
            return self._captured_pieces_A

    def show_reserve(self, player):
        """show current amount of pieces captured by player"""

        #player doesn't exist
        if self.check_if_player(player) is False:
            return 'Player Not Found'

        if player == self._player_A[0]:
            return self._reserve_pieces_A
        else:
            return self._reserve_pieces_B

    def check_if_player(self, player):
        """checks if player exists within game"""

        if player != self._player_A[0] and player != self._player_B[0]:
            return False

    def get_current_player(self):
        """returns the current turn's player"""
        return self._player_turn

    def check_for_win(self, player):
        """
        checks to see if player captured 6 pieces belonging to opponent
        """

        # checks if player matches init method player A
        if player == self._player_A[0]:
            total_captured = self._captured_pieces_A
        else:
            total_captured = self._captured_pieces_B

        if total_captured == 2:
            return True

        return False

game = FocusGame(('Synclair', 'S'), ('Christine', 'C'))
print(game.move_piece('Synclair', (0, 0), (0, 1), 1))  # Returns message "successfully moved"
print(game.move_piece('Christine', (0, 2), (0, 3), 1))
print(game.move_piece('Synclair', (0, 1), (0, 0), 1))  # Returns message "successfully moved"
print(game.move_piece('Christine', (1, 0), (1, 1), 1))
print(game.move_piece('Synclair', (0, 4), (0, 3), 1))
print(game.move_piece('Christine', (1, 1), (3, 1), 2))
# print(game.show_pieces((1, 2)))  # Returns ['R'])
# print(game.show_pieces((1,3))) #Returns ['R'])
print(game.move_piece('Synclair', (1, 2), (0, 2), 1))
print(game.move_piece('Christine', (5, 5), (5, 4), 1))
print(game.move_piece('Synclair', (0, 5), (0, 4), 1))
print(game.move_piece('Christine', (5, 1), (5, 0), 1))
print(game.move_piece('Synclair', (0, 4), (0, 3), 1))
print(game.move_piece('Christine', (4, 2), (4, 3), 1))
print(game.move_piece('Synclair', (0, 2), (0, 3), 1))  # stack is 5 bottom of stack is G
print(game.move_piece('Christine', (1, 4), (0, 4), 1))
print(game.move_piece('Synclair', (0, 0), (0, 1), 1))
print(game.move_piece('Christine', (0, 4), (0, 3), 1)) # 'C' is reserve
print(game.move_piece('Synclair', (1, 3), (0, 3), 1)) # 'C' is captured
print(game.move_piece('Christine', (5, 4), (3, 4), 2))
print(game.move_piece('Synclair', (2, 1), (3, 1), 1))
print(game.move_piece('Christine', (3, 5), (3, 4), 1))
# # # print(game.show_pieces((0,1))) #Returns ['R'])
print('Synclair reserve is: ', game.show_reserve('Synclair'))
print('Christine reserve is: ', game.show_reserve('Christine'))
print('Christine captured is: ',game.show_captured('Christine'))
print('Synclair captured is: ', game.show_captured('Synclair'))
