# Author: Christine Lantigua
# Date: 11/24/2020
# Description: Two player game where either player's goal is to capture 6 opponent pieces. Game is played
#              on a 6x6 board where players are allowed to move their pieces horizontally or vertically
#              ONLY. Each board space has a stack which can contain anywhere between 0 and 5 elements.
#              The left-most element being the "bottom of the stack" and the right-most element being
#              the "top of the stack". A player can move a stack provided their piece is at the top of
#              a stack. If a player moves one stack onto a new stack, and the total length of the new stack
#              is now more than 5, the bottom of the stack will become a captured or reserve piece by
#              the player. Captured/reserved depends on the piece at the bottom, if the piece belongs to player
#              it will go into the player's reserve pieces (which they can place anywhere on the board at
#              any point, provided it is their turn). Otherwise, the piece belongs to their opponent
#              and is now considered captured. Game is played until 6 pieces are captured.
#              Player and player piece are case insensitive, either player may start the game.


class FocusGame:
    """
    Two player game where either player's goal is to capture 6 opponent pieces. Game is played on a 6x6 board
    where players are allowed to move their pieces horizontally or vertically ONLY. Players move pieces along
    the board
    """

    def __init__(self, player_info_1, player_info_2):
        """
        Initializes game board with the player and the player's color and starting position for game pieces.
        Board is set to function which populates the board with the entered player pieces.
        """
        self._player_A = player_info_1
        self._player_B = player_info_2
        self._player_turn = None

        self._captured_pieces_A = 0
        self._captured_pieces_B = 0

        self._reserve_pieces_A = 0
        self._reserve_pieces_B = 0

        self._board = self._populate_board()

        self._game_status = "UNFINISHED"

    def _populate_board(self):
        """
        Populates FocusGame board with specified player pieces, as the game is case insensitive.
        """
        board = []
        players = [self._player_A[1], self._player_B[1]]

        # 6 x 6 board
        for row in range(0, 6):
            row_contents = []
            play_amount = 0

            # there is a different piece pattern for odd/even rows, starting piece needs to be alternated
            if row == 1 or row == 3 or row == 5:
                selected_player = players[1]
            else:
                selected_player = players[0]

            for column in range(0, 6):
                if play_amount == 2:

                    # alternates between player pieces after piece is appended twice
                    if selected_player == players[1]:
                        selected_player = players[0]

                    elif selected_player == players[0]:
                        selected_player = players[1]

                    play_amount = 0

                play_amount += 1
                row_contents.append([selected_player])

            # adds finished row to the board
            board.append(row_contents)

        return board

    def move_piece(self, player, current_location, new_location, pieces_to_move):
        """
        Moves specified player's piece if move is possible, otherwise, returns an error based on
        any of the following: incorrect player turn, invalid locations (current or new location), or
        invalid number of pieces being moved. Will check for win condition after move is made, if no win
        player turn is alternated to other player.
        """

        # game is finished
        if self.get_game_status == "FINISHED":
            return False

        # check if it is the turn of the player attempting to go
        if self.check_player_turn(player) is False:
            return False

        # grab player piece at the top of stack to see if move from starting location is valid
        player_piece = self.get_player_piece()

        # grab the top stack piece at current location to see if it matches player piece
        top_of_stack = self.top_piece(current_location)

        # stack is empty -- invalid move
        if top_of_stack is False:
            return False

        # player piece is not at the top of the stack -- invalid move
        if player_piece != top_of_stack:
            return False

        # check new location to see if current location - new location = spaces to move
        if self.check_move_valid(new_location, current_location, pieces_to_move) is False:
            return False

        # updates board with new information after move has been validated above
        self.update_board(new_location, current_location, player_piece, pieces_to_move)

        # check for win
        if self.check_for_win(player):
            self._game_status = "FINISHED"
            return player.upper() + " WINS"

        # switch turn to other player after successful move and no win
        self.change_turn()

        # #
        # for row in self._board:
        #     print(row)
        # print("")
        # #

        return 'successfully moved'

    def set_current_player(self, player):
        """
        Sets the current player turn if one has not yet been set (as either player can start the game).
        """

        # first move of the game, player turn is not set
        if self._player_turn is None:
            self._player_turn = player

    def change_turn(self):
        """
        Changes PLAYER_TURN from the current player to opposite player
        """

        turn = self._player_turn

        # player turn == [name of player A]
        if turn == self._player_A[0]:
            self._player_turn = self._player_B[0]
        else:
            self._player_turn = self._player_A[0]

    def get_player_piece(self):
        """
        Returns the piece belonging to the current turn's player
        """

        turn = self._player_turn

        # player turn == [piece of player A]
        if turn == self._player_A[0]:
            return self._player_A[1]
        else:
            return self._player_B[1]

    def top_piece(self, location):
        """
        Returns the top of a stack at a specified location, as a string.
        """

        # grabs the stack at this location
        stack = self.show_pieces(location)

        # empty stack means a player cannot move FROM this location to a new location
        if stack == []:
            return False

        length_of_stack = len(stack)

        # grabs the right-most piece within the stack (top of stack)
        top_piece = stack[length_of_stack - 1]

        return top_piece

    def check_move_valid(self, move_piece_from, move_piece_to, pieces_to_move):
        """
        Validates getting to the new position, from the current position (horizontally/vertically) using
        spaces to move.
        """

        # check if stack length at old/current location is equal or less than spaces to move
        stack_check = self.validate_move(move_piece_to, pieces_to_move)

        # spaces to move invalid
        if stack_check is False:
            return False

        # grab the row and column of new and current position
        row_1 = move_piece_from[0]
        row_2 = move_piece_to[0]

        column_1 = move_piece_from[1]
        column_2 = move_piece_to[1]

        # get the subtraction of the two (can only move horizontal or vertically)
        horizontal = row_1 - row_2
        vertical = column_1 - column_2

        # cannot move diagonally, if both X and Y change, move is not horizontal or vertical
        if abs(horizontal) and abs(vertical) > 0:
            return False

        # horizontal or vertical move has to be less than or equal to amount of pieces to move
        if abs(horizontal) <= pieces_to_move or abs(vertical) <= pieces_to_move:
            return True

        return False

    def validate_move(self, stack_location, pieces_to_move):
        """
        Checks to see if stack at current position is equal to the amount of pieces to move.
        """

        # grabs the length of stack
        stack = self.show_pieces(stack_location)
        length = len(stack)

        # checks to see if the spaces to move is equal to stack length
        if pieces_to_move <= length:
            return True

        return False

    def show_pieces(self, location):
        """
        Shows the pieces at specified location by grabbing the stack.
        """

        # get the row to go into and then the column via tuple
        row = location[0]
        column = location[1]

        # using row and column, get the piece at that location on board
        stack = self._board[row][column]

        return stack

    def update_board(self, new_location, current_location, player_piece, pieces_to_move):
        """
        Updates the current location by removing pieces from the stack in reverse order and adding the
        pieces into the new location's stack. The number of pieces removed/added from the stack depends
        on the number of pieces the player wanted to move.
        """

        # grabs array at "new" location
        new_board_location = self.show_pieces(new_location)

        # grabs array at "old" location
        current_board_location = self.show_pieces(current_location)

        length_old_stack = len(current_board_location)
        length_new_stack = len(new_board_location)

        # pop from "old" location and add piece into "new" location
        for piece in range(0, pieces_to_move):
            piece_to_move = current_board_location.pop()
            new_board_location.append(piece_to_move)

        # new stack is greater than 5, grab reserve/capture pieces
        if (length_old_stack + length_new_stack) > 5:
            self.set_reserve_capture(new_location, player_piece)

    def set_reserve_capture(self, location, player_piece):
        """
        Obtains a location of a stack that is 6 or more elements. Gets the current player turn to determine
        the following: If piece at the bottom of the stack is player piece, add to player's reserve.
        If piece at bottom of stack is opponent piece, add to captured.
        """

        # grabs the stack, stack length and current turn
        stack = self.show_pieces(location)
        stack_length = len(stack)
        current_turn = self.get_current_player()

        # Repeats until the stack is 5 elements long
        while stack_length > 5:
            bottom_of_stack = stack[0]

            if bottom_of_stack == player_piece:
                self.set_reserve(current_turn)
            else:
                self.set_captured(current_turn)

            stack.pop(0)

            stack_length -= 1

    def set_captured(self, current_player_turn):
        """
        Updates the number of captured pieces by a player by 1
        """

        if current_player_turn == self._player_A[0]:
            self._captured_pieces_B += 1
        else:
            self._captured_pieces_A += 1

    def set_reserve(self, current_player_turn):
        """
        Updates the number of reserve pieces by a player by 1
        """

        if current_player_turn == self._player_A[0]:
            self._reserve_pieces_A += 1
        else:
            self._reserve_pieces_B += 1

    def show_captured(self, player):
        """
        Shows the current captured opponent pieces held by a player
        """

        # player does not exist
        if self.check_if_player(player) is False:
            return 'Player Not Found'

        if player == self._player_A[0]:
            return self._captured_pieces_B
        else:
            return self._captured_pieces_A

    def show_reserve(self, player):
        """
        Shows the current reserve pieces held by a player
        """

        # player does not exist
        if self.check_if_player(player) is False:
            return 'Player Not Found'

        if player == self._player_A[0]:
            return self._reserve_pieces_A
        else:
            return self._reserve_pieces_B

    def check_if_player(self, player):
        """
        Checks if player exists within instantiated game
        """

        if player != self._player_A[0] and player != self._player_B[0]:
            return False

    def get_current_player(self):
        """returns the current turn's player"""

        return self._player_turn

    def check_player_turn(self, player):
        """
        Checks the current turn against the player attempting to make a move. If current turn is not
        yet set (set to None), function will call set_current_player. Function will return an error if
        player attempting to make a move is not meant to go yet.
        """

        # first move of the game, player turn is not set
        if self._player_turn is None:
            self.set_current_player(player)

        # grab current turn
        current_player_turn = self.get_current_player()

        # check to see if player matches current_turn
        if player != current_player_turn:
            return False

        return True

    def check_for_win(self, player):
        """
        Checks to see if specified player captured 6 pieces belonging to opponent.
        """

        # [player name] == [name of player A]
        if player == self._player_A[0]:
            total_captured = self._captured_pieces_B
        else:
            total_captured = self._captured_pieces_A

        # win condition is 6 pieces
        if total_captured == 6:
            return True

        return False

    def reserved_move(self, player, location):
        """
        Places a reserve piece in specified location on the board. If player has no reserve pieces,
        a "No pieces in reserve" error will print.
        """

        # gets specified player's reserve
        player_reserve = self.show_reserve(player)
        current_turn = self.get_current_player()

        # returns an error if player has no reserve
        if player_reserve == 0:
            return "No pieces in reserve"

        # returns an error if not player turn
        if self.check_player_turn(player) is False:
            return False

        # grabs the stack at specified location
        stack = self.show_pieces(location)

        player_piece = self.get_player_piece()

        # add player piece to top of stack
        stack.append(player_piece)

        # add pieces to reserve/captured if stack is greater than 5
        if len(stack) > 5:
            self.set_reserve_capture(location, player_piece)

        self.decrease_reserve(current_turn)

        # change current turn to next player
        self.change_turn()

        # #
        # for row in self._board:
        #     print(row)
        # print("")
        # #

        return 'reserve move successful'

    def decrease_reserve(self, current_player_turn):
        """
        Decreases reserve of a player by 1
        """

        # current player turn == [name of player A]
        if current_player_turn == self._player_A[0]:
            self._reserve_pieces_A -= 1
        else:
            self._reserve_pieces_B -= 1

    def get_game_status(self):
        """
        Returns current game status
        "UNFINISHED" or "FINISHED"
        """
        return self._game_status

# game = FocusGame(('Synclair', 'S'), ('Christine', 'C'))
# print(game.move_piece('Synclair', (0, 0), (0, 1), 1))  # Returns message "successfully moved"
# print(game.move_piece('Christine', (0, 2), (0, 3), 1))
# print(game.move_piece('Synclair', (0, 1), (0, 0), 1))  # Returns message "successfully moved"
# print(game.move_piece('Christine', (1, 0), (1, 1), 1))
# print(game.move_piece('Synclair', (0, 4), (0, 3), 1))
# print(game.move_piece('Christine', (1, 1), (3, 1), 2))
# # print(game.show_pieces((1, 2)))  # Returns ['R'])
# print(game.move_piece('Synclair', (1, 2), (0, 2), 1))
# print(game.move_piece('Christine', (5, 5), (5, 4), 1))
# print(game.move_piece('Synclair', (0, 5), (0, 4), 1))
# print(game.move_piece('Christine', (5, 1), (5, 0), 1))
# print(game.move_piece('Synclair', (0, 4), (0, 3), 1))
# print(game.move_piece('Christine', (4, 2), (4, 3), 1))
# print(game.move_piece('Synclair', (0, 2), (0, 3), 1))  # stack is 5 bottom of stack is G
# print(game.move_piece('Christine', (1, 4), (0, 4), 1))
# print(game.move_piece('Synclair', (0, 0), (0, 1), 1))
# print(game.move_piece('Christine', (0, 4), (0, 3), 1)) # 'C' is reserve
# print(game.move_piece('Synclair', (1, 3), (0, 3), 1)) # 'C' is captured
# print(game.move_piece('Christine', (5, 4), (3, 4), 2))
# print(game.move_piece('Synclair', (2, 1), (3, 1), 1))
# # print(game.move_piece('Christine', (3, 5), (3, 4), 1))
# print(game.reserved_move('Christine', (0,3)))
# print(game.move_piece('Synclair', (0, 1), (0, 3), 2))
# print(game.move_piece('Christine', (3, 5), (3, 4), 1))
# print(game.move_piece('Synclair', (3, 2), (3, 1), 1))
# print(game.move_piece('Christine', (3, 0), (3, 1), 1))
# print(game.move_piece('Synclair', (3, 3), (3, 2), 1))
# print(game.move_piece('Christine', (3, 1), (3, 4), 3))
# print(game.move_piece('Synclair', (2, 5), (1, 5), 1))
# print(game.move_piece('Christine', (3, 1), (3, 3), 2))
# print(game.move_piece('Synclair', (3, 2), (3, 3), 1))
# print(game.move_piece('Christine', (4, 3), (4, 5), 2))
# print(game.move_piece('Synclair', (3, 3), (3, 4), 1))
# print(game.move_piece('Christine', (5, 0), (5, 1), 1))
# # # # print(game.show_pieces((0,1))) #Returns ['R'])
# print('Synclair reserve is: ', game.show_reserve('Synclair'))
# print('Christine reserve is: ', game.show_reserve('Christine'))
# print('Christine captured is: ',game.show_captured('Christine'))
# print('Synclair captured is: ', game.show_captured('Synclair'))
# #
# # # #
# # # for row in self._board:
# # #     print(row)
# # # print("")
# # # #
