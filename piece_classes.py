import board

class Piece:
    def __init__(self, position, color, board):
        self.position = position
        self.color = color
        if color == "White":
            self.opposite_color = "Black"
        else:
            self.opposite_color = "White"
        self.board = board
        self.has_moved = False
        self.possible_moves = []
        self.type_name = type(self).__name__

    def list_possible_moves(self):
        return []


class Pawn(Piece):
    def __init__(self, position, color, board):
        super().__init__(position, color, board)
        self.type_name = "Pawn"

    def list_possible_moves(self):
        if self.color == "White":
            self.possible_moves.append([self.position[0]+1, self.position[1]])
            self.possible_moves.append([self.position[0]+2, self.position[1]])
            if self.position[1] != 8:
                self.possible_moves.append([self.position[0]+1, self.position[1]+1])
            if self.position[1] != 1:
                self.possible_moves.append([self.position[0]+1, self.position[1]-1])

            one_forward = [self.position[0]+1, self.position[1]]
            two_forward = [self.position[0]+2, self.position[1]]
            right_diagonal = [self.position[0] + 1, self.position[1] + 1]
            left_diagonal = [self.position[0]+1, self.position[1]-1]

            if self.has_moved or self.board.get_square(one_forward) != "Empty" and two_forward in self.possible_moves:
                self.possible_moves.remove(two_forward)
            elif not self.has_moved:
                if self.board.get_square(two_forward) != "Empty" and two_forward in self.possible_moves:
                    self.possible_moves.remove(two_forward)

            if not self.board.get_square(one_forward) == "Empty" and one_forward in self.possible_moves:
                self.possible_moves.remove(one_forward)

            if self.board.get_square(right_diagonal) != "Black" and right_diagonal in self.possible_moves:
                self.possible_moves.remove(right_diagonal)

            if self.board.get_square(left_diagonal) != "Black" and left_diagonal in self.possible_moves:
                self.possible_moves.remove(left_diagonal)

            en_passant_permitted = True
            if en_passant_permitted:
                if self.position[0] == 5:
                    past_move = self.board.past_move
                    print(past_move)
                    right_move = [[self.position[0]+2, self.position[1]+1], [self.position[0], self.position[1]+1]]
                    left_move = [[self.position[0]+2, self.position[1]-1], [self.position[0], self.position[1]-1]]

                    print(right_move, left_move)

                    left_piece = self.board.get_piece([self.position[0], self.position[1]-1])
                    if left_piece is not None:
                        if left_piece.type_name == "Pawn":
                            if past_move == left_move:
                                self.possible_moves.append(left_diagonal)

                    right_piece = self.board.get_piece([self.position[0], self.position[1]+1])
                    if right_piece is not None:
                        if right_piece.type_name == "Pawn":
                            if past_move == right_move:
                                self.possible_moves.append(right_diagonal)

        else:
            self.possible_moves.append([self.position[0]-1, self.position[1]])
            self.possible_moves.append([self.position[0]-2, self.position[1]])
            self.possible_moves.append([self.position[0]-1, self.position[1]-1])
            self.possible_moves.append([self.position[0]-1, self.position[1]+1])

            one_forward = [self.position[0]-1, self.position[1]]
            two_forward = [self.position[0]-2, self.position[1]]
            right_diagonal = [self.position[0] - 1, self.position[1] - 1]
            left_diagonal = [self.position[0] - 1, self.position[1] + 1]

            if self.has_moved or self.board.get_square(one_forward) != "Empty" and two_forward in self.possible_moves:
                self.possible_moves.remove(two_forward)
            if not self.has_moved:
                if self.board.get_square(two_forward) != "Empty" and two_forward in self.possible_moves:
                    self.possible_moves.remove(two_forward)

            if not self.board.get_square(one_forward) == "Empty" and one_forward in self.possible_moves:
                self.possible_moves.remove(one_forward)

            if self.board.get_square(right_diagonal) != "White" and right_diagonal in self.possible_moves:
                self.possible_moves.remove(right_diagonal)

            if self.board.get_square(left_diagonal) != "White" and left_diagonal in self.possible_moves:
                self.possible_moves.remove(left_diagonal)

            en_passant_permitted = True
            if en_passant_permitted:
                if self.position[0] == 4:
                    past_move = self.board.past_move
                    right_move = [[self.position[0] - 2, self.position[1] - 1],
                                  [self.position[0], self.position[1] - 1]]
                    left_move = [[self.position[0] - 2, self.position[1] + 1], [self.position[0], self.position[1] + 1]]

                    right_diagonal = [self.position[0] - 1, self.position[1] - 1]
                    left_diagonal = [self.position[0] - 1, self.position[1] + 1]

                    left_piece = self.board.get_piece([self.position[0], self.position[1] + 1])
                    if left_piece is not None:
                        if left_piece.type_name == "Pawn":
                            if past_move == left_move:
                                self.possible_moves.append(left_diagonal)

                    right_piece = self.board.get_piece([self.position[0], self.position[1] - 1])
                    if right_piece is not None:
                        if right_piece.type_name == "Pawn":
                            if past_move == right_move:
                                self.possible_moves.append(right_diagonal)

        return self.possible_moves


class Rook(Piece):
    def __init__(self, position, color, board):
        super().__init__(position, color, board)
        self.type_name = "Rook"

    def list_possible_moves(self):
        possible_position = self.position

        while self.board.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0] + 1, possible_position[1]]
            if self.board.get_square(possible_position) == "Empty":
                self.possible_moves.append(possible_position)
            elif self.board.get_square(possible_position) == self.opposite_color:
                self.possible_moves.append(possible_position)
                break
            elif self.board.get_square(possible_position) == self.color:
                break

        possible_position = self.position

        while self.board.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0] - 1, possible_position[1]]
            if self.board.get_square(possible_position) == "Empty":
                self.possible_moves.append(possible_position)
            elif self.board.get_square(possible_position) == self.opposite_color:
                self.possible_moves.append(possible_position)
                break
            elif self.board.get_square(possible_position) == self.color:
                break

        possible_position = self.position

        while self.board.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0], possible_position[1] + 1]
            if self.board.get_square(possible_position) == "Empty":
                self.possible_moves.append(possible_position)
            elif self.board.get_square(possible_position) == self.opposite_color:
                self.possible_moves.append(possible_position)
                break
            elif self.board.get_square(possible_position) == self.color:
                break

        possible_position = self.position
        while self.board.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0], possible_position[1] - 1]
            if self.board.get_square(possible_position) == "Empty":
                self.possible_moves.append(possible_position)
            elif self.board.get_square(possible_position) == self.opposite_color:
                self.possible_moves.append(possible_position)
                break
            elif self.board.get_square(possible_position) == self.color:
                break

        return self.possible_moves


class Bishop(Piece):
    def __init__(self, position, color, board):
        super().__init__(position, color, board)
        self.type_name = "Bishop"

    def list_possible_moves(self):
        possible_position = self.position

        while self.board.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0] + 1, possible_position[1] + 1]
            if self.board.get_square(possible_position) == "Empty":
                self.possible_moves.append(possible_position)
            elif self.board.get_square(possible_position) == self.opposite_color:
                self.possible_moves.append(possible_position)
                break
            elif self.board.get_square(possible_position) == self.color:
                break

        possible_position = self.position

        while self.board.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0] - 1, possible_position[1] - 1]
            if self.board.get_square(possible_position) == "Empty":
                self.possible_moves.append(possible_position)
            elif self.board.get_square(possible_position) == self.opposite_color:
                self.possible_moves.append(possible_position)
                break
            elif self.board.get_square(possible_position) == self.color:
                break

        possible_position = self.position

        while self.board.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0] + 1, possible_position[1] - 1]
            if self.board.get_square(possible_position) == "Empty":
                self.possible_moves.append(possible_position)
            elif self.board.get_square(possible_position) == self.opposite_color:
                self.possible_moves.append(possible_position)
                break
            elif self.board.get_square(possible_position) == self.color:
                break

        possible_position = self.position

        while self.board.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0] - 1, possible_position[1] + 1]
            if self.board.get_square(possible_position) == "Empty":
                self.possible_moves.append(possible_position)
            elif self.board.get_square(possible_position) == self.opposite_color:
                self.possible_moves.append(possible_position)
                break
            elif self.board.get_square(possible_position) == self.color:
                break

        return self.possible_moves


class Queen(Piece):
    def __init__(self, position, color, board):
        super().__init__(position, color, board)
        self.type_name = "Queen"

    def list_possible_moves(self):
        possible_position = self.position

        while self.board.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0] + 1, possible_position[1] + 1]
            if self.board.get_square(possible_position) == "Empty":
                self.possible_moves.append(possible_position)
            elif self.board.get_square(possible_position) == self.opposite_color:
                self.possible_moves.append(possible_position)
                break
            elif self.board.get_square(possible_position) == self.color:
                break

        possible_position = self.position

        while self.board.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0] - 1, possible_position[1] - 1]
            if self.board.get_square(possible_position) == "Empty":
                self.possible_moves.append(possible_position)
            elif self.board.get_square(possible_position) == self.opposite_color:
                self.possible_moves.append(possible_position)
                break
            elif self.board.get_square(possible_position) == self.color:
                break

        possible_position = self.position

        while self.board.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0] + 1, possible_position[1] - 1]
            if self.board.get_square(possible_position) == "Empty":
                self.possible_moves.append(possible_position)
            elif self.board.get_square(possible_position) == self.opposite_color:
                self.possible_moves.append(possible_position)
                break
            elif self.board.get_square(possible_position) == self.color:
                break

        possible_position = self.position

        while self.board.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0] - 1, possible_position[1] + 1]
            if self.board.get_square(possible_position) == "Empty":
                self.possible_moves.append(possible_position)
            elif self.board.get_square(possible_position) == self.opposite_color:
                self.possible_moves.append(possible_position)
                break
            elif self.board.get_square(possible_position) == self.color:
                break

        possible_position = self.position

        while self.board.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0] + 1, possible_position[1]]
            if self.board.get_square(possible_position) == "Empty":
                self.possible_moves.append(possible_position)
            elif self.board.get_square(possible_position) == self.opposite_color:
                self.possible_moves.append(possible_position)
                break
            elif self.board.get_square(possible_position) == self.color:
                break

        possible_position = self.position

        while self.board.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0] - 1, possible_position[1]]
            if self.board.get_square(possible_position) == "Empty":
                self.possible_moves.append(possible_position)
            elif self.board.get_square(possible_position) == self.opposite_color:
                self.possible_moves.append(possible_position)
                break
            elif self.board.get_square(possible_position) == self.color:
                break

        possible_position = self.position

        while self.board.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0], possible_position[1] + 1]
            if self.board.get_square(possible_position) == "Empty":
                self.possible_moves.append(possible_position)
            elif self.board.get_square(possible_position) == self.opposite_color:
                self.possible_moves.append(possible_position)
                break
            elif self.board.get_square(possible_position) == self.color:
                break

        possible_position = self.position

        while self.board.get_square(possible_position) != "Bound":
            possible_position = [possible_position[0], possible_position[1] - 1]
            if self.board.get_square(possible_position) == "Empty":
                self.possible_moves.append(possible_position)
            elif self.board.get_square(possible_position) == self.opposite_color:
                self.possible_moves.append(possible_position)

        return self.possible_moves


class Knight(Piece):
    def __init__(self, position, color, board):
        super().__init__(position, color, board)
        self.type_name = "Knight"

    def list_possible_moves(self):
        possible_squares = []
        if self.position[1] < 7:
            possible_squares.append([self.position[0] + 1, self.position[1] + 2])
            possible_squares.append([self.position[0] - 1, self.position[1] + 2])
        if self.position[1] > 2:
            possible_squares.append([self.position[0] - 1, self.position[1] - 2])
            possible_squares.append([self.position[0] + 1, self.position[1] - 2])
        if self.position[0] < 7:
            possible_squares.append([self.position[0] + 2, self.position[1] + 1])
            possible_squares.append([self.position[0] + 2, self.position[1] - 1])
        if self.position[0] > 2:
            possible_squares.append([self.position[0] - 2, self.position[1] - 1])
            possible_squares.append([self.position[0] - 2, self.position[1] + 1])

        if self.position[0] == 1:
            if [self.position[0] - 1, self.position[1] + 2] in possible_squares:
                possible_squares.remove([self.position[0] - 1, self.position[1] + 2])
            if [self.position[0] - 1, self.position[1] - 2] in possible_squares:
                possible_squares.remove([self.position[0] - 1, self.position[1] - 2])

        if self.position[1] == 1:
            if [self.position[0] - 2, self.position[1] - 1] in possible_squares:
                possible_squares.remove([self.position[0] - 2, self.position[1] - 1])
            if [self.position[0] + 2, self.position[1] - 1] in possible_squares:
                possible_squares.remove([self.position[0] + 2, self.position[1] - 1])

        if self.position[0] == 8:
            if [self.position[0] + 1, self.position[1] + 2] in possible_squares:
                possible_squares.remove([self.position[0] + 1, self.position[1] + 2])
            if [self.position[0] + 1, self.position[1] - 2] in possible_squares:
                possible_squares.remove([self.position[0] + 1, self.position[1] - 2])

        if self.position[1] == 8:
            if [self.position[0] - 2, self.position[1] + 1] in possible_squares:
                possible_squares.remove([self.position[0] - 2, self.position[1] + 1])
            if [self.position[0] + 2, self.position[1] + 1] in possible_squares:
                possible_squares.remove([self.position[0] + 2, self.position[1] + 1])

        self.possible_moves = possible_squares

        for square in possible_squares:
            if self.board.get_square(square) == self.color:
                self.possible_moves.remove(square)

        self.possible_moves = possible_squares

        return self.possible_moves


class King(Piece):
    def __init__(self, position, color, board):
        super().__init__(position, color, board)
        self.type_name = "King"

    def list_possible_moves(self):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    square = [self.position[0]+i, self.position[1]+j]
                    if 1 <= self.position[0]+i <= 8 and 1 <= self.position[1]+j <= 8:
                        if self.board.get_square(square) == self.opposite_color or self.board.get_square(square) == "Empty":
                            self.possible_moves.append(square)

        castle_permitted = True
        if castle_permitted:
            if not self.has_moved:
                if not self.board.is_threatened(self.position, self.color):
                    if self.color == "White":
                        rook_a1 = self.board.get_piece([1, 1])
                        if rook_a1 is not None:
                            if not rook_a1.has_moved:
                                if self.board.get_square([1, 2]) == "Empty" and self.board.get_square(
                                        [3, 1]) == "Empty" and self.board.get_square([1, 4]) == "Empty":
                                    if not self.board.is_threatened([1, 3], self.color) and not self.board.is_threatened([1, 3], self.color):
                                        self.possible_moves.append([1, 3])

                        rook_h1 = self.board.get_piece([1, 8])
                        if rook_h1 is not None:
                            if not rook_h1.has_moved:
                                if self.board.get_square([1, 6]) == "Empty" and self.board.get_square([1, 7]) == "Empty":
                                    self.possible_moves.append([1, 7])

                    if self.color == "Black":
                        rook_a8 = self.board.get_piece([8, 1])
                        if rook_a8 is not None:
                            if not rook_a8.has_moved:
                                if self.board.get_square([8, 2]) == "Empty" and self.board.get_square(
                                        [8, 3]) == "Empty" and self.board.get_square([4, 8]) == "Empty":
                                    if not self.board.is_threatened([8, 2], self.color) and not self.board.is_threatened(
                                            [8, 3], self.color) and not self.board.is_threatened([8, 4], self.color)\
                                            and not self.board.is_threatened([8, 5], self.color):
                                        self.possible_moves.append([8, 3])

                        rook_h8 = self.board.get_piece([8, 8])
                        if rook_h8 is not None:
                            if not rook_h8.has_moved:
                                if self.board.get_square([8, 6]) == "Empty" and self.board.get_square([8, 7]) == "Empty"\
                                        and not self.board.is_threatened([8, 5], self.color) and not\
                                        self.board.is_threatened([8, 6], self.color) and not\
                                        self.board.is_threatened([8, 7], self.color):
                                    self.possible_moves.append([8, 7])
        return self.possible_moves



























